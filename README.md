# FinFlow

FinFlow is a Python-first personal finance tracker web app scaffold designed around a **universal bank statement parser framework**.

## Tech Stack
- **Backend/API**: FastAPI
- **UI**: NiceGUI
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Visualization**: Plotly
- **Data processing**: pandas
- **PDF processing**: pypdf, pdfplumber

## Project Structure

```text
finflow/
├── app/
│   ├── api/
│   ├── services/
│   ├── config.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── statement_import/
│   ├── extractors/
│   ├── matchers/
│   ├── normalizers/
│   ├── parsers/
│   ├── readers/
│   ├── classifier.py
│   ├── exceptions.py
│   ├── pipeline.py
│   ├── registry.py
│   └── utils.py
├── ui/
├── tests/
├── sample_data/
├── data/
├── requirements.txt
└── README.md
```

## Architecture Overview

### Core Domain Models
- `Account`: source account/card metadata.
- `Category`: user-defined transaction category.
- `StatementImport`: audit trail and import history.
- `Transaction`: canonical normalized transaction schema including dedup fingerprint.

### Universal Import Pipeline (Scaffold)
The pipeline in `statement_import/pipeline.py` follows a staged ingestion flow:
1. File loading (`readers/pdf_reader.py`)
2. PDF decryption/unlocking handling
3. Statement classification (`classifier.py`)
4. Text/table extraction (`extractors/*`)
5. Parser selection (`registry.py`)
6. Transaction normalization (`normalizers/*`)
7. Deduplication hooks (`app/services/dedup_service.py`)
8. DB import hook (via API/services placeholders)
9. Import reporting payload

### Parser Framework
- **Base interfaces**:
  - `BaseStatementParser`
  - `BaseExtractor`
  - `BaseClassifier`
- **Registry/factory**:
  - `ParserRegistry` supports plugin-style parser registration.
- **Fallback strategy**:
  - Generic table parser and generic line parser.
- **Plugin examples**:
  - `ExampleBankParserA`
  - `ExampleBankParserB`

### API Contracts
FastAPI router scaffolds:
- `/transactions`
- `/categories`
- `/imports/preview`
- `/imports/run`

Pydantic schemas cover create/read flows for categories, accounts, transactions, and statement imports.

### UI Skeleton (NiceGUI)
Pages:
- Dashboard (`/`)
- Transactions (`/transactions`)
- Statement import (`/import`) with preview-before-import UX placeholders
- Import history (`/import-history`)

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Stage 1 Scope
This scaffold intentionally provides **architecture + extensibility hooks** with placeholder implementations. It does not yet include production-grade parser logic for real bank formats.

## Next Implementation Steps
1. Add robust PDF/table extraction with `pdfplumber` and pandas DataFrames.
2. Implement OCR provider integration for scanned statements.
3. Build parser test fixtures per bank and format version.
4. Add deduplication against existing DB records (not just in-batch).
5. Implement authenticated user model and multi-user data isolation.
6. Wire UI tables/charts to real API-backed queries.
7. Add import conflict resolution and reconciliation flows.
