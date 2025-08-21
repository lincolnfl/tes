from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import json
from airflow.models import Variable
from elasticsearch import Elasticsearch

logstash_url = "http://logstash:5044/"
api_key = "xZRysV5GhtBQn8FNB_ddUzuiWJd6YYNsQUuIJE9D498"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 11, 3),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

def extract_data(**kwargs):
    try:
        response = requests.get("https://data.traffic.hereapi.com/v7/flow?in=circle:3.575953,98.621565;r=1000&locationReferencing=olr&apiKey=" + api_key)
        if response.status_code == 200:
            traffic_data = response.json()
            return traffic_data
        else:
            raise Exception("Failed to fetch data from the API.")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")

def transform_data(**kwargs):
    traffic_data = kwargs['ti'].xcom_pull(task_ids='extract_data')
    data = {
        "message": json.dumps(traffic_data)
    }
    return data

def load_data_to_logstash(**kwargs):
    data = kwargs['ti'].xcom_pull(task_ids='transform_data')

    # Send data to Logstash
    post_response = requests.post(logstash_url, json=data)
    if post_response.status_code != 200:
        raise Exception("Failed to send data to Logstash.")


dag = DAG(
    'traffic_data',
    default_args=default_args,
    schedule_interval=timedelta(minutes=1),  # Run the DAG every 1 minute
    catchup=False,
    max_active_runs=1,
)

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    provide_context=True,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data_to_logstash',
    python_callable=load_data_to_logstash,
    provide_context=True,
    dag=dag,
)

# Define task dependencies
extract_task >> transform_task >> load_task
