# Simple ETL Pipeline (CSV-to-SQLite)
This project demonstrates a basic Extract, Transform, Load (ETL) pipeline built in Python using YAML configuration.
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
├── etl_demo.db  # generated after running
└── etl_demo_summary.txt  # generated after running

---

## 3. Installation and Setup

### Prerequisites
- Python 3.8 or higher

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/CodeBoiCarti/Simple-ETL-Pipeline.git
   cd etl-pipeline
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run the pipeline:

bash
Copy code
python etl_pipeline.py
