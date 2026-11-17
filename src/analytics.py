"""Reusable KPI calculations for sales analytics."""
import pandas as pd


def summarize_sales(df: pd.DataFrame) -> dict[str, float | int]:
    """Compute revenue, sales count, units and average ticket."""
    revenue = float(df["total_amount"].sum())
    orders = int(df["sale_id"].nunique())
    units = int(df["quantity"].sum())
    return {
        "revenue": round(revenue, 2),
        "orders": orders,
        "units": units,
        "average_ticket": round(revenue / orders, 2) if orders else 0.0,
    }
