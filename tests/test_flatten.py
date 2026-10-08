"""Small regression checks for the JSON-to-tabular flatten transformation.

The tests use synthetic data only and document expected transformation behavior.
Adapt the import path to the project's existing module layout when running locally.
"""

import pytest

try:
    from flatten import flatten
except ImportError:
    flatten = None


@pytest.mark.skipif(flatten is None, reason="flatten module is not available in this checkout")
def test_flatten_nested_record():
    records = [{"customer": {"id": 101, "name": "Asha"}, "amount": 250.50}]

    result = flatten(records)

    assert result[0]["customer_id"] == 101
    assert result[0]["customer_name"] == "Asha"
    assert result[0]["amount"] == 250.50


@pytest.mark.skipif(flatten is None, reason="flatten module is not available in this checkout")
def test_flatten_preserves_multiple_records():
    records = [
        {"customer": {"id": 101}, "amount": 100},
        {"customer": {"id": 102}, "amount": 200},
    ]

    result = flatten(records)

    assert len(result) == 2
    assert {row["customer_id"] for row in result} == {101, 102}
