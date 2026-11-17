# Sales Data ETL 📊

A reproducible beginner-friendly **Extract → Transform → Load (ETL)** pipeline using Python, Pandas, SQLite and automated tests. Built as a data engineering portfolio project.

## Architecture

`CSV (raw) → Pandas extraction & validation → SQLite (sales) → SQL analysis`

## Features

- Reads raw CSV sales records.
- Normalizes product/category names, IDs and dates.
- Rejects malformed, duplicate or invalid rows, saving a rejection report.
- Computes total revenue per sale (`quantity * unit_price`).
- Loads into SQLite with **upsert** logic for idempotent runs.
- Includes pytest tests and GitHub Actions CI.

## Quick start

Python 3.10+ required (3.12 recommended).

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.main
python -m pytest -q
```

The CLI creates `outputs/sales.db` and `outputs/rejected_sales.csv`. These generated artifacts are ignored by Git.

### Custom file locations

```bash
python -m src.main --input data/sales.csv --database outputs/sales.db --rejected outputs/rejected_sales.csv
```

### SQL analysis

Open `outputs/sales.db` with DB Browser for SQLite or run:

```bash
sqlite3 outputs/sales.db < sql/analysis.sql
```

Example dataset contains **15 rows: 10 valid and 5 rejected** (including one duplicate ID). All records are synthetic for demonstration.

## Quality rules

A sale is valid if its ID, date (YYYY-MM-DD), product, category, positive integer quantity and nonnegative unit price are present. Duplicate IDs are rejected after the first occurrence; the loader upserts existing records by `sale_id`.

## Project layout

- `src/extract.py` – CSV extraction
- `src/transform.py` – validation, cleaning and metrics
- `src/load.py` – SQLite schema and upsert
- `src/main.py` – runnable CLI
- `tests/` – automated checks
- `sql/analysis.sql` – business questions
- `.github/workflows/ci.yml` – continuous integration

## Future enhancements

Add PostgreSQL, data quality reporting, scheduler/orchestration and Power BI in a follow-up project.
