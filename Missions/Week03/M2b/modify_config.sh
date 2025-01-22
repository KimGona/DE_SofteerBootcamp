#!/bin/bash

# Check if a directory path is passed
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <Hadoop configuration directory path>"
  exit 1
fi

CONFIG_DIR="$1"

# Ensure the directory exists
if [ ! -d "$CONFIG_DIR" ]; then
  echo "Error: Directory $CONFIG_DIR does not exist."
  exit 1
fi

# Backup the original files
BACKUP_DIR="${CONFIG_DIR}/backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp "$CONFIG_DIR"/*.xml "$BACKUP_DIR"
echo "Backup completed. Original files are saved in $BACKUP_DIR."

# Function to modify an XML file
modify_xml() {
  FILE="$1"
  PROPERTY="$2"
  VALUE="$3"

  if grep -q "<name>$PROPERTY</name>" "$FILE"; then
    sed -i.bak "/<name>$PROPERTY<\/name>/!b;n;c<value>$VALUE</value>" "$FILE"
    echo "Updated $PROPERTY to $VALUE in $FILE"
  else
    echo "Error: Property $PROPERTY not found in $FILE."
  fi
}

# Modify core-site.xml
CORE_SITE="$CONFIG_DIR/core-site.xml"
modify_xml "$CORE_SITE" "fs.defaultFS" "hdfs://namenode:9000"
modify_xml "$CORE_SITE" "hadoop.tmp.dir" "/hadoop/tmp"
modify_xml "$CORE_SITE" "io.file.buffer.size" "131072"

# Modify hdfs-site.xml
HDFS_SITE="$CONFIG_DIR/hdfs-site.xml"
modify_xml "$HDFS_SITE" "dfs.replication" "2"
modify_xml "$HDFS_SITE" "dfs.blocksize" "134217728"
modify_xml "$HDFS_SITE" "dfs.namenode.name.dir" "/hadoop/dfs/name"

# Modify mapred-site.xml
MAPRED_SITE="$CONFIG_DIR/mapred-site.xml"
modify_xml "$MAPRED_SITE" "mapreduce.framework.name" "yarn"
modify_xml "$MAPRED_SITE" "mapreduce.jobhistory.address" "namenode:10020"
modify_xml "$MAPRED_SITE" "mapreduce.task.io.sort.mb" "256"

# Modify yarn-site.xml
YARN_SITE="$CONFIG_DIR/yarn-site.xml"
modify_xml "$YARN_SITE" "yarn.resourcemanager.address" "namenode:8032"
modify_xml "$YARN_SITE" "yarn.nodemanager.resource.memory-mb" "8192"
modify_xml "$YARN_SITE" "yarn.scheduler.minimum-allocation-mb" "1024"

# Restart Hadoop services
echo "Restarting Hadoop services..."
stop-all.sh
start-all.sh

echo "Configuration modification completed successfully."
