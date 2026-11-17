"""Command-line entry point for the ETL pipeline."""
from __future__ import annotations
import argparse
import logging
from pathlib import Path
from src.extract import extract_sales
from src.transform import transform_sales
from src.load import load_sales

LOGGER = logging.getLogger(__name__)


def run(input_path: Path, database_path: Path, rejected_path: Path) -> dict[str, int]:
    source = extract_sales(input_path)
    valid, rejected = transform_sales(source)
    loaded = load_sales(valid, database_path)
    rejected_path.parent.mkdir(parents=True, exist_ok=True)
    rejected.to_csv(rejected_path, index=False)
    stats = {"extracted": len(source), "valid": len(valid), "rejected": len(rejected), "loaded": loaded}
    LOGGER.info("ETL summary: %s", stats)
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="ETL for CSV sales data")
    parser.add_argument("--input", type=Path, default=Path("data/sales.csv"))
    parser.add_argument("--database", type=Path, default=Path("outputs/sales.db"))
    parser.add_argument("--rejected", type=Path, default=Path("outputs/rejected_sales.csv"))
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    print(run(args.input, args.database, args.rejected))


if __name__ == "__main__":
    main()
