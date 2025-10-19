# Simple ETL Pipeline (CSV to SQLite)

This project demonstrates a modular Extract, Transform, Load (ETL) pipeline built in Python.  
It reads configuration from a YAML file, processes customer data from a CSV source, and loads the cleaned data into a SQLite database.  
A summary report is generated at the end of each run.

---

## 1. Features

- Configurable through `config.yaml`
- Extracts data from CSV files
- Cleans and transforms data:
  - Trims whitespace
  - Normalizes column names
  - Filters active customers (optional)
  - Drops empty rows (configurable)
- Loads cleaned data into a SQLite database
- Generates a summary report including:
  - Total rows processed
  - Active/Inactive counts
  - Missing values by column
  - Number of countries represented
- Uses Python’s logging module for traceable execution

---

## 2. Project Structure
etl-pipeline/
├── data/
│   └── customers.csv
├── etl_pipeline.py
├── config.yaml
├── requirements.txt
└── README.md
├── etl_demo.db  #generated after running
└── etl_demo_summary.txt  #generated after running

## 3. Installation and Setup

### Prerequisites
- Python 3.8 or higher

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/codeboicarti/Simple-ETL-Pipeline.git
   cd Simple-ETL-Pipeline
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the pipeline:
   ```bash
   python etl_pipeline.py

8. License

This project is released under the MIT License.
You are free to use and modify it for educational or professional purposes.

