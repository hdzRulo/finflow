"""Custom exceptions for statement ingestion stages."""


class StatementImportError(Exception):
    """Base exception for statement processing failures."""


class UnsupportedStatementError(StatementImportError):
    """Raised when no parser can be selected for an input statement."""


class StatementDecryptionError(StatementImportError):
    """Raised when encrypted PDF cannot be unlocked."""
