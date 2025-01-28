#!/bin/bash

# Variables
MASTER_URL="spark://spark-master:7077"
APP_NAME="Pi Estimation"
SCRIPT_PATH="/opt/spark/jobs/pi.py"
NUM_SAMPLES=100000

# Submit Spark job
docker exec -it spark-master \
  bin/spark-submit \
  --master $MASTER_URL \
  --name "$APP_NAME" \
  $SCRIPT_PATH $NUM_SAMPLES
