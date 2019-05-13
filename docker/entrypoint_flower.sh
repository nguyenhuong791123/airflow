#!/bin/sh

CMD="airflow flower"

cat /root/airflow.cfg > $AIRFLOW_HOME/airflow.cfg

exec $CMD