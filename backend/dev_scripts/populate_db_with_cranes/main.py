"""
Script for populating the database from Excel files and attachments.

This script processes Excel files containing crane data and associated
attachments, then imports them into the database. It handles both new
crane creation and updates to existing cranes.

Data Format Requirements:
    Excel files must follow this structure:

    First Sheet (Metadata Sheet):
        Basic information:
        - B4: "Модель"                         C4: model
        - B5: "Производитель"                  C5: manufacturer
        - B6: "Страна"                         C6: country
        - B7: "Тип шасси"                      C7: chassis_type
        - B8: "Макс гп"                        C8: max_lifting_capacity
        - B9: "Описание"                       C9: description (optional)
        - B10: "Ссылка на производителя"       C10: manufacturer_url (optional)
        - B11: "Ссылка на кран"                C11: crane_url (optional)

        Economic section:
        - D4: "Сборник"                        E4: pricebook
        - D5: "Код ресурса"                    E5: resource_code
        - D6: "Базовая цена"                   E6: base_price
        - D7: "Зарплата машиниста"             E7: labor_cost

        Attachments:
        - F4: "Ссылка на чертеж"               G4: dwg_url (optional)

    Subsequent Sheets (LC Tables):
        Each sheet after the first contains one lifting capacity table:
        - B1: table name
        - B4: "Вылет, м" (header)
        - C4 onwards: boom lengths (header row)
        - B5 onwards: radius values (first column)
        - C5 onwards: capacity values at intersection of radius and boom length
        - Empty values are marked with '-' or 0

    Structure:
        - First sheet: Contains all crane metadata
        - Sheet 2, 3, ...: Each contains one lifting capacity table

    Attachments should be stored in the same directory as the Excel file.

Features:
    - Processes multiple Excel files in subdirectories
    - Handles both new crane creation and existing crane updates
    - Processes binary attachments (PDFs, DWGs, etc.)
    - Validates data using Pydantic schemas
    - Provides detailed logging of import process
    - Handles errors gracefully with rollback on failure
    - Supports multiple lifting capacity tables per crane

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
    - CRANES_DIR: Default directory containing crane data files
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

from app.settings import CRANES_DIR, DATABASE_URL

from .data_extractor import extract_cranes_data
from .db_operations import write_cranes_to_db


def populate_db(
    cranes_dir: Optional[Union[str, Path]] = None,
    database_url: Optional[str] = None,
) -> None:
    """
    Main entry point for populating the database with cranes data.
    Uses command line arguments if provided,
    otherwise falls back to app settings.

    Args:
        cranes_dir: Directory containing cranes data files (optional)
        database_url: Database URL (optional)
    """

    # Use provided args if available, otherwise fall back to settings
    final_cranes_dir = cranes_dir or CRANES_DIR
    final_database_url = database_url or DATABASE_URL

    if not all([final_cranes_dir, final_database_url]):
        print(
            "Error: CRANES_DIR and DATABASE_URL must be provided either "
            "via command line or in settings"
        )
        return

    print("Starting database population...")
    print(f"Using data directory: {final_cranes_dir}")
    print(f"Using database URL: {final_database_url}")
    print("\n")
    print("Extracting cranes data...")

    cranes_data_list = extract_cranes_data(final_cranes_dir)

    print("Successfully extracted cranes data")

    write_cranes_to_db(cranes_data_list, final_database_url)


if __name__ == "__main__":
    # Allow running directly for testing
    populate_db()
