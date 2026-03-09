"""Generic parser for line-by-line statement text."""

import re

from statement_import.parsers.base_parser import BaseStatementParser

LINE_PATTERN = re.compile(r"(?P<date>\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s+(?P<description>.*?)\s+(?P<amount>-?\$?[\d,]+(?:\.\d{2})?)$")


class GenericLineParser(BaseStatementParser):
    name = "generic_line"

    @classmethod
    def can_parse(cls, classification: dict) -> bool:
        return classification.get("layout_family") in {"line", "generic"}

    def parse(self, extracted_payload: dict) -> list[dict]:
        rows = []
        for line in (extracted_payload.get("text") or "").splitlines():
            m = LINE_PATTERN.search(line.strip())
            if m:
                rows.append(
                    {
                        "transaction_date": m.group("date"),
                        "description": m.group("description"),
                        "amount": m.group("amount"),
                        "raw_text": line,
                    }
                )
        return rows
