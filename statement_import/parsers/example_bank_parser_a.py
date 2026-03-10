"""Example plugin parser for Bank A format."""

import re

from statement_import.parsers.base_parser import BaseStatementParser

PATTERN = re.compile(r"A-BANK\s+(?P<date>\d{4}-\d{2}-\d{2})\s+(?P<desc>.*?)\s+(?P<amount>-?[\d,]+\.\d{2})")


class ExampleBankParserA(BaseStatementParser):
    name = "example_bank_a"

    @classmethod
    def can_parse(cls, classification: dict) -> bool:
        return classification.get("bank_name") == "ExampleBankA"

    def parse(self, extracted_payload: dict) -> list[dict]:
        rows = []
        for line in (extracted_payload.get("text") or "").splitlines():
            m = PATTERN.search(line)
            if m:
                rows.append(
                    {
                        "transaction_date": m.group("date"),
                        "description": m.group("desc"),
                        "amount": m.group("amount"),
                        "raw_text": line,
                    }
                )
        return rows
