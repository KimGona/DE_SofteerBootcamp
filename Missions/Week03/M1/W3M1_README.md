# Week03 Mission1 실행 instruction

1. 하둡 로컬에 다운로드
- https://dlcdn.apache.org/hadoop/common/hadoop-3.4.0/
- hadoop-3.4.0.tar.gz 파일 다운로드 받기


2. 도커 이미지 빌드
- docker build -t hadoop-single .

3. 컨테이너 실행
- docker run -it --name single-cluster -p 9870:9870 -p 9000:9000 hadoop-single

4. 터미널에서 컨테이너 내부로 들어가기
- docker exec -it single-cluster bash

5. 컨테이너 내부에서 hdfs 초기화(처음에만 하기)
- hdfs namenode -format

6. 하둡 서비스 시작
- start-dfs.sh

- jps #서비스 상태 확인

- hdfs dfs -mkdir /user #폴더 생성


- hdfs dfs -ls /

- echo "Hello Hadoop" > sample.txt #파일 만들기

- hdfs dfs -put sample.txt /user/kga  #파일 업로드     

- hdfs dfs -ls /user/kga #파일 확인

- hdfs dfs -get /user/kga/sample.txt downloaded_sample.txt #파일 다운로드

- http://localhost:9870 실행해보기