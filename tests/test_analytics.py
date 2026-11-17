import pandas as pd
from src.analytics import summarize_sales


def test_kpis():
    df = pd.DataFrame({
        "sale_id": ["S1", "S2"],
        "quantity": [2, 3],
        "total_amount": [20.0, 45.0],
    })
    assert summarize_sales(df) == {
        "revenue": 65.0,
        "orders": 2,
        "units": 5,
        "average_ticket": 32.5,
    }


def test_empty_dataset():
    df = pd.DataFrame(columns=["sale_id", "quantity", "total_amount"])
    assert summarize_sales(df)["average_ticket"] == 0
