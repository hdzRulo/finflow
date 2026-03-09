"""PDF file loader with decryption placeholder support."""

from pathlib import Path

from statement_import.exceptions import StatementDecryptionError

try:
    from pypdf import PdfReader  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - environment-dependent
    PdfReader = None


class PDFReader:
    """Loads PDF content and handles encrypted statements."""

    def load(self, file_path: Path, password: str | None = None) -> dict:
        if PdfReader is None:
            raise RuntimeError("pypdf is not installed. Install dependencies from requirements.txt")

        reader = PdfReader(str(file_path))
        if reader.is_encrypted:
            if not password:
                raise StatementDecryptionError("Password required for encrypted PDF")
            if reader.decrypt(password) == 0:
                raise StatementDecryptionError("Invalid PDF password")
        text_chunks = [page.extract_text() or "" for page in reader.pages]
        return {"pages": len(reader.pages), "text": "\n".join(text_chunks), "file_path": str(file_path)}
