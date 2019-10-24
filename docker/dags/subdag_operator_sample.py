# -*- coding: utf-8 -*-
import airflow
from airflow.executors.celery_executor import CeleryExecutor
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator

def get_id_list():
    """ idのリストを返す. 例のためとりあえず簡単に0〜99. """
    return range(100)

def subdag(parent_dag_name, child_dag_name, args):
    """ 各idに対して実行する処理フローを記述したDAGを返す """
    sub_dag = DAG(dag_id="{}.{}".format(parent_dag_name, child_dag_name), default_args=args, schedule_interval="@once")
    for id in get_id_list():
        t1 = BashOperator(
            task_id='{}-task-1'.format(id),
            bash_command='echo task1: {}'.format(id),
            default_args=args,
            dag=sub_dag,
        )
        t2 = BashOperator(
            task_id='{}-task-2'.format(id),
            bash_command='echo task2: {}'.format(id),
            default_args=args,
            dag=sub_dag,
        )
        t1 >> t2
    return sub_dag 

DAG_NAME = 'subdag_operator_sample'
args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
    'provide_context': True,
}

dag = DAG(dag_id='subdag_operator_sample', default_args=args, schedule_interval='@once')

t1 = DummyOperator(
    task_id='start',
    default_args=args,
    dag=dag,
)

t2 = SubDagOperator(
    task_id='subdag',
    executor=CeleryExecutor(),
    subdag=subdag(DAG_NAME, 'subdag', args),
    default_args=args,
    dag=dag,
)

t1 >> t2