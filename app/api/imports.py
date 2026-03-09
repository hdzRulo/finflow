"""Import API endpoints for statement uploads and history."""

import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import StatementImportRead
from app.services.import_service import ImportService

router = APIRouter(prefix="/imports", tags=["imports"])
service = ImportService()


@router.post("/preview")
async def preview_import(file: UploadFile = File(...), password: str | None = Form(default=None)):
    suffix = Path(file.filename).suffix or ".pdf"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    return service.preview_import(tmp_path, password=password)


@router.post("/confirm/{preview_id}")
def confirm_import(preview_id: str, db: Session = Depends(get_db)):
    return service.execute_import(preview_id, db)


@router.get("/history", response_model=list[StatementImportRead])
def list_history(db: Session = Depends(get_db)):
    return service.list_history(db)
