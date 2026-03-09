"""Import service that orchestrates statement pipeline integration."""

import logging
from pathlib import Path

from statement_import.pipeline import StatementImportPipeline

logger = logging.getLogger(__name__)


class ImportService:
    """Facade for initiating parser pipeline and returning report payloads."""

    def __init__(self) -> None:
        self.pipeline = StatementImportPipeline()

    def preview_import(self, file_path: str) -> dict:
        logger.info("Generating preview for %s", file_path)
        return self.pipeline.run(Path(file_path), preview_only=True)

    def execute_import(self, file_path: str) -> dict:
        logger.info("Executing import for %s", file_path)
        return self.pipeline.run(Path(file_path), preview_only=False)
