"""Example plugin parser for Bank A table-based format."""

from statement_import.parsers.base_parser import BaseStatementParser


class ExampleBankParserA(BaseStatementParser):
    name = "example_bank_a"

    @classmethod
    def can_parse(cls, classification: dict) -> bool:
        return classification.get("bank_name") == "ExampleBankA"

    def parse(self, extracted_payload: dict) -> list[dict]:
        # Placeholder parser implementation.
        return []
