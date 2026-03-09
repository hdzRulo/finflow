import pytest

from statement_import.exceptions import StatementDecryptionError
from statement_import.readers.pdf_reader import PDFReader


class DummyReader:
    is_encrypted = True
    pages = []

    def decrypt(self, password):
        return 0


def test_pdf_reader_requires_password(monkeypatch):
    monkeypatch.setattr("statement_import.readers.pdf_reader.PdfReader", lambda _: DummyReader())
    with pytest.raises(StatementDecryptionError):
        PDFReader().load(file_path="dummy.pdf")
