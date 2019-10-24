# -*- coding: utf-8 -*-
import airflow
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.api.common.experimental.trigger_dag import trigger_dag
from airflow.utils import timezone
import json

def get_id_list():
    """ idのリストを返す. 例のためとりあえず簡単に0〜99. """
    return range(100)

def trigger(**kwargs):
    dag_id = kwargs['dag_id']  # triggerするDAG idを引数から取得
    execution_date = kwargs['ti'].execution_date.isoformat()
    for id in get_id_list():
        run_id = 'trig__{}_{}'.format(id, execution_date)
        trigger_dag(dag_id=dag_id,
                    run_id=run_id,
                    conf=json.dumps({'id': id}),
                    execution_date=None,
                    replace_microseconds=False)

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
    'provide_context': True,
}

###
### TriggerするDAGの定義
###
DAG_NAME = 'trigger_dag_sample'
dag = DAG(
    dag_id=DAG_NAME,
    default_args=args,
    schedule_interval="@once",
)

t1 = DummyOperator(
    task_id='start',
    default_args=args,
    dag=dag,
)

t2 = PythonOperator(
    task_id='trigger_account_dag',
    python_callable=trigger,
    op_kwargs={'dag_id': 'triggered_dag_sample'},
    default_args=args,
    dag=dag,
)
t1 >> t2

###
### triggerされるDAGの定義
###
sub_dag = DAG(
    dag_id='triggered_dag_sample',
    default_args=args,
    schedule_interval='@once',
)

command_template_1 = "echo task1: {{ dag_run.conf['id'] }}"
command_template_2 = "echo task2: {{ dag_run.conf['id'] }}"

t1 = BashOperator(
    task_id='task-1',
    bash_command=command_template_1,
    default_args=args,
    dag=sub_dag,
)
t2 = BashOperator(
    task_id='task-2',
    bash_command=command_template_2,
    default_args=args,
    dag=sub_dag,
)
t1 >> t2