"""
This module contains the functions for serving crane attachments.
"""
from urllib.parse import quote

from fastapi import HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db.queries import get_crane_attachment_db_model_by_id
from app.settings import SUPPORTED_IMAGE_CONTENT_TYPES


def serve_attachment(attachment_id: int, db: Session):
    """
    Serve a crane attachment by its ID.
    Images are displayed inline, other files are downloaded.

    Args:
        attachment_id: ID of the attachment to serve
        db: Database session

    Returns:
        File content as inline display for images or
        downloadable response for other files
    """
    attachment = get_crane_attachment_db_model_by_id(db, attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")

    # Determine if this is an image that should be displayed inline
    is_image = attachment.content_type in SUPPORTED_IMAGE_CONTENT_TYPES

    # Set appropriate headers based on content type
    headers = {}

    # Properly encode filename for Content-Disposition header
    # Use RFC 5987 encoding for international characters
    filename = attachment.filename
    encoded_filename = quote(filename, safe="")

    if is_image:
        # Images: display inline
        headers["Content-Disposition"] = (
            f"inline; filename={encoded_filename}; "
            f"filename*=UTF-8''{encoded_filename}"
        )
    else:
        # Other files: download
        headers["Content-Disposition"] = (
            f"attachment; filename={encoded_filename}; "
            f"filename*=UTF-8''{encoded_filename}"
        )

    # Return the file with appropriate headers
    return Response(
        content=attachment.data,
        media_type=attachment.content_type,
        headers=headers,
    )
