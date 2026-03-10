"""Generic parser for table-oriented statements."""

from statement_import.parsers.base_parser import BaseStatementParser


class GenericTableParser(BaseStatementParser):
    name = "generic_table"

    @classmethod
    def can_parse(cls, classification: dict) -> bool:
        return classification.get("layout_family") == "table"

    def parse(self, extracted_payload: dict) -> list[dict]:
        rows = []
        for item in extracted_payload.get("tables", []):
            raw = item.get("raw", [])
            if len(raw) >= 3:
                rows.append(
                    {
                        "transaction_date": raw[0],
                        "description": raw[1],
                        "amount": raw[2],
                        "balance": raw[3] if len(raw) > 3 else None,
                        "raw_text": " | ".join([str(x) for x in raw if x]),
                    }
                )
        return rows
