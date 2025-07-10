"""
Script for populating the database from Excel files.

All data in excel files must have the following structure:

A1: "Модель"             B1: model
A2: "Производитель"      B2: manufacturer
A3: "Тип"                B3: chassis_type
A4: "Сборник"            B4: pricebook
A5: "Код ресурса"        B5: resource_code

D1: "Сметная цена без учета оплаты труда"
D2: base_price
D3: "Оплата труда машинистов"
D4: labor_cost
D5: "Максимальная грузоподъемность" G5: max_lifting_capacity

B8: Lifting capacity table starts here
"""

import os
from pprint import pprint
from typing import Dict, List, Optional, Tuple

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.models import CraneDbModel
from app.schemas.cranes import ChassisType, Crane

load_dotenv()

# Configuration
DATA_DIR = os.getenv("DATA_DIR")
DATABASE_URL = os.getenv("DATABASE_URL")


def extract_crane_metadata_from_xlsx(
    df: pd.DataFrame,
) -> Tuple[str, str, ChassisType, str, str, float]:
    """
    Extract crane information from specific cells in the Excel file.
    Returns: (
        model, manufacturer, chassis_type,
        pricebook, resource_code, price_per_hour
    )

    Cell layout:
    A1: "Модель"             B1: model
    A2: "Производитель"      B2: manufacturer
    A3: "Тип шасси"          B3: chassis_type
    A4: "Сборник"            B4: pricebook
    A5: "Код ресурса"        B5: resource_code

    D1: "Сметная цена без учета оплаты труда"
    D2: base_price
    D3: "Оплата труда машинистов"
    D4: labor_cost
    D5: "Максимальная грузоподъемность" G5: max_lifting_capacity

    B8: Lifting capacity table starts here
    """
    print("\nExtracting crane metadata:")
    # Extract and normalize text data by stripping whitespace
    model = str(df.iloc[0, 1]).strip()  # B1
    manufacturer = str(df.iloc[1, 1]).strip()  # B2
    chassis_type = str(df.iloc[2, 1]).strip()  # B3
    pricebook = str(df.iloc[3, 1]).strip()  # B4
    resource_code = str(df.iloc[4, 1]).strip()  # B5

    print(f"Model: {model}")
    print(f"Manufacturer: {manufacturer}")
    print(f"Chassis Type: {chassis_type}")
    print(f"Pricebook: {pricebook}")
    print(f"Resource Code: {resource_code}")

    # Convert numeric values
    base_price = float(df.iloc[1, 3])  # D2
    labor_cost = float(df.iloc[3, 3])  # D4

    print(f"Base Price: {base_price}")
    print(f"Labor Cost: {labor_cost}")

    max_lifting_capacity = float(df.iloc[4, 6])  # G5

    print(f"Max Lifting Capacity: {max_lifting_capacity}")

    return (
        model,
        manufacturer,
        ChassisType(chassis_type),
        pricebook,
        resource_code,
        base_price,
        labor_cost,
        max_lifting_capacity,
    )


def extract_lc_table_from_xlsx(
    df: pd.DataFrame,
) -> Dict[str, Dict[float, float]]:  # Dict[boom_length, Dict[radius, capacity]]
    """
    Parse the lifting capacity table from an Excel DataFrame.

    Table structure:
    - "Вылет, м" is located in cell B8
    - Boom lengths are in the header row starting from C8
    - Radius values are in the first column starting from B9
    - Empty values are marked with '-' or ''

    Args:
        df: pandas DataFrame containing the Excel data

    Returns:
        Dict mapping boom lengths to their radius-capacity pairs:
        {
            "11.5*": {  # boom_length
                3.0: 95.0,  # radius: capacity
                3.5: 86.0,
                4.0: 78.0,
                ...
            },
            "11.5": {
                3.0: 83.0,
                3.5: 80.0,
                ...
            },
            ...
        }
    """
    print("\nExtracting lifting capacity table:")

    # Fixed positions
    TABLE_START_ROW = 7  # B8 in 0-based indexing
    TABLE_START_COL = 1  # B column in 0-based indexing

    # Get boom lengths from the header row (C8 onwards)
    boom_lengths = []
    for col in range(TABLE_START_COL + 1, df.shape[1]):
        value = df.iloc[TABLE_START_ROW, col]
        if pd.isna(value) or value == '':
            break
        try:
            # Only strip whitespace, preserve all other characters
            value_str = str(value).strip()
            boom_lengths.append(value_str)
        except (ValueError, TypeError):
            continue

    print(f"Found boom lengths: {boom_lengths}")

    # Initialize the lifting capacity table dictionary
    # Structure: Dict[boom_length, Dict[radius, capacity]]
    lc_table: Dict[str, Dict[float, float]] = {
        boom_length: {} for boom_length in boom_lengths
    }

    # Process each row starting from B9
    row_idx = TABLE_START_ROW + 1
    while row_idx < df.shape[0]:
        try:
            # Get radius value from column B
            radius = df.iloc[row_idx, TABLE_START_COL]
            if pd.isna(radius) or radius == '':
                break
            radius = float(radius)

            # Process each boom length column
            for col_idx, boom_length in enumerate(boom_lengths):
                # Starting from column C
                capacity = df.iloc[row_idx, TABLE_START_COL + 1 + col_idx]

                # Skip empty or invalid values
                if pd.isna(capacity) or capacity in ['-', '', 0]:
                    continue

                try:
                    capacity = float(capacity)
                    lc_table[boom_length][radius] = capacity
                except (ValueError, TypeError):
                    continue

            row_idx += 1
        except Exception as e:
            print(f"Error processing row {row_idx + 1}: {str(e)}")
            break

    # Pretty print the result
    print("\nLifting capacity table:")
    pprint(lc_table, width=40, sort_dicts=False)

    return lc_table


