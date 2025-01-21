#!/bin/bash

# Function to backup and modify a file
modify_config_file() {
    FILE=$1
    BACKUP_FILE="$FILE.bak"
    echo "Backing up $FILE..."
    cp $FILE $BACKUP_FILE

    echo "Modifying $FILE..."
    
    # Modify the settings using sed
    case $FILE in
        "core-site.xml")
            sed -i '' 's|<name>fs.defaultFS</name><value>.*</value>|<name>fs.defaultFS</name><value>hdfs://namenode:9000</value>|' $FILE
            sed -i '' 's|<name>hadoop.tmp.dir</name><value>.*</value>|<name>hadoop.tmp.dir</name><value>/hadoop/tmp</value>|' $FILE
            sed -i '' 's|<name>io.file.buffer.size</name><value>.*</value>|<name>io.file.buffer.size</name><value>131072</value>|' $FILE
            ;;
        "hdfs-site.xml")
            sed -i '' 's|<name>dfs.replication</name><value>.*</value>|<name>dfs.replication</name><value>2</value>|' $FILE
            sed -i '' 's|<name>dfs.blocksize</name><value>.*</value>|<name>dfs.blocksize</name><value>134217728</value>|' $FILE
            sed -i '' 's|<name>dfs.namenode.name.dir</name><value>.*</value>|<name>dfs.namenode.name.dir</name><value>/hadoop/dfs/name</value>|' $FILE
            ;;
        "mapred-site.xml")
            sed -i '' 's|<name>mapreduce.framework.name</name><value>.*</value>|<name>mapreduce.framework.name</name><value>yarn</value>|' $FILE
            sed -i '' 's|<name>mapreduce.jobhistory.address</name><value>.*</value>|<name>mapreduce.jobhistory.address</name><value>namenode:10020</value>|' $FILE
            sed -i '' 's|<name>mapreduce.task.io.sort.mb</name><value>.*</value>|<name>mapreduce.task.io.sort.mb</name><value>256</value>|' $FILE
            ;;
        "yarn-site.xml")
            sed -i '' 's|<name>yarn.resourcemanager.address</name><value>.*</value>|<name>yarn.resourcemanager.address</name><value>namenode:8032</value>|' $FILE
            sed -i '' 's|<name>yarn.nodemanager.resource.memory-mb</name><value>.*</value>|<name>yarn.nodemanager.resource.memory-mb</name><value>8192</value>|' $FILE
            sed -i '' 's|<name>yarn.scheduler.minimum-allocation-mb</name><value>.*</value>|<name>yarn.scheduler.minimum-allocation-mb</name><value>1024</value>|' $FILE
            ;;
        *)
            echo "Unknown file: $FILE"
            exit 1
            ;;
    esac
}

# Main script logic
CONFIG_DIR=$1
if [ -z "$CONFIG_DIR" ]; then
    echo "Usage: $0 <path_to_hadoop_config_directory>"
    exit 1
fi

cd $CONFIG_DIR

# Modify each configuration file
for config_file in core-site.xml hdfs-site.xml mapred-site.xml yarn-site.xml; do
    if [ -f $config_file ]; then
        modify_config_file $config_file
    else
        echo "Configuration file $config_file not found."
    fi
done

# Restart Hadoop services
#echo $HADOOP_HOME
#cat $HADOOP_HOME/sbin/stop-dfs.sh

echo "Stopping Hadoop DFS..."
$HADOOP_HOME/sbin/stop-dfs.sh
echo "Stopping YARN..."
$HADOOP_HOME/sbin/stop-yarn.sh
echo "Starting Hadoop DFS..."
$HADOOP_HOME/sbin/start-dfs.sh
echo "Starting YARN..."
$HADOOP_HOME/sbin/start-yarn.sh

echo "Configuration changes applied and services restarted."
