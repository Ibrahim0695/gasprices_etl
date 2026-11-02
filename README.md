# Gas Prices ETL

A Python ETL pipeline that retrieves Washington gas prices from CollectAPI, transforms the city-level results with pandas, and replaces the `cities` table in PostgreSQL.

## Requirements

- Python 3.8 or newer
- PostgreSQL
- A CollectAPI account and API key
- Docker Desktop with Docker Compose (for Airflow scheduling on Windows)

## Configure

Copy the example environment file and fill in your own values:

```powershell
Copy-Item .env.example .env
```

Set the PostgreSQL connection values, a valid `COLLECTAPI_KEY`, and a unique `AIRFLOW_ADMIN_PASSWORD`. Keep `.env` private; it is excluded from Git and the Docker build context. The API key must not be committed to source.

## Run the ETL manually

Create and activate a virtual environment, then install the Python dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

The loader creates or replaces the PostgreSQL `cities` table on each run.

## Run Airflow daily

Airflow runs in Docker rather than in the Windows virtual environment. The Compose setup runs the webserver and scheduler as separate services with SQLite and the SequentialExecutor for local development.

```powershell
docker compose up --build -d
```

Wait for the webserver health check, then open <http://localhost:8081>. The `gas_prices_daily` DAG is enabled and scheduled with `@daily`; catchup is disabled. Airflow metadata persists in a Docker volume.

For an existing Airflow volume created with `airflow standalone`, retrieve its generated admin password with:

```powershell
docker compose exec airflow-webserver cat /opt/airflow/standalone_admin_password.txt
```

On a fresh volume, the init service creates the admin user using `AIRFLOW_ADMIN_USERNAME` and `AIRFLOW_ADMIN_PASSWORD` from `.env`.

The Compose setup assumes PostgreSQL is reachable from Docker via the Windows host, and overrides `DATABASE_HOST` to `host.docker.internal`. If PostgreSQL is not running on the Windows host, adjust `DATABASE_HOST` in `docker-compose.yaml` to the appropriate address reachable from the containers.

View service status and logs with:

```powershell
docker compose ps
docker compose logs -f airflow-webserver airflow-scheduler
```

Stop the services with `docker compose down`. This preserves the Airflow metadata volume.

## Project files

- `main.py` — manual ETL entry point.
- `extract.py` — fetches gas-price data using `COLLECTAPI_KEY`.
- `transform.py` — prepares city-level data for loading.
- `load.py` — writes the `cities` table to PostgreSQL.
- `pipeline.py` — alternate ETL entry point using the shared modules.
- `dags/gas_prices_daily.py` — daily Airflow DAG.
- `docker-compose.yaml` and `Dockerfile` — local Airflow deployment.
- `.env.example` — environment variable template without credentials.
- `requirements.txt` — Python dependencies.
