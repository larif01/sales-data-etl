import sqlite3
import pandas as pd
import pytest
from src.transform import transform_sales
from src.main import run


def test_valid_invalid_and_duplicates():
    data = pd.DataFrame([
        {"sale_id":"s1", "sale_date":"2026-01-01", "product":" mouse ","category":"tech","quantity":"2","unit_price":"10.50"},
        {"sale_id":"s1", "sale_date":"2026-01-01", "product":"mouse","category":"tech","quantity":"2","unit_price":"10.50"},
        {"sale_id":"s2", "sale_date":"2026-01-01", "product":"mouse","category":"tech","quantity":"-1","unit_price":"10.50"},
    ])
    valid, rejected = transform_sales(data)
    assert len(valid) == 1
    assert len(rejected) == 2
    assert valid.iloc[0]["total_amount"] == pytest.approx(21)
    assert valid.iloc[0]["sale_id"] == "S1"
    assert set(rejected["rejection_reason"]) == {"duplicate_sale_id", "missing_or_invalid_fields"}


def test_required_columns():
    with pytest.raises(ValueError, match="Missing required columns"):
        transform_sales(pd.DataFrame({"sale_id": ["S1"]}))


def test_pipeline_is_idempotent(tmp_path):
    source = tmp_path / "sales.csv"
    source.write_text("sale_id,sale_date,product,category,quantity,unit_price\nS1,2026-01-01,Mouse,Tech,2,10.50\n")
    database, rejected = tmp_path / "sales.db", tmp_path / "rejected.csv"
    assert run(source, database, rejected)["loaded"] == 1
    assert run(source, database, rejected)["loaded"] == 1
    with sqlite3.connect(database) as conn:
        assert conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0] == 1
