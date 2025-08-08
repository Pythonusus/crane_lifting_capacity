"""
Module for database operations related to crane data.

This module handles writing crane data and attachments to the database,
including checking for existing entries and handling updates.
"""

from pprint import pprint
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.models import CraneBinaryAttachmentDbModel, CraneDbModel
from app.db.queries import get_crane_db_model_by_name
from app.schemas.cranes import Crane


def write_cranes_to_db(crane_data_list: List[Crane], db_url: str) -> None:
    """
    Write crane data to database, handling updates
    for existing entries and attachments.

    Args:
        crane_data_list: List of Crane objects with attachments
        db_url: Database connection URL
    """
    print(f"\n{'=' * 100}")
    print(
        f"Starting database write operation for {len(crane_data_list)} cranes"
    )
    print(f"{'=' * 100}\n")

    engine = create_engine(db_url)

    with Session(engine) as session:
        for crane_data in crane_data_list:
            try:
                crane_name = f"{crane_data.manufacturer}_{crane_data.model}"

                # Check if crane already exists
                existing_crane = get_crane_db_model_by_name(
                    session,
                    crane_name,
                )

                if existing_crane:
                    print(f"\nUpdating existing crane: {crane_name}")
                    # Update existing crane data
                    existing_crane.model = crane_data.model
                    existing_crane.manufacturer = crane_data.manufacturer
                    existing_crane.chassis_type = crane_data.chassis_type.value
                    existing_crane.pricebook = crane_data.pricebook
                    existing_crane.resource_code = crane_data.resource_code
                    existing_crane.base_price = crane_data.base_price
                    existing_crane.labor_cost = crane_data.labor_cost
                    existing_crane.max_lifting_capacity = (
                        crane_data.max_lifting_capacity
                    )
                    existing_crane.lc_table_radiuses = (
                        crane_data.lc_table_radiuses
                    )
                    existing_crane.lc_table = crane_data.lc_table

                    crane_db_model = existing_crane
                else:
                    print(f"\nCreating new crane: {crane_name}")
                    # Create new crane
                    crane_db_model = CraneDbModel(
                        model=crane_data.model,
                        manufacturer=crane_data.manufacturer,
                        chassis_type=crane_data.chassis_type.value,
                        pricebook=crane_data.pricebook,
                        resource_code=crane_data.resource_code,
                        base_price=crane_data.base_price,
                        labor_cost=crane_data.labor_cost,
                        max_lifting_capacity=crane_data.max_lifting_capacity,
                        lc_table_radiuses=crane_data.lc_table_radiuses,
                        lc_table=crane_data.lc_table,
                    )
                    session.add(crane_db_model)
                    session.flush()  # Get the ID for the new crane

                # Print crane data being written
                print("  Crane data:")
                print(f"    Model: {crane_data.model}")
                print(f"    Manufacturer: {crane_data.manufacturer}")
                print(f"    Chassis Type: {crane_data.chassis_type.value}")
                print(f"    Pricebook: {crane_data.pricebook}")
                print(f"    Resource Code: {crane_data.resource_code}")
                print(f"    Base Price: {crane_data.base_price}")
                print(f"    Labor Cost: {crane_data.labor_cost}")
                print(
                    f"    Max Lifting Capacity: "
                    f"{crane_data.max_lifting_capacity}"
                )
                print(
                    f"    LC Table Radiuses: {crane_data.lc_table_radiuses}"
                )
                print("    LC Table:")
                pprint(crane_data.lc_table, indent=6, width=80)

                # HANDLE ATTACHMENTS
                # Check and remove existing attachments first
                print("\n  Handling attachments:")
                existing_attachments = (
                    session.query(CraneBinaryAttachmentDbModel)
                    .filter(
                        CraneBinaryAttachmentDbModel.crane_id
                        == crane_db_model.id
                    )
                    .all()
                )

                if existing_attachments:
                    print(
                        f"    Removing {len(existing_attachments)} "
                        "existing attachments:"
                    )
                    for existing_att in existing_attachments:
                        print(f"      - {existing_att.filename}")

                    # Remove existing attachments for this crane
                    session.query(CraneBinaryAttachmentDbModel).filter(
                        CraneBinaryAttachmentDbModel.crane_id
                        == crane_db_model.id
                    ).delete()

                else:
                    print("    No existing attachments to remove")

                if crane_data.attachments:
                    # Add new attachments
                    print(
                        f"    Adding {len(crane_data.attachments)} "
                        "new attachments:"
                    )
                    for attachment in crane_data.attachments:
                        print(
                            f"      + {attachment.filename} "
                            f"({attachment.content_type})"
                        )
                        attachment_db_model = CraneBinaryAttachmentDbModel(
                            crane_id=crane_db_model.id,
                            filename=attachment.filename,
                            content_type=attachment.content_type,
                            data=attachment.data,
                        )
                        session.add(attachment_db_model)
                else:
                    print("    No new attachments to add")

                session.commit()
                print(f"  Successfully processed crane: {crane_name}")

            except Exception as e:
                print(f"Error writing crane to database: {str(e)}")
                session.rollback()
                raise

    print(f"\n{'=' * 100}")
    print(
        f"Database write operation completed successfully for "
        f"{len(crane_data_list)} cranes!"
    )
    print(f"{'=' * 100}\n")
