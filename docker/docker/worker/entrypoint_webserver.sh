#!/bin/sh

CMD="airflow webserver"

cat /root/airflow.cfg > $AIRFLOW_HOME/airflow.cfg

exec $CMD