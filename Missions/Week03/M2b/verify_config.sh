#!/bin/bash

# Function to verify Hadoop settings using the getconf command
verify_config() {
    KEY=$1
    EXPECTED_VALUE=$2
    COMMAND=$3

    echo "Verifying $KEY..."
    VALUE=$($COMMAND -confKey $KEY)
    if [ "$VALUE" == "$EXPECTED_VALUE" ]; then
        echo "PASS: $COMMAND -confKey $KEY -> $VALUE"
    else
        echo "FAIL: $COMMAND -confKey $KEY -> $VALUE (expected $EXPECTED_VALUE)"
    fi
}

# Verify configuration settings
echo "Verifying configuration changes..."

# Check for core-site.xml settings
verify_config "fs.defaultFS" "hdfs://namenode:9000" "hdfs getconf"
verify_config "hadoop.tmp.dir" "/hadoop/tmp" "hdfs getconf"
verify_config "io.file.buffer.size" "131072" "hdfs getconf"

# Check for hdfs-site.xml settings
verify_config "dfs.replication" "2" "hdfs getconf"
verify_config "dfs.blocksize" "134217728" "hdfs getconf"
verify_config "dfs.namenode.name.dir" "/hadoop/dfs/name" "hdfs getconf"

# Check for mapred-site.xml settings
verify_config "mapreduce.framework.name" "yarn" "hadoop getconf"
verify_config "mapreduce.jobhistory.address" "namenode:10020" "hadoop getconf"
verify_config "mapreduce.task.io.sort.mb" "256" "hadoop getconf"

# Check for yarn-site.xml settings
verify_config "yarn.resourcemanager.address" "namenode:8032" "yarn getconf"
verify_config "yarn.nodemanager.resource.memory-mb" "8192" "yarn getconf"
verify_config "yarn.scheduler.minimum-allocation-mb" "1024" "yarn getconf"

# Verify replication factor by creating a test file
echo "Creating test file in HDFS..."
hadoop fs -touchz /user/test/testfile
REPLICATION=$(hdfs dfs -stat %r /user/test/testfile)
if [ "$REPLICATION" == "2" ]; then
    echo "PASS: Replication factor is $REPLICATION"
else
    echo "FAIL: Replication factor is $REPLICATION (expected 2)"
fi

echo "Verification completed."
