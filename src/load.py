"""Load data into SQLite using idempotent upserts."""
from pathlib import Path
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE IF NOT EXISTS sales (
    sale_id TEXT PRIMARY KEY,
    sale_date TEXT NOT NULL,
    product TEXT NOT NULL,
    category TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price REAL NOT NULL CHECK (unit_price >= 0),
    total_amount REAL NOT NULL CHECK (total_amount >= 0)
);
"""


def load_sales(df: pd.DataFrame, database: str | Path) -> int:
    path = Path(database)
    path.parent.mkdir(parents=True, exist_ok=True)
    records = list(df.itertuples(index=False, name=None))
    with sqlite3.connect(path) as conn:
        conn.execute(SCHEMA)
        conn.executemany("""
            INSERT INTO sales (sale_id, sale_date, product, category, quantity, unit_price, total_amount)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(sale_id) DO UPDATE SET
              sale_date=excluded.sale_date, product=excluded.product,
              category=excluded.category, quantity=excluded.quantity,
              unit_price=excluded.unit_price, total_amount=excluded.total_amount
        """, records)
        conn.commit()
    return len(records)
