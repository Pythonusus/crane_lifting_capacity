"""
Module for handling crane attachment files.

This module handles finding, reading, and processing crane attachment files
from the file system.
"""

import mimetypes
from pathlib import Path
from typing import List, Union

from app.schemas.cranes import CraneBinaryAttachment


def get_content_type(filename: Union[str, Path]) -> str:
    """
    Determine the content type based on file extension.

    Args:
        filename: Filename or Path object to determine content type for

    Returns:
        MIME content type string
    """
    filename_str = str(filename)
    content_type, _ = mimetypes.guess_type(filename_str)
    if content_type is None:
        # Fallback for unsupported extensions
        if filename_str.lower().endswith(".dwg"):
            return "application/acad"
        if filename_str.lower().endswith(".xlsx"):
            return "application/vnd.ms-excel"
        return "application/octet-stream"
    return content_type


def parse_crane_attachments(
    crane_dir: Union[str, Path]
) -> List[CraneBinaryAttachment]:
    """
    Parse all attachment files for a specific crane.

    Args:
        attachments_dir: Directory containing the crane's files
                         (accepts both str and Path objects)

    Returns:
        List of CraneBinaryAttachment objects
    """
    attachments = []

    # Convert to Path object for consistent handling
    attachments_path = Path(crane_dir)

    if not attachments_path.exists():
        print(f"No crane directory found at: {attachments_path}")
        return attachments

    # Process all files in the crane directory
    for file_path in attachments_path.iterdir():
        # Skip directories
        if file_path.is_dir():
            continue

        try:
            with open(file_path, "rb") as f:
                file_data = f.read()

                # Create CraneBinaryAttachment object
                attachment = CraneBinaryAttachment(
                    filename=file_path.name,
                    content_type=get_content_type(file_path.name),
                    data=file_data
                )

                attachments.append(attachment)

        except (OSError, IOError) as e:
            print(f"Error reading file {file_path}: {e}")
            continue

    return attachments
