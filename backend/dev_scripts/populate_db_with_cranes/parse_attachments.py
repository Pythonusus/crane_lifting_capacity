"""
Module for handling crane attachment files.

This module handles finding, reading, and processing crane attachment files
from the file system.
"""

import mimetypes
import os
from typing import List

from app.schemas.cranes import CraneBinaryAttachment


def get_content_type(filename: str) -> str:
    """Determine the content type based on file extension."""
    content_type, _ = mimetypes.guess_type(filename)
    if content_type is None:
        # Fallback for unsupported extensions
        if filename.lower().endswith('.dwg'):
            return 'application/acad'
        if filename.lower().endswith('.xlsx'):
            return 'application/vnd.ms-excel'
        return 'application/octet-stream'
    return content_type


def find_crane_attachments(attachments_dir: str) -> List[CraneBinaryAttachment]:
    """
    Find all attachment files for a specific crane.

    Args:
        attachments_dir: Directory containing the crane's files

    Returns:
        List of CraneBinaryAttachment objects
    """
    attachments = []

    if not os.path.exists(attachments_dir):
        print(f"No crane directory found at: {attachments_dir}")
        return attachments

    # Process all files in the crane directory
    for filename in os.listdir(attachments_dir):
        file_path = os.path.join(attachments_dir, filename)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        with open(file_path, 'rb') as f:
            file_data = f.read()

            # Create CraneBinaryAttachment object
            attachment = CraneBinaryAttachment(
                filename=filename,
                content_type=get_content_type(filename),
                data=file_data
            )

            attachments.append(attachment)

    return attachments
