

Docker 이미지 빌드:
docker-compose build

컨테이너 실행:
docker-compose up -d

마스터 노드에 접속:
docker exec -it hadoop-master bash

- service ssh status로 ssh 연결되어 있는지 확인하기
- sudo service ssh start

6. 하둡 서비스 시작
- start-dfs.sh

- jps #서비스 상태 확인
(NameNode, SecondaryNameNode, DataNode, 그리고 ResourceManager 나오는지 확인)

디렉토리 생성
설정된 NameNode 저장소 디렉토리가 없거나 잘못되었을 수 있습니다. 디렉토리를 수동으로 생성하고 올바른 권한을 설정하세요:

sudo mkdir -p /usr/local/hadoop/data/namenode
sudo chown -R hadoop:hadoop /usr/local/hadoop/data/namenode
sudo mkdir -p /usr/local/hadoop/data/datanode
sudo chown -R hadoop:hadoop /usr/local/hadoop/data/datanode

$HADOOP_HOME/bin/hdfs namenode -format # 처음에 네임노드 포맷 확인(기존에 저장된 데이터 있으면 삭제됨)


## 하둡 master

2. HDFS 상태 테스트
2.1. NameNode 상태 확인
NameNode의 웹 UI로 접속해 상태를 확인합니다.

http://<master-ip>:9870
2.2. DataNode 상태 확인
CLI를 통해 HDFS 상태를 확인합니다.

docker exec -it master bash -c "hdfs dfsadmin -report"

예상 결과:
Configured Capacity와 DFS Remaining 값을 확인합니다.
적어도 하나의 DataNode가 Live nodes 섹션에 표시되어야 합니다.

1. NameNode 실행 문제
NameNode가 시작되지 않은 상태이므로 직접 실행하여 오류를 확인합니다.
$HADOOP_HOME/bin/hdfs namenode


## 하둡 worker

hadoop@worker:~$ $HADOOP_HOME/sbin/yarn-daemon.sh start nodemanager
WARNING: Use of this script to start YARN daemons is deprecated.
WARNING: Attempting to execute replacement "yarn --daemon start" instead.
hadoop@worker:~$ jps
547 SecondaryNameNode
730 NodeManager
858 Jps

hdfs dfsadmin -report #live datanode 한 개 이상 있어야 한다.


## HDFS operation 확인
HDFS 디렉토리 확인
hdfs dfs -ls /

HDFS 폴더 생성
hdfs dfs -mkdir /user/test

파일 생성
echo 'Hello, Hadoop!' > /tmp/testfile.txt

HDFS에 파일 업로드
hdfs dfs -put /tmp/testfile.txt /user/test

업로드된 파일 확인
hdfs dfs -ls /user/test

HDFS에 저장된 파일 다운로드
hdfs dfs -get /user/test/testfile.txt /tmp/test_file_downloaded.txt

다운로드된 파일 확인
cat /tmp/test_file_downloaded.txt



## yarn 작동하는지 테스트 코드 실행(마스터에서)
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar pi 16 1000 

결과: 아래처럼 나온다
Estimated value of Pi is 3.14250000000000000000

컨테이너 종료:
docker-compose down

