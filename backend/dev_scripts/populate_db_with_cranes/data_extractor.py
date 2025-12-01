"""
Module for extracting crane data.

This module coordinates the extraction of crane data from Excel files
and their associated attachments.
"""

from pathlib import Path
from typing import Dict, List, Union

import pandas as pd

from app.schemas.cranes import Crane, LcTable

from .parse_attachments import parse_crane_attachments
from .parse_excel_data import (
    extract_crane_metadata_from_xlsx,
    extract_lc_table_from_xlsx,
)


def extract_cranes_data(data_dir: Union[str, Path]) -> List[Crane]:
    """
    Process all Excel files in the data directory and its subdirectories
    and return list of crane data with their attachments.

    Structure:
    - First sheet contains crane metadata
    - Following sheets contain LC tables (one table per sheet)

    Args:
        data_dir: Directory containing Excel files or with subdirectories
                 containing Excel files (accepts both str and Path objects)

    Returns:
        List of Crane objects with attachments
    """
    crane_data_list = []

    # Convert to Path object for consistent handling
    data_path = Path(data_dir)

    # Walk through all Excel files in the directory tree
    for file_path in data_path.rglob("*.xlsx"):
        try:
            # Open Excel file once
            excel_file = pd.ExcelFile(file_path, engine="openpyxl")

            # Read the first sheet (metadata sheet)
            metadata_df = pd.read_excel(excel_file, sheet_name=0, header=None)

            # Parse crane metadata from first sheet
            (
                model,
                manufacturer,
                country,
                chassis_type,
                max_lifting_capacity,
                description,
                manufacturer_url,
                crane_url,
                pricebook,
                resource_code,
                base_price,
                labor_cost,
                dwg_url,
            ) = extract_crane_metadata_from_xlsx(metadata_df)

            # Process each sheet after the first one as LC tables
            lc_tables: Dict[str, LcTable] = {}
            for sheet_name in excel_file.sheet_names[1:]:
                try:
                    lc_df = pd.read_excel(
                        excel_file, sheet_name=sheet_name, header=None
                    )
                    table_name, lc_table = extract_lc_table_from_xlsx(lc_df)
                    lc_tables[table_name] = lc_table
                except Exception as e:
                    print(
                        f"Warning: Could not parse LC table from sheet "
                        f"'{sheet_name}' in {file_path.name}: {e}"
                    )
                    continue

            print(f"Processed {manufacturer} {model} metadata")
            # Find all attachments for this crane in the directory
            # containing the Excel file.
            crane_dir = file_path.parent
            print(f"Searching for attachments in {crane_dir}")
            attachments = parse_crane_attachments(str(crane_dir))

            print(f"Processed {manufacturer} {model} attachments")
            # Create Pydantic model for validation at the very end
            crane_data = Crane(
                model=model,
                manufacturer=manufacturer,
                country=country,
                chassis_type=chassis_type,
                description=description,
                manufacturer_url=manufacturer_url,
                crane_url=crane_url,
                pricebook=pricebook,
                resource_code=resource_code,
                base_price=base_price,
                labor_cost=labor_cost,
                max_lifting_capacity=max_lifting_capacity,
                dwg_url=dwg_url,
                lc_tables=lc_tables,
                attachments=attachments,
            )
            crane_data_list.append(crane_data)

        except Exception as e:
            print(f"Error processing {file_path.name}: {e}\n")
            import traceback

            traceback.print_exc()

    return crane_data_list
