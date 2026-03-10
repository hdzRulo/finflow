from pathlib import Path

from statement_import.pipeline import StatementImportPipeline


def test_import_pipeline_happy_path(monkeypatch):
    pipeline = StatementImportPipeline()

    monkeypatch.setattr(
        pipeline.reader,
        "load",
        lambda path, password=None: {
            "text": "A-BANK 2024-01-01 Grocery -10.00",
            "tables": [],
            "is_scanned": False,
        },
    )
    report = pipeline.run(Path("dummy.pdf"), preview_only=True)

    assert report["preview_only"] is True
    assert report["selected_parser"] == "example_bank_a"
    assert report["detected_transactions"] == 1


def test_import_pipeline_forwards_pdf_password(monkeypatch):
    pipeline = StatementImportPipeline()
    received: dict[str, str | None] = {"password": None}

    def fake_load(path, password=None):
        received["password"] = password
        return {
            "text": "A-BANK 2024-01-01 Grocery -10.00",
            "tables": [],
            "is_scanned": False,
        }

    monkeypatch.setattr(pipeline.reader, "load", fake_load)

    pipeline.run(Path("dummy.pdf"), password="s3cr3t", preview_only=True)

    assert received["password"] == "s3cr3t"
