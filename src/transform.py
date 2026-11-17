"""Validate and normalize sales records."""
from __future__ import annotations
import pandas as pd

REQUIRED_COLUMNS = {"sale_id", "sale_date", "product", "category", "quantity", "unit_price"}
OUTPUT_COLUMNS = ["sale_id", "sale_date", "product", "category", "quantity", "unit_price", "total_amount"]


def transform_sales(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    data = df.copy()
    for col in ["sale_id", "sale_date", "product", "category", "quantity", "unit_price"]:
        data[col] = data[col].fillna("").astype(str).str.strip()
    data["sale_id"] = data["sale_id"].str.upper()
    data["product"] = data["product"].str.title()
    data["category"] = data["category"].str.title()
    data["sale_date"] = pd.to_datetime(data["sale_date"], errors="coerce", format="%Y-%m-%d")
    data["quantity"] = pd.to_numeric(data["quantity"], errors="coerce")
    data["unit_price"] = pd.to_numeric(data["unit_price"], errors="coerce")
    invalid = (
        data["sale_id"].eq("") | data["product"].eq("") | data["category"].eq("") |
        data["sale_date"].isna() | data["quantity"].isna() | data["unit_price"].isna() |
        (data["quantity"] <= 0) | (data["quantity"] % 1 != 0) | (data["unit_price"] < 0)
    )
    data["rejection_reason"] = ""
    data.loc[invalid, "rejection_reason"] = "missing_or_invalid_fields"
    duplicate = data["sale_id"].duplicated(keep="first") & ~invalid
    data.loc[duplicate, "rejection_reason"] = "duplicate_sale_id"
    rejected = data.loc[data["rejection_reason"].ne("")].copy()
    valid = data.loc[data["rejection_reason"].eq("")].copy()
    valid["quantity"] = valid["quantity"].astype(int)
    valid["unit_price"] = valid["unit_price"].round(2)
    valid["total_amount"] = (valid["quantity"] * valid["unit_price"]).round(2)
    valid["sale_date"] = valid["sale_date"].dt.strftime("%Y-%m-%d")
    return valid[OUTPUT_COLUMNS].reset_index(drop=True), rejected.reset_index(drop=True)
