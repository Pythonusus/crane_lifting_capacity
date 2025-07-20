"""
Script for dumping crane data from database to JSON format.
"""

import json
import os
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import CraneDbModel
from app.schemas.cranes import Crane

load_dotenv()


def dump_cranes_to_json(
    database_url: Optional[str] = None,
    output_dir: Optional[str] = None,
) -> None:
    """
    Dump all cranes from database to separate JSON files.

    Args:
        database_url: (if not provided, will use DATABASE_URL from .env)
        output_dir: Output dir path (default is 'cranes_dump' in script dir)
    """
    # Use provided database URL or fall back to environment variable
    final_database_url = database_url or os.getenv("DATABASE_URL")
    if not final_database_url:
        print(
            "Error: DATABASE_URL must be provided via argument or in .env file"
        )
        return

    # Use provided output directory or default to script directory
    if output_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        final_output_dir = os.path.join(script_dir, "cranes_dump")
    else:
        final_output_dir = output_dir

    print(f"Using database URL: {final_database_url}")
    print(f"Output directory: {final_output_dir}")

    # Create output directory if it doesn't exist
    os.makedirs(final_output_dir, exist_ok=True)

    # Create database engine and session
    engine = create_engine(final_database_url)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        # Get all cranes
        cranes = session.query(CraneDbModel).all()
        print(f"Found {len(cranes)} cranes in database")

        # Convert to JSON files using Pydantic schema
        dumped_count = 0
        for crane in cranes:
            # Use Pydantic schema to convert and validate
            crane_schema = Crane.model_validate(crane)

            # Create filename: manufacturer_model.json
            filename = f"{crane.manufacturer}_{crane.model}.json"

            file_path = os.path.join(final_output_dir, filename)

            # Write individual crane to JSON file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(
                    crane_schema.model_dump(), f, indent=2, ensure_ascii=False
                )

            dumped_count += 1
            print(f"Dumped: {filename}")

        print(
            f"Successfully dumped {dumped_count} \
            cranes to {final_output_dir}"
        )

        # Print summary
        print("\nCrane summary:")
        for crane in cranes:
            print(f"-{crane.manufacturer} {crane.model} (ID: {crane.id})")

    except Exception as e:
        print(f"Error dumping cranes data: {str(e)}")
    finally:
        session.close()


def dump_cranes_summary(
    database_url: Optional[str] = None,
) -> None:
    """
    Print a summary of all cranes in the database.

    Args:
        database_url: if not provided, will use DATABASE_URL from .env
    """
    # Use provided database URL or fall back to environment variable
    final_database_url = database_url or os.getenv("DATABASE_URL")
    if not final_database_url:
        print(
            "Error: DATABASE_URL must be provided via argument or in .env file"
        )
        return

    print(f"Using database URL: {final_database_url}")

    # Create database engine and session
    engine = create_engine(final_database_url)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        # Get all cranes
        cranes = session.query(CraneDbModel).all()
        print(f"\nFound {len(cranes)} cranes in database:")
        print("=" * 80)

        for crane in cranes:
            print(f"ID: {crane.id}")
            print(f"Name: {crane.name}")
            print(f"Chassis Type: {crane.chassis_type}")
            print(f"Max Lifting Capacity: {crane.max_lifting_capacity} tons")
            print(f"Price per Hour: {crane.price_per_hour}")
            print(f"Boom Lengths: {crane.lc_table_boom_lengths}")
            print(f"Radiuses: {crane.lc_table_radiuses}")
            print("-" * 80)

    except Exception as e:
        print(f"Error getting crane summary: {str(e)}")
    finally:
        session.close()


if __name__ == "__main__":
    # Allow running directly for testing
    dump_cranes_to_json()
