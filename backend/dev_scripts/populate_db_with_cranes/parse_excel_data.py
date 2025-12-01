"""
Module for parsing Excel files containing crane data.

This module handles the extraction of crane metadata and lifting capacity tables
from Excel files with a specific structure.
"""

from typing import Dict, List, Optional, Tuple

import pandas as pd

from app.schemas.cranes import ChassisType, LcTable

# Fixed positions of the lifting capacity table in the Excel file
TABLE_START_ROW = 3  # 4th row in 0-based indexing
TABLE_START_COL = 1  # B column in 0-based indexing


def extract_crane_metadata_from_xlsx(
    df: pd.DataFrame,
) -> Tuple[
    str,  # model
    str,  # manufacturer
    str,  # country
    ChassisType,  # chassis_type
    float,  # max_lifting_capacity
    Optional[str],  # description
    Optional[str],  # manufacturer_url
    Optional[str],  # crane_url
    str,  # pricebook
    str,  # resource_code
    float,  # base_price
    float,  # labor_cost
    Optional[str],  # dwg_url
]:
    """
    Extract crane information from specific cells in the Excel file.

    Returns: (
        model, manufacturer, country, chassis_type, max_lifting_capacity,
        description, manufacturer_url, crane_url,
        pricebook, resource_code, base_price, labor_cost, dwg_url
    )

    Cell layout

    Basic information:
    --------------------------------------------------------------
    B4: "Модель"                              C4: model
    B5: "Производитель"                       C5: manufacturer
    B6: "Страна"                              C6: country
    B7: "Тип шасси"                           C7: chassis_type
    B8: "Макс гп"                             C8: max_lifting_capacity
    B9: "Описание"                            C9: description
    B10: "Ссылка на производителя"            C10: manufacturer_url
    B11: "Ссылка на кран"                     C11: crane_url

    Economic section:
    --------------------------------------------------------------
    D4: "Сборник"                             E4: pricebook
    D5: "Код ресурса"                         E5: resource_code
    D6: "Базовая цена"                        E6: base_price
    D7: "Зарплата машиниста"                  E7: labor_cost

    Attachments:
    --------------------------------------------------------------
    F4: "Ссылка на чертеж"                    G4: dwg_url
    """
    # Basic information
    model = str(df.iloc[3, 2]).strip()  # C4
    manufacturer = str(df.iloc[4, 2]).strip()  # C5
    country = str(df.iloc[5, 2]).strip()  # C6
    chassis_type = str(df.iloc[6, 2]).strip()  # C7
    max_lifting_capacity = float(df.iloc[7, 2])  # C8

    description = df.iloc[8, 2]  # C9
    if pd.isna(description) or description == "":
        description = None
    else:
        description = str(description).strip()

    manufacturer_url = df.iloc[9, 2]  # C10
    if pd.isna(manufacturer_url) or manufacturer_url == "":
        manufacturer_url = None
    else:
        manufacturer_url = str(manufacturer_url).strip()

    crane_url = df.iloc[10, 2]  # C11
    if pd.isna(crane_url) or crane_url == "":
        crane_url = None
    else:
        crane_url = str(crane_url).strip()

    # Economic section
    pricebook = str(df.iloc[3, 4]).strip()  # E4
    resource_code = str(df.iloc[4, 4]).strip()  # E5
    base_price = float(df.iloc[5, 4])  # E6
    labor_cost = float(df.iloc[6, 4])  # E7

    # Attachments
    # Check if column G (index 6) exists before accessing
    if df.shape[1] > 6:
        dwg_url = df.iloc[3, 6]  # G4
        if pd.isna(dwg_url) or dwg_url == "":
            dwg_url = None
        else:
            dwg_url = str(dwg_url).strip()
    else:
        dwg_url = None

    return (
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
    )


def extract_lc_table_radiuses_from_xlsx(df: pd.DataFrame) -> List[str]:
    """
    Extract the radiuses from the lifting capacity table.

    Args:
        df: pandas DataFrame containing the Excel data

    Returns:
        List of radiuses
    """
    radiuses = []
    for row in range(TABLE_START_ROW + 1, df.shape[0]):
        radius_value = df.iloc[row, TABLE_START_COL]
        if pd.isna(radius_value) or radius_value == "":
            break
        try:
            radius = str(radius_value).strip()
            radiuses.append(radius)
        except (ValueError, TypeError):
            continue
    return radiuses


def extract_boom_lengths_from_xlsx(df: pd.DataFrame) -> List[str]:
    """
    Extract the boom lengths from the lifting capacity table.

    Args:
        df: pandas DataFrame containing the Excel data

    Returns:
        List of boom lengths
    """
    boom_lengths = []
    for col in range(TABLE_START_COL + 1, df.shape[1]):
        value = df.iloc[TABLE_START_ROW, col]
        if pd.isna(value) or value == "":
            break
        try:
            value_str = str(value).strip()
            boom_lengths.append(value_str)
        except (ValueError, TypeError):
            continue
    return boom_lengths


def extract_lc_table_from_xlsx(df: pd.DataFrame) -> Tuple[str, LcTable]:
    """
    Parse the lifting capacity table from an Excel DataFrame.

    Table structure:
    - "Вылет, м" is located in cell B4
    - Boom lengths are in the header row starting from C4
    - Radius values are in the first column starting from B5
    - Empty values are marked with "-" or 0

    Args:
        df: pandas DataFrame containing the Excel data

    Returns:
        Tuple containing:
            - table_name: str, the name of the lifting capacity table
              (from cell B1)
            - LcTable object with:
                - radiuses: List[str], the list of all
                  radius values in the table (from B5 downwards)
                - table: Dict[str, Dict[str, float]],
                  mapping boom length (header, from C4 onwards)
                  to a dict of radius(str): lifting capacity (float).
        Example:
            (
                "Main boom table",    # table_name
                LcTable(
                    lc_table_radiuses=["3.0", "3.5", "4.0", ...],
                    lc_table={
                        "11.5*": {
                            "3.0": 95.0,
                            "3.5": 86.0,
                            "4.0": 78.0,
                            ...
                        },
                        "11.5": {
                            "3.0": 83.0,
                            "3.5": 80.0,
                            ...
                        },
                        ...
                    }
                )
            )
    """

    table_name = str(df.iloc[0, 1]).strip()  # B1

    radiuses = extract_lc_table_radiuses_from_xlsx(df)

    # Get boom lengths from the header row (C4 onwards)
    boom_lengths = extract_boom_lengths_from_xlsx(df)

    # Initialize the lifting capacity table dictionary
    # Structure: Dict[boom_length, Dict[radius, capacity]]
    table: Dict[str, Dict[str, float]] = {
        boom_length: {} for boom_length in boom_lengths
    }

    # Process each row starting from B9
    row_idx = TABLE_START_ROW + 1
    while row_idx < df.shape[0]:
        try:
            # Get radius value from column B
            radius = df.iloc[row_idx, TABLE_START_COL]
            if pd.isna(radius) or radius == "":
                break
            radius = str(radius).strip()

            # Process each boom length column
            for col_idx, boom_length in enumerate(boom_lengths):
                # Starting from column C
                capacity = df.iloc[row_idx, TABLE_START_COL + 1 + col_idx]

                # Skip empty or invalid values
                if pd.isna(capacity) or capacity in ["-", "", 0]:
                    continue

                try:
                    capacity = float(capacity)
                    table[boom_length][radius] = capacity
                except (ValueError, TypeError):
                    continue

            row_idx += 1
        except Exception:
            break

    return table_name, LcTable(
        radiuses=radiuses,
        table=table,
    )
