"""Universal import pipeline orchestration."""

from pathlib import Path

from app.services.dedup_service import mark_duplicates
from statement_import.classifier import HeuristicClassifier
from statement_import.extractors.ocr_extractor import OCRExtractor
from statement_import.extractors.table_extractor import TableExtractor
from statement_import.extractors.text_extractor import TextExtractor
from statement_import.normalizers.transaction_normalizer import TransactionNormalizer
from statement_import.readers.pdf_reader import PDFReader
from statement_import.registry import ParserRegistry


class StatementImportPipeline:
    """Coordinates ingestion stages from file load to import reporting."""

    def __init__(self) -> None:
        self.reader = PDFReader()
        self.text_extractor = TextExtractor()
        self.table_extractor = TableExtractor()
        self.ocr_extractor = OCRExtractor()
        self.classifier = HeuristicClassifier()
        self.registry = ParserRegistry()
        self.normalizer = TransactionNormalizer()

    def run(self, file_path: Path, password: str | None = None, preview_only: bool = True) -> dict:
        warnings: list[str] = []
        errors: list[str] = []

        raw = self.reader.load(file_path, password=password)
        extracted = self.text_extractor.extract(raw)
        extracted = self.table_extractor.extract(extracted)

        if extracted.get("is_scanned"):
            extracted = self.ocr_extractor.extract(extracted)
            warnings.append("Statement appears scanned; OCR placeholder path used")

        classification = self.classifier.classify(extracted)
        parser = self.registry.create_parser(classification)
        parsed_rows = parser.parse(extracted)
        normalized = [self.normalizer.normalize(row, file_path=str(file_path)) for row in parsed_rows]
        normalized = [row for row in normalized if row.get("transaction_date") and row.get("description")]
        normalized = mark_duplicates(normalized)

        if not normalized:
            warnings.append("No transactions parsed from statement")

        return {
            "source_file": str(file_path),
            "classification": classification,
            "selected_parser": parser.name,
            "preview_only": preview_only,
            "detected_transactions": len(normalized),
            "normalized_transactions": normalized,
            "warnings": warnings,
            "errors": errors,
        }
