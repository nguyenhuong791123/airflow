#!/bin/sh

CMD="airflow scheduler"

cat /root/airflow.cfg > $AIRFLOW_HOME/airflow.cfg
airflow initdb
airflow upgradedb

exec $CMD