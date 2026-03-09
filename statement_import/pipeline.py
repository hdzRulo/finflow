"""Universal import pipeline orchestration."""

from pathlib import Path

from statement_import.classifier import HeuristicClassifier
from statement_import.extractors.text_extractor import TextExtractor
from statement_import.normalizers.transaction_normalizer import TransactionNormalizer
from statement_import.readers.pdf_reader import PDFReader
from statement_import.registry import ParserRegistry


class StatementImportPipeline:
    """Coordinates ingestion stages from file load to import reporting."""

    def __init__(self) -> None:
        self.reader = PDFReader()
        self.extractor = TextExtractor()
        self.classifier = HeuristicClassifier()
        self.registry = ParserRegistry()
        self.normalizer = TransactionNormalizer()

    def run(self, file_path: Path, preview_only: bool = True) -> dict:
        """Run staged ingestion pipeline. Placeholder business logic."""
        raw = self.reader.load(file_path)
        extracted = self.extractor.extract(raw)
        classification = self.classifier.classify(extracted)
        parser = self.registry.create_parser(classification)
        parsed_rows = parser.parse(extracted)
        normalized = [self.normalizer.normalize(row, file_path=str(file_path)) for row in parsed_rows]
        report = {
            "source_file": str(file_path),
            "classification": classification,
            "selected_parser": parser.name,
            "preview_only": preview_only,
            "detected_transactions": len(normalized),
            "normalized_transactions": normalized,
        }
        return report
