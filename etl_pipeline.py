import pandas as pd
import sqlite3
import yaml
import logging
from pathlib import Path


# 1. Load Configuration

def load_config(path="config.yaml"):
    """Load YAML configuration safely."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    
    content = content.replace("\ufeff", "")

    # Parse YAML safely
    config = yaml.safe_load(content)

    if config is None:
        raise ValueError(f"YAML file '{path}' is empty or invalid. Check formatting.")

    return config



# 2. Setup Logging

def setup_logging(level: str):
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s - %(levelname)s - %(message)s"
    )



# 3. Extract

def extract(csv_path: str, delimiter: str = ",") -> pd.DataFrame:
    """Read data from CSV file."""
    logging.info(f"Extracting data from {csv_path}...")
    if not Path(csv_path).exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path, delimiter=delimiter)
    logging.info(f"Extracted {len(df)} rows.")
    return df



# 4. Transform

def transform(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Clean and transform the data."""
    logging.info("Transforming data...")

    # Drop completely empty rows
    if config["transformations"].get("drop_empty_rows", True):
        before = len(df)
        df = df.dropna(how="all")
        logging.info(f"Dropped {before - len(df)} empty rows.")

    # Normalize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Trim whitespace in string columns
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()

    # Filter active rows (if applicable)
    if config["transformations"].get("filter_active", False) and "status" in df.columns:
        before = len(df)
        df = df[df["status"].str.lower() == "active"]
        logging.info(f"Filtered {before - len(df)} inactive rows.")

    logging.info(f"Transformed {len(df)} rows.")
    return df


# 5. Load

def load(df: pd.DataFrame, db_path: str, table_name: str):
    """Load transformed data into SQL database."""
    logging.info(f"Loading data into {table_name} table...")

    conn = sqlite3.connect(db_path)
    try:
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        logging.info(f"Successfully loaded {len(df)} rows into '{table_name}'.")
    finally:
        conn.close()


# 6. Summary Reporting

def generate_summary(df: pd.DataFrame, config: dict):
    """Generate and log a simple summary report."""
    logging.info("Generating summary report...")

    total_rows = len(df)
    active_rows = df["status"].str.lower().eq("active").sum() if "status" in df.columns else 0
    inactive_rows = total_rows - active_rows

    missing_age = df["age"].isna().sum() if "age" in df.columns else 0
    missing_country = df["country"].isna().sum() if "country" in df.columns else 0
    unique_countries = df["country"].dropna().nunique() if "country" in df.columns else 0

    summary = f"""
---------- DATA SUMMARY ----------
Total rows loaded: {total_rows}
Active customers: {active_rows}
Inactive customers: {inactive_rows}
Missing Age values: {missing_age}
Missing Country values: {missing_country}
Countries represented: {unique_countries}
----------------------------------
"""
    print(summary)
    logging.info(summary)

    #Save summary to text file
    report_path = Path(config["database"]["db_path"]).with_suffix(".summary.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(summary)

    logging.info(f"Summary report saved to: {report_path}")


# 7. ETL Runner

def run_etl():
    """Execute the full ETL pipeline using configuration."""
    config = load_config(r"C:\Users\gokul\Downloads\Gokul's Documents\Project\config.yaml")

    setup_logging(config["logging"]["level"])

    logging.info("Starting ETL pipeline with YAML config...")

    try:
        df_raw = extract(
            csv_path=config["data_source"]["csv_path"],
            delimiter=config["data_source"].get("delimiter", ",")
        )
        df_clean = transform(df_raw, config)
        load(
            df_clean,
            db_path=config["database"]["db_path"],
            table_name=config["database"]["table_name"]
        )
        generate_summary(df_clean, config)
        logging.info("ETL pipeline completed successfully ✅")
    except Exception as e:
        logging.error(f"ETL pipeline failed ❌: {e}")



# 7. Entry Point

if __name__ == "__main__":
    run_etl()

