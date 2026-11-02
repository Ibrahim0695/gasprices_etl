import sys
from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROJECT_PATH = PROJECT_ROOT / "project"
sys.path.insert(0, str(PROJECT_PATH if (PROJECT_PATH / "main.py").is_file() else PROJECT_ROOT))


def run_etl():
    from main import main

    main()


with DAG(
    dag_id="gas_prices_daily",
    description="Fetch and load Washington gas prices daily",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    is_paused_upon_creation=False,
    tags=["gas-prices", "etl"],
) as dag:
    run_gas_prices_etl = PythonOperator(
        task_id="run_gas_prices_etl",
        python_callable=run_etl,
    )
