"""Generic parser for table-oriented statements."""

from statement_import.parsers.base_parser import BaseStatementParser


class GenericTableParser(BaseStatementParser):
    name = "generic_table"

    @classmethod
    def can_parse(cls, classification: dict) -> bool:
        return classification.get("layout_family") in {"table", "generic"}

    def parse(self, extracted_payload: dict) -> list[dict]:
        return extracted_payload.get("tables", [])
