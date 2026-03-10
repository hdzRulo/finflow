from statement_import.parsers.generic_line_parser import GenericLineParser
from statement_import.parsers.generic_table_parser import GenericTableParser


def test_generic_table_parser_maps_rows():
    parser = GenericTableParser()
    payload = {"tables": [{"raw": ["2024-01-01", "Coffee", "-4.50", "100.00"]}]}
    out = parser.parse(payload)
    assert out[0]["description"] == "Coffee"
    assert out[0]["amount"] == "-4.50"


def test_generic_line_parser_extracts_line_transactions():
    parser = GenericLineParser()
    payload = {"text": "01/01/2024 Grocery Store -24.10"}
    out = parser.parse(payload)
    assert len(out) == 1
    assert out[0]["description"] == "Grocery Store"