def extract_data_from_excel_files(data_dir: str) -> List[Crane]:
    """
    Process all Excel files in the data directory and its subdirectories
    and return list of crane data.

    Args:
        data_dir: Directory containing Excel files

    Returns:
        List of Cranes Pydantic models
    """
    crane_data_list = []

    # Walk through all files in data directory
    for root, _, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.xlsx'):
                file_path = os.path.join(root, file)
                try:
                    # Read the Excel file once for both operations
                    df = pd.read_excel(
                        file_path, engine='openpyxl', header=None
                    )

                    print(f"Processing {file_path}")

                    # Parse crane info and lifting capacity table
                    (
                        model,
                        manufacturer,
                        chassis_type,
                        pricebook,
                        resource_code,
                        base_price,
                        labor_cost,
                        max_lifting_capacity,
                    ) = extract_crane_metadata_from_xlsx(df)

                    lc_table = extract_lc_table_from_xlsx(df)

                    # Create Pydantic model for validation
                    crane_data = Crane(
                        model=model,
                        manufacturer=manufacturer,
                        chassis_type=chassis_type,
                        pricebook=pricebook,
                        resource_code=resource_code,
                        base_price=base_price,
                        labor_cost=labor_cost,
                        max_lifting_capacity=max_lifting_capacity,
                        lc_table=lc_table,
                    )

                    crane_data_list.append(crane_data)
                    print(f"Successfully processed {file}\n")

                except Exception as e:
                    print(f"Error processing {file}: {str(e)}\n")

    return crane_data_list


def write_cranes_to_db(crane_data_list: List[Crane], db_url: str) -> None:
    """
    Write crane data to database, handling updates for existing entries.

    Args:
        crane_data_list: List of Cranes Pydantic models
        db_url: Database connection URL
    """
    engine = create_engine(db_url)

    with Session(engine) as session:
        for crane_data in crane_data_list:
            try:
                # Create SQLAlchemy model
                crane_db = CraneDbModel(
                    model=crane_data.model,
                    manufacturer=crane_data.manufacturer,
                    chassis_type=crane_data.chassis_type,
                    pricebook=crane_data.pricebook,
                    resource_code=crane_data.resource_code,
                    base_price=crane_data.base_price,
                    labor_cost=crane_data.labor_cost,
                    max_lifting_capacity=crane_data.max_lifting_capacity,
                    lc_table=crane_data.lc_table,
                )

                # Check if crane already exists
                existing = (
                    session.query(CraneDbModel)
                    .filter_by(model=crane_data.model)
                    .first()
                )

                if existing:
                    print(
                        f"Updating existing crane \
                        {crane_data.manufacturer} \
                        {crane_data.model}"
                    )
                    existing.manufacturer = crane_data.manufacturer
                    existing.chassis_type = crane_data.chassis_type
                    existing.lc_table = crane_data.lc_table
                    existing.base_price = crane_data.base_price
                    existing.labor_cost = crane_data.labor_cost
                    existing.pricebook = crane_data.pricebook
                    existing.resource_code = crane_data.resource_code
                else:
                    print(
                        f"Adding new crane \
                        {crane_data.manufacturer} \
                        {crane_data.model}"
                    )
                    session.add(crane_db)

                session.commit()
                print(
                    f"Successfully saved \
                    {crane_data.manufacturer} \
                    {crane_data.model}"
                )

            except Exception as e:
                print(f"Error writing crane to database: {str(e)}")
                session.rollback()


def populate_db_from_excel(
    data_dir: Optional[str] = None, database_url: Optional[str] = None
) -> None:
    """
    Main entry point for populating the database from Excel files.
    Uses command line arguments if provided,
    otherwise falls back to environment variables.

    Args:
        data_dir: Directory containing Excel files (optional)
        database_url: Database URL (optional)
    """

    # Use provided args if available, otherwise fall back to env vars
    final_data_dir = data_dir or os.getenv("DATA_DIR")
    final_database_url = database_url or os.getenv("DATABASE_URL")

    if not all([final_data_dir, final_database_url]):
        print(
            "Error: DATA_DIR and DATABASE_URL must be provided either \
            via command line or in .env file"
        )
        return

    print(f"Using data directory: {final_data_dir}")
    print(f"Using database URL: {final_database_url}")

    cranes_data_list = extract_data_from_excel_files(final_data_dir)
    write_cranes_to_db(cranes_data_list, final_database_url)


if __name__ == "__main__":
    # Allow running directly for testing
    populate_db_from_excel()
