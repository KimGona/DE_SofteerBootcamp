#!/bin/bash

# Format HDFS only on the master node
if [ "$HOSTNAME" == "master" ]; then
  if [ ! -d "/usr/local/hadoop/data/namenode" ]; then
    $HADOOP_HOME/bin/hdfs namenode -format -force
  fi
  $HADOOP_HOME/sbin/start-dfs.sh
  $HADOOP_HOME/sbin/start-yarn.sh
else
  $HADOOP_HOME/bin/hdfs datanode
fi

# Keep container running
tail -f /dev/null