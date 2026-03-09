from statement_import.parsers.generic_table_parser import GenericTableParser


def test_generic_table_parser_returns_tables():
    parser = GenericTableParser()
    payload = {"tables": [{"description": "Coffee", "amount": -4.5}]}
    assert parser.parse(payload) == payload["tables"]
