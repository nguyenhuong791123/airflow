from airflow import DAG
#Please import from 'airflow.operators.[operator_module]' instead. Support for direct imports will be dropped entirely in Airflow 2.0.
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.email_operator import EmailOperator

default_args = {
    'owner': 'Airflow'
    ,'start_date': datetime(2016, 6, 12, 15, 00, 00)
    ,'email': ['nguyenhuong791123@gmail.com']
    ,'email_on_failure': False
    ,'email_on_retry': False,
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


EMAIL_CONTENT = """

<ul>
    <li>Instatnce key: %s</li>
    <li>Owner: %s</li>
    <li>Host: %s</li>
</ul>

""" % ("{{ task_instance_key_str }}", "{{ task.owner}}", "{{ ti.hostname }}",)
send_mail = EmailOperator (
    dag=dag,
    task_id="send_mail",
    to=["nguyenhuong791123@gmail.com"],
    subject="バッチ成功: 実行日 {{ ds }}",
    html_content=EMAIL_CONTENT)

task1.set_downstream(task2)
send_mail.set_upstream(task2)
