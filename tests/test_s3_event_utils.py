"""Unit tests for S3 notification object-key decoding."""

import pytest

from s3_event_utils import decode_s3_object_key


@pytest.mark.parametrize(
    ("encoded_key", "expected"),
    [
        ("orders%2Fdaily%20sales.json", "orders/daily sales.json"),
        ("incoming%2Ffile+with+spaces.csv", "incoming/file with spaces.csv"),
        ("incoming%2Fprice%2Btax.csv", "incoming/price+tax.csv"),
        ("already-readable.json", "already-readable.json"),
    ],
)
def test_decode_s3_object_key(encoded_key, expected):
    assert decode_s3_object_key(encoded_key) == expected


@pytest.mark.parametrize("invalid_key", ["", None, 123])
def test_decode_s3_object_key_rejects_invalid_input(invalid_key):
    with pytest.raises(ValueError, match="non-empty string"):
        decode_s3_object_key(invalid_key)
