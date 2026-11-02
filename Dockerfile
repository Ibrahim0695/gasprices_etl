FROM apache/airflow:slim-2.10.5-python3.11

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir \
    "apache-airflow==2.10.5" \
    apache-airflow-providers-fab \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.5/constraints-3.11.txt" \
    -r /requirements.txt
