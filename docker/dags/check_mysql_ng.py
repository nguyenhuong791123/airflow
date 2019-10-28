import logging
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.hooks.mysql_hook import MySqlHook
from airflow.utils.email import send_email

default_args = {
    'owner': 'SC APP'
    ,'start_date': datetime(2019, 6, 12, 15, 00, 00)
    ,'email': ['nguyenhuong791123@gmail.com']
    ,'email_on_failure': False
    ,'email_on_retry': False,
}

dag = DAG('airflow_dags', default_args=default_args, schedule_interval='0/1 * * * *')

def send(content):
    EMAIL_CONTENT = """

    <ul>
        <li>Instatnce key: %s</li>
        <li>Owner: %s</li>
        <li>Host: %s</li>
        <li>Context: %s</li>
    </ul>

    """ % ("{{ task_instance_key_str }}", "{{ task.owner}}", "{{ ti.hostname }}", content)
    print(EMAIL_CONTENT)
    send_email(to=['nguyenhuong791123@gmail.com'],
        subject='send_mail',
        html_content=EMAIL_CONTENT)
    # send = EmailOperator (
    #     dag=dag,
    #     task_id="send_mail",
    #     to=["nguyenhuong791123@gmail.com"],
    #     subject="バッチ成功: 実行日 {{ ds }}",
    #     html_content=EMAIL_CONTENT)

class ReturningMySqlOperator(MySqlOperator):
    def execute(self, context):
        self.log.info('Executing: %s', self.sql)
        hook = MySqlHook(mysql_conn_id=self.mysql_conn_id,
                         schema=self.database)
        return hook.get_records(
            self.sql,
            parameters=self.parameters)

t1 = ReturningMySqlOperator(
    task_id='basic_mysql',
    mysql_conn_id='airflow_db',
    sql="select * from dag",
    dag=dag)

def get_records(**kwargs):
    ti = kwargs['ti']
    xcom = ti.xcom_pull(task_ids='basic_mysql')
    for x in xcom:
        # print(x)
        send(x)

    # string_to_print = 'Value in xcom is: {}'.format(xcom)
    # Get data in your logs
    # logging.info(string_to_print)

t2 = PythonOperator(
    task_id='日本語',
    provide_context=True,
    python_callable=get_records,
    dag=dag)

t1 >> t2