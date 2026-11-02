"""Utilities for handling S3 notification event fields."""

from urllib.parse import unquote_plus


def decode_s3_object_key(encoded_key: str) -> str:
    """Decode the URL-encoded object key supplied in an S3 event.

    S3 notification records encode object keys using form-style URL encoding:
    spaces may appear as '+', while a literal plus sign is encoded as '%2B'.
    """
    if not isinstance(encoded_key, str) or not encoded_key:
        raise ValueError("S3 object key must be a non-empty string")

    return unquote_plus(encoded_key)
