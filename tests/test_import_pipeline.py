from pathlib import Path

from statement_import.pipeline import StatementImportPipeline


def test_import_pipeline_preview_uses_parser(monkeypatch):
    pipeline = StatementImportPipeline()

    monkeypatch.setattr(pipeline.reader, "load", lambda path: {"text": "Example Bank A", "tables": []})
    report = pipeline.run(Path("dummy.pdf"), preview_only=True)

    assert report["preview_only"] is True
    assert "selected_parser" in report
