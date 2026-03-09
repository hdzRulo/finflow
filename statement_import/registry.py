"""Registry/factory for parser selection."""

from statement_import.parsers.base_parser import BaseStatementParser
from statement_import.parsers.example_bank_parser_a import ExampleBankParserA
from statement_import.parsers.example_bank_parser_b import ExampleBankParserB
from statement_import.parsers.generic_line_parser import GenericLineParser
from statement_import.parsers.generic_table_parser import GenericTableParser


class ParserRegistry:
    """Maintains parser plugins and resolves best parser by classification hints."""

    def __init__(self) -> None:
        self._parsers: list[type[BaseStatementParser]] = []
        self._register_defaults()

    def _register_defaults(self) -> None:
        self.register(ExampleBankParserA)
        self.register(ExampleBankParserB)
        self.register(GenericTableParser)
        self.register(GenericLineParser)

    def register(self, parser_cls: type[BaseStatementParser]) -> None:
        self._parsers.append(parser_cls)

    def create_parser(self, classification: dict) -> BaseStatementParser:
        confidence = classification.get("confidence", 0)
        if confidence >= 0.8:
            for parser_cls in self._parsers[:2]:
                if parser_cls.can_parse(classification):
                    return parser_cls()

        if GenericTableParser.can_parse(classification):
            return GenericTableParser()
        return GenericLineParser()
