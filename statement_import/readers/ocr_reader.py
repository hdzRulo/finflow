"""OCR abstraction placeholder for scanned PDFs/images."""


class OCRReader:
    """Wrap OCR providers (Tesseract/Cloud OCR) behind one interface."""

    def extract_text(self, image_bytes: bytes) -> str:
        """Placeholder OCR extraction method."""
        return ""
