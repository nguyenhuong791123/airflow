#!/bin/sh

CMD="airflow worker"

cat /root/airflow.cfg > $AIRFLOW_HOME/airflow.cfg

exec $CMD