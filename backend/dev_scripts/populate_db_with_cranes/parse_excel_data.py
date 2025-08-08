"""
Module for parsing Excel files containing crane data.

This module handles the extraction of crane metadata and lifting capacity tables
from Excel files with a specific structure.
"""

from typing import Dict, List, Tuple

import pandas as pd

from app.schemas.cranes import ChassisType


def extract_crane_metadata_from_xlsx(
    df: pd.DataFrame,
) -> Tuple[str, str, ChassisType, str, str, float, float, float, List[str]]:
    """
    Extract crane information from specific cells in the Excel file.
    Returns: (
        model, manufacturer, chassis_type,
        pricebook, resource_code, base_price, labor_cost,
        max_lifting_capacity, lc_table_radiuses
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
    D5: "Максимальная грузоподъемность"
    G5: max_lifting_capacity
    """
    # Extract and normalize text data by stripping whitespace
    model = str(df.iloc[0, 1]).strip()  # B1
    manufacturer = str(df.iloc[1, 1]).strip()  # B2
    chassis_type = str(df.iloc[2, 1]).strip()  # B3
    pricebook = str(df.iloc[3, 1]).strip()  # B4
    resource_code = str(df.iloc[4, 1]).strip()  # B5

    # Convert numeric values
    base_price = float(df.iloc[1, 3])  # D2
    labor_cost = float(df.iloc[3, 3])  # D4
    max_lifting_capacity = float(df.iloc[4, 6])  # G5

    # Parse radiuses starting from B9 until empty cell
    lc_table_radiuses = []
    row_idx = 8  # B9 in 0-based indexing
    while row_idx < df.shape[0]:
        radius_value = df.iloc[row_idx, 1]  # Column B
        if pd.isna(radius_value) or radius_value == '':
            break
        try:
            radius = str(radius_value).strip()
            lc_table_radiuses.append(radius)
        except (ValueError, TypeError):
            break
        row_idx += 1

    return (
        model,
        manufacturer,
        ChassisType(chassis_type),
        pricebook,
        resource_code,
        base_price,
        labor_cost,
        max_lifting_capacity,
        lc_table_radiuses,
    )


def extract_lc_table_from_xlsx(
    df: pd.DataFrame,
) -> Dict[str, Dict[str, float]]:  # Dict[boom_length, Dict[radius, capacity]]
    """
    Parse the lifting capacity table from an Excel DataFrame.

    Table structure:
    - "Вылет, м" is located in cell B8
    - Boom lengths are in the header row starting from C8
    - Radius values are in the first column starting from B9
    - Empty values are marked with '-' or 0

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

    # Fixed positions
    TABLE_START_ROW = 7  # 8th row in 0-based indexing
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

    # Initialize the lifting capacity table dictionary
    # Structure: Dict[boom_length, Dict[radius, capacity]]
    lc_table: Dict[str, Dict[str, float]] = {
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
            radius = str(radius).strip()

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
        except Exception:
            break

    return lc_table
