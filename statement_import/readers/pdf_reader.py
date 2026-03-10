"""PDF file loader with decryption and scan detection support."""

from pathlib import Path

from statement_import.exceptions import StatementDecryptionError

try:
    import pdfplumber
    from pypdf import PdfReader  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    PdfReader = None
    pdfplumber = None


class PDFReader:
    """Loads PDF content and handles encrypted statements."""

    def load(self, file_path: Path, password: str | None = None) -> dict:
        if PdfReader is None:
            raise RuntimeError("pypdf/pdfplumber not installed")

        reader = PdfReader(str(file_path))
        if reader.is_encrypted:
            if not password:
                raise StatementDecryptionError("Password required for encrypted PDF")
            if reader.decrypt(password) == 0:
                raise StatementDecryptionError("Invalid PDF password")

        text_chunks: list[str] = []
        tables: list[dict] = []

        with pdfplumber.open(str(file_path), password=password) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                if text:
                    text_chunks.append(text)
                extracted_tables = page.extract_tables() or []
                for t in extracted_tables:
                    for row in t[1:]:
                        if not row:
                            continue
                        tables.append({"raw": row})

        full_text = "\n".join(text_chunks)
        is_scanned = len(full_text.strip()) < 40
        return {
            "pages": len(reader.pages),
            "text": full_text,
            "tables": tables,
            "file_path": str(file_path),
            "is_scanned": is_scanned,
        }
