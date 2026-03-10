from app.config import Settings


def test_ensure_sqlite_parent_dir_creates_missing_directory(tmp_path):
    db_file = tmp_path / "missing" / "nested" / "finance.db"

    Settings._ensure_sqlite_parent_dir(f"sqlite:///{db_file}")

    assert db_file.parent.exists()


def test_ensure_sqlite_parent_dir_skips_in_memory_sqlite(tmp_path):
    marker_dir = tmp_path / "marker"

    Settings._ensure_sqlite_parent_dir("sqlite:///:memory:")

    assert not marker_dir.exists()
