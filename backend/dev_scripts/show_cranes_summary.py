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
    - Provides lifting capacity table overview (supports multiple tables)
    - Handles missing data gracefully

Output Format:
    For each crane displays:
    - ID and name (manufacturer_model)
    - Model, manufacturer, country, chassis type
    - Maximum lifting capacity
    - Pricing information (base_price, labor_cost, price_per_hour)
    - Economic information (pricebook, resource_code)
    - URLs (manufacturer_url, crane_url, dwg_url)
    - Description
    - Lifting capacity tables (multiple tables with boom lengths and radiuses)
    - List of attachments with filenames and content types

Example Output:
    Found 3 cranes in database:
    ============================================================================
    ID: 1
    Name: Liebherr_LTM1100
    Model: LTM1100
    Manufacturer: Liebherr
    Country: Germany
    Chassis Type: Спецшасси автомобильного типа
    Max Lifting Capacity: 100.0 tons
    Description: Mobile crane with advanced features
    Manufacturer URL: https://www.liebherr.com
    Crane URL: https://www.liebherr.com/cranes/ltm1100
    Pricebook: Pricebook 2024
    Resource Code: CRANE-001
    Base Price: 50000.0
    Labor Cost: 7000.0
    Price per Hour: 57000.0
    DWG URL: https://example.com/dwg/ltm1100.dwg
    LC Tables:
      Table: main
        Boom Lengths: ['10.0', '20.0', '30.0']
        Radiuses: ['3.0', '4.0', '5.0', '6.0', '7.0']
    Attachments:
      - manual.pdf (application/pdf)
      - spec_sheet.pdf (application/pdf)
    --------------------------------------------------------------------------

Usage:
    # Show summary using default database
    python manage.py show-cranes-summary

    # Show summary with custom database URL
    python manage.py show-cranes-summary --database-url
                     postgresql://user:pass@localhost/cranes

Environment Variables:
    - DATABASE_URL: Default database connection URL

Error Handling:
    - Validates database connection before querying
    - Handles missing environment variables gracefully
    - Provides detailed error messages for database issues
    - Gracefully handles missing attachments or data
"""

from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import CraneDbModel
from app.settings import DATABASE_URL


def show_cranes_summary(
    database_url: Optional[str] = None,
) -> None:
    """
    Print a summary of all cranes in the database.

    Args:
        database_url: Database URL (if not provided, will use DATABASE_URL
                      from settings)
    """
    # Use provided database URL or fall back to settings
    final_database_url = database_url or DATABASE_URL
    if not final_database_url:
        print(
            "Error: DATABASE_URL must be provided via argument or in settings"
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
            print(f"Model: {crane.model}")
            print(f"Manufacturer: {crane.manufacturer}")
            print(f"Country: {crane.country}")
            print(f"Chassis Type: {crane.chassis_type}")
            print(f"Max Lifting Capacity: {crane.max_lifting_capacity} tons")
            print(f"Description: {crane.description}")
            print(f"Manufacturer URL: {crane.manufacturer_url}")
            print(f"Crane URL: {crane.crane_url}")
            print(f"Pricebook: {crane.pricebook}")
            print(f"Resource Code: {crane.resource_code}")
            print(f"Base Price: {crane.base_price}")
            print(f"Labor Cost: {crane.labor_cost}")
            print(f"Price per Hour: {crane.price_per_hour}")
            print(f"DWG URL: {crane.dwg_url}")

            # Display LC tables (can be multiple tables per crane)
            print("LC Tables:")
            if crane.lc_tables:
                for table_name, lc_table_data in crane.lc_tables.items():
                    print(f"  Table: {table_name}")
                    # Extract boom lengths from table keys
                    boom_lengths = list(lc_table_data.get("table", {}).keys())
                    radiuses = lc_table_data.get("radiuses", [])
                    print(f"    Boom Lengths: {boom_lengths}")
                    print(f"    Radiuses: {radiuses}")
            else:
                print("  No LC tables available")

            print("Attachments:")
            if crane.attachments:
                for attachment in crane.attachments:
                    print(
                        f"  - {attachment.filename} ({attachment.content_type})"
                    )
            else:
                print("  No attachments")

            print("-" * 80)

    except Exception as e:
        print(f"Error getting crane summary: {str(e)}")
    finally:
        session.close()


if __name__ == "__main__":
    # Allow running directly for testing
    show_cranes_summary()
