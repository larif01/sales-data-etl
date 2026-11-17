"""Extract sales data from CSV."""
from pathlib import Path
import pandas as pd


def extract_sales(path: str | Path) -> pd.DataFrame:
    """Read CSV as strings to preserve identifiers and validate later."""
    return pd.read_csv(path, dtype=str, keep_default_na=False)
