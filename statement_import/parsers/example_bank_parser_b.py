"""Example plugin parser for Bank B line format."""

from statement_import.parsers.base_parser import BaseStatementParser


class ExampleBankParserB(BaseStatementParser):
    name = "example_bank_b"

    @classmethod
    def can_parse(cls, classification: dict) -> bool:
        return classification.get("bank_name") == "ExampleBankB"

    def parse(self, extracted_payload: dict) -> list[dict]:
        # Placeholder parser implementation.
        return []
