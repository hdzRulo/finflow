"""Generic parser for line-by-line statement text."""

from statement_import.parsers.base_parser import BaseStatementParser


class GenericLineParser(BaseStatementParser):
    name = "generic_line"

    @classmethod
    def can_parse(cls, classification: dict) -> bool:
        return True

    def parse(self, extracted_payload: dict) -> list[dict]:
        # Placeholder tokenization strategy.
        text = extracted_payload.get("text", "")
        return [] if not text else [{"description": "UNPARSED LINE", "raw_text": text[:120]}]
