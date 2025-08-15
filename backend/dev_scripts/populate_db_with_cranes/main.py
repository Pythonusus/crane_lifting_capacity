"""
Script for populating the database from Excel files and attachments.

This script processes Excel files containing crane data and associated
attachments, then imports them into the database. It handles both new
crane creation and updates to existing cranes.

Data Format Requirements:
    Excel files must follow this structure:
    - A1: "Модель"             B1: model
    - A2: "Производитель"      B2: manufacturer
    - A3: "Тип шасси"          B3: chassis_type
    - A4: "Сборник"            B4: pricebook
    - A5: "Код ресурса"        B5: resource_code

    - D1: "Сметная цена без учета оплаты труда"
    - D2: base_price
    - D3: "Оплата труда машинистов"
    - D4: labor_cost
    - D5: "Максимальная грузоподъемность"
    - G5: max_lifting_capacity
    - B8: "Вылет, м" (LC table starts here)
    - B9+: radiuses (until empty cell)
    - C+8: boom lengths (until empty cell)

    Empty values in LC table are marked with '-' or 0

    Attachments should be stored in
        {ATTACHMENTS_DIR}/attachments/{chassis_type}/crane_data_directory

Features:
    - Processes multiple Excel files in subdirectories
    - Handles both new crane creation and existing crane updates
    - Processes binary attachments (PDFs, DWGs, etc.)
    - Validates data using Pydantic schemas
    - Provides detailed logging of import process
    - Handles errors gracefully with rollback on failure

Database Operations:
    - Creates new cranes with all data and attachments
    - Updates existing cranes with new data
    - Replaces all attachments for existing cranes
    - Maintains data integrity with transaction rollback on errors

Usage:
    # Import from default data directory
    python manage.py populate-db

    # Import from specific directory
    python manage.py populate-db --data-dir /path/to/data/dir

    # Import with custom database URL
    python manage.py populate-db --database-url postgresql://user:pass@localhost/cranes

Environment Variables:
    - ATTACHMENTS_DIR: Default directory containing
        {ATTACHMENTS_DIR}/attachments/{chassis_type}/crane_data_directory
    - DATABASE_URL: Default database connection URL

Error Handling:
    - Validates Excel file structure before processing
    - Handles missing or corrupted Excel files gracefully
    - Provides detailed error messages for data validation issues
    - Rolls back database transactions on errors
    - Logs all operations for debugging
"""

from pathlib import Path
from typing import Optional, Union

from app.settings import ATTACHMENTS_DIR, DATABASE_URL

from .data_extractor import extract_cranes_data
from .db_operations import write_cranes_to_db


def populate_db(
    data_dir: Optional[Union[str, Path]] = None,
    database_url: Optional[str] = None,
) -> None:
    """
    Main entry point for populating the database with cranes data.
    Uses command line arguments if provided,
    otherwise falls back to app settings.

    Args:
        data_dir: Directory containing cranes data files (optional)
        database_url: Database URL (optional)
    """

    # Use provided args if available, otherwise fall back to settings
    final_data_dir = data_dir or ATTACHMENTS_DIR
    final_database_url = database_url or DATABASE_URL

    if not all([final_data_dir, final_database_url]):
        print(
            "Error: ATTACHMENTS_DIR and DATABASE_URL must be provided either "
            "via command line or in settings"
        )
        return

    print("Starting database population...")
    print(f"Using data directory: {final_data_dir}")
    print(f"Using database URL: {final_database_url}")
    print("\n")
    print("Extracting cranes data...")

    cranes_data_list = extract_cranes_data(final_data_dir)

    print("Successfully extracted cranes data")

    write_cranes_to_db(cranes_data_list, final_database_url)


if __name__ == "__main__":
    # Allow running directly for testing
    populate_db()
