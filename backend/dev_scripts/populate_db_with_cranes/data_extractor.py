"""
Module for extracting crane data.

This module coordinates the extraction of crane data from Excel files
and their associated attachments.
"""

from pathlib import Path
from typing import List, Union

import pandas as pd

from app.schemas.cranes import Crane

from .parse_attachments import find_crane_attachments
from .parse_excel_data import (
    extract_crane_metadata_from_xlsx,
    extract_lc_table_from_xlsx,
)


def extract_cranes_data(data_dir: Union[str, Path]) -> List[Crane]:
    """
    Process all Excel files in the data directory and its subdirectories
    and return list of crane data with their attachments.

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
    for file_path in data_path.rglob('*.xlsx'):
        try:
            # Read the Excel file once for both operations
            df = pd.read_excel(
                file_path, engine='openpyxl', header=None
            )
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
                lc_table_radiuses,
            ) = extract_crane_metadata_from_xlsx(df)

            lc_table = extract_lc_table_from_xlsx(df)

            print(f"Processed {manufacturer} {model} metadata")
            # Find all attachments for this crane in the directory
            # containing the Excel file.
            crane_dir = file_path.parent
            print(f"Searching for attachments in {crane_dir}")
            attachments = find_crane_attachments(str(crane_dir))

            print(f"Processed {manufacturer} {model} attachments")
            # Create Pydantic model for validation at the very end
            crane_data = Crane(
                model=model,
                manufacturer=manufacturer,
                chassis_type=chassis_type,
                pricebook=pricebook,
                resource_code=resource_code,
                base_price=base_price,
                labor_cost=labor_cost,
                max_lifting_capacity=max_lifting_capacity,
                lc_table_radiuses=lc_table_radiuses,
                lc_table=lc_table,
                attachments=attachments,
            )
            crane_data_list.append(crane_data)

        except Exception:
            print(f"Error processing {file_path.name}\n")

    return crane_data_list
