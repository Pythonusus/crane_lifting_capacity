"""
Script for dumping crane data from database to JSON format.

This script exports all crane data from the database to individual JSON files.
Each crane is saved as a separate file named {manufacturer}_{model}.json.

Features:
    - Exports complete crane data including lifting capacity tables
    - Handles attachments as metadata only (filename, content_type, size)
    - Creates organized output directory structure
    - Provides detailed logging of export process
    - Supports custom database URLs and output directories

Output Format:
    Each JSON file contains:
    - Basic crane information (model, manufacturer, chassis_type, etc.)
    - Pricing information (base_price, labor_cost, price_per_hour)
    - Lifting capacity data (max_lifting_capacity, lc_table, lc_table_radiuses)
    - Attachment metadata (filename, content_type, data_size_bytes)

Example Output:
    {
      "id": 1,
      "model": "LTM1100",
      "manufacturer": "Liebherr",
      "chassis_type": "mobile",
      "base_price": 45000.0,
      "labor_cost": 12000.0,
      "max_lifting_capacity": 100.0,
      "lc_table": {"10.0": {"3.0": 80.0, "4.0": 65.0}},
      "attachments": [
        {
          "filename": "manual.pdf",
          "content_type": "application/pdf",
          "data_size_bytes": 2048576
        }
      ]
    }

Usage:
    # Export to default directory
    python manage.py dump-cranes

    # Export to custom directory
    python manage.py dump-cranes --output-dir /path/to/output

    # Use custom database URL
    python manage.py dump-cranes --database-url
        postgresql://user:pass@localhost/cranes

Environment Variables:
    - DATABASE_URL: Default database connection URL

Error Handling:
    - Validates database connection before export
    - Handles missing environment variables gracefully
    - Provides detailed error messages for database issues
    - Creates output directories automatically
"""

import json
from pathlib import Path
from typing import Optional, Union

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import CraneBinaryAttachmentDbModel, CraneDbModel
from app.schemas.cranes import Crane
from app.settings import DATABASE_URL


def dump_cranes_to_json(
    database_url: Optional[str] = None,
    output_dir: Optional[Union[str, Path]] = None,
) -> None:
    """
    Dump all cranes from database to separate JSON files.
    Attachments are dumped as metadata only (without binary data).

    Args:
        database_url: Database URL (if not provided, will use DATABASE_URL
                      from settings)
        output_dir: Output dir path (default is 'cranes_dump' in script dir)
    """

    print(f"\n{'=' * 100}")
    print("Dumping cranes data to JSON files")
    print(f"{'=' * 100}\n")

    # Use provided database URL or fall back to settings
    final_database_url = database_url or DATABASE_URL
    if not final_database_url:
        print(
            "Error: DATABASE_URL must be provided via argument or in settings"
        )
        return

    # Use provided output directory or default to script directory
    if output_dir is None:
        script_dir = Path(__file__).resolve().parent
        final_output_dir = script_dir / "cranes_dump"
    else:
        final_output_dir = Path(output_dir)

    print(f"Using database URL: {final_database_url}")
    print(f"Output directory: {final_output_dir}")

    # Create output directory if it doesn't exist
    final_output_dir.mkdir(parents=True, exist_ok=True)

    # Create database engine and session
    engine = create_engine(final_database_url)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        # Get all cranes with their attachments
        cranes = session.query(CraneDbModel).all()
        print(f"Found {len(cranes)} cranes in database")

        # Convert to JSON files using Pydantic schema
        dumped_count = 0
        total_attachments = 0

        for crane in cranes:
            # Get attachments for this crane
            attachments = (
                session.query(CraneBinaryAttachmentDbModel)
                .filter(CraneBinaryAttachmentDbModel.crane_id == crane.id)
                .all()
            )

            # Create attachment metadata (without binary data)
            attachment_metadata = []
            for attachment in attachments:
                attachment_metadata.append(
                    {
                        "filename": attachment.filename,
                        "content_type": attachment.content_type,
                        "data_size_bytes": (
                            len(attachment.data) if attachment.data else 0
                        ),
                    }
                )

            # Use Pydantic schema to convert and validate
            crane_schema = Crane.model_validate(crane)

            # Create a custom dump with attachment metadata
            crane_dump = crane_schema.model_dump()

            # Replace attachments with metadata only
            crane_dump["attachments"] = attachment_metadata

            # Create filename: manufacturer_model.json
            filename = f"{crane.manufacturer}_{crane.model}.json"

            file_path = final_output_dir / filename

            # Write individual crane to JSON file
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(crane_dump, f, indent=2, ensure_ascii=False)

            dumped_count += 1
            total_attachments += len(attachments)
            print(f"Dumped: {filename} ({len(attachments)} attachments)")

        print(
            f"\nSuccessfully dumped {dumped_count} cranes "
            f"with {total_attachments} total attachments to {final_output_dir}"
        )
        print(f"{'=' * 100}\n")

    except Exception as e:
        print(f"Error dumping cranes data: {str(e)}")
    finally:
        session.close()


if __name__ == "__main__":
    # Allow running directly for testing
    dump_cranes_to_json()
