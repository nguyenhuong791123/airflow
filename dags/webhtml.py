from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'vagrant',
    'start_date': datetime(2016, 6, 12, 15, 00, 00)
}

dag = DAG('airflow_logs', default_args=default_args, schedule_interval='0/1 * * * *')

task1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag)

task2 = BashOperator(
    task_id='print_hello-world',
    bash_command='echo "hello world!!"',
    dag=dag)

task1.set_downstream(task2)