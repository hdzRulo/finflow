# FinFlow (Stage 2 MVP)

FinFlow is a Python-first personal finance tracker with a working MVP statement import pipeline.

## Features implemented
- Transaction CRUD + filtering (date/category/description/amount)
- Category management
- Dashboard summaries (income vs expense, spending by category, recent transactions)
- Statement PDF upload + optional password support
- Text vs scanned-PDF detection
- Parser selection (bank-specific -> generic table -> generic line)
- Transaction normalization (date/amount/description/sign)
- Deduplication via transaction fingerprint
- Preview-before-import with duplicate flags
- Import history tracking

## Project tree
```text
finflow/
  app/
  statement_import/
  ui/
  tests/
  sample_data/
  data/
  requirements.txt
  README.md
```

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- API docs: `http://127.0.0.1:8000/docs`
- NiceGUI pages:
  - `/`
  - `/transactions-ui`
  - `/import`
  - `/import-history`

## Import flow (end-to-end)
1. Upload PDF from `/import`
2. Enter password if needed
3. Preview parses + selected parser + duplicate flags
4. Confirm import (duplicates skipped by default)
5. Check `/import-history`

## API endpoints
- `GET/POST/PUT/DELETE /transactions`
- `GET/POST /categories`
- `POST /imports/preview` (multipart file + optional password)
- `POST /imports/confirm/{preview_id}`
- `GET /imports/history`

## Add a new parser plugin
1. Create parser in `statement_import/parsers/` inheriting `BaseStatementParser`
2. Implement `can_parse(classification)` + `parse(extracted_payload)`
3. Register parser in `statement_import/registry.py`
4. Add parser tests in `tests/`

## Notes
- OCR path is intentionally a clean abstraction with placeholder extraction in MVP.
- Universal parsing is extensible; this MVP focuses on framework + baseline behavior.
