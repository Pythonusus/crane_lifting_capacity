"""
Script for displaying a summary of all cranes in the database.

This script provides a quick overview of all cranes stored in the database,
including their basic information, pricing, lifting capacity, and attachments.
It's useful for verifying data integrity and getting a quick overview of
the crane inventory.

Features:
    - Displays comprehensive crane information in readable format
    - Shows pricing calculations (base_price + labor_cost = price_per_hour)
    - Lists all attachments for each crane
    - Provides lifting capacity table overview
    - Handles missing data gracefully

Output Format:
    For each crane displays:
    - ID and name (manufacturer_model)
    - Chassis type and maximum lifting capacity
    - Pricing information (base_price, labor_cost, price_per_hour)
    - Lifting capacity table structure (boom lengths and radiuses)
    - List of attachments with filenames and content types

Example Output:
    Found 3 cranes in database:
    ================================================================================
    ID: 1
    Name: Liebherr_LTM1100
    Chassis Type: mobile
    Max Lifting Capacity: 100.0 tons
    Price per Hour: 57000.0
    Boom Lengths: ['10.0', '20.0', '30.0']
    Radiuses: ['3.0', '4.0', '5.0', '6.0', '7.0']
    Attachments:
      - manual.pdf (application/pdf)
      - spec_sheet.pdf (application/pdf)
    --------------------------------------------------------------------------------

Usage:
    # Show summary using default database
    python manage.py show-cranes-summary

    # Show summary with custom database URL
    python manage.py show-cranes-summary --database-url postgresql://user:pass@localhost/cranes

Environment Variables:
    - DATABASE_URL: Default database connection URL

Error Handling:
    - Validates database connection before querying
    - Handles missing environment variables gracefully
    - Provides detailed error messages for database issues
    - Gracefully handles missing attachments or data
"""

import os
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import CraneDbModel


def show_cranes_summary(
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
            print("Attachments:")
            for attachment in crane.attachments:
                print(f"  - {attachment.filename} ({attachment.content_type})")
            print("-" * 80)

    except Exception as e:
        print(f"Error getting crane summary: {str(e)}")
    finally:
        session.close()
