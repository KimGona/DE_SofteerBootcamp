from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, unix_timestamp, expr, hour
import time
from pyspark.sql.functions import year, month

# Spark 세션 생성 - Java Heap space 부족 방지
spark = SparkSession.builder \
    .appName("NYC_Taxi_Data_Analysis") \
    .config("spark.driver.memory", "4g") \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.extraJavaOptions", "--add-opens=java.base/javax.security.auth=ALL-UNNAMED") \
    .config("spark.driver.extraJavaOptions", "--add-opens=java.base/javax.security.auth=ALL-UNNAMED") \
    .getOrCreate()


## Data Loading
df = spark.read.parquet("./input/yellow_tripdata_2024-01.parquet")

# 데이터 개수 확인: 2,964,624개
print(f"총 레코드 수: {df.count()}")

# 데이터 스키마 확인
df.printSchema()

# 데이터 조회
df.show(5)

# 데이터 정제
# 탑승시간과 하차시간을 timestamp형식으로 변환
# 데이터 전송여부를 이진값으로 변환(Y - 1, N - 0)
df = df.withColumn("tpep_pickup_datetime", col("tpep_pickup_datetime").cast("timestamp")) \
       .withColumn("tpep_dropoff_datetime", col("tpep_dropoff_datetime").cast("timestamp")) \
       .withColumn("store_and_fwd_flag", when(col("store_and_fwd_flag") == "Y", 1).otherwise(0))

# 승차지점 지역ID, 하차지점 지역ID, 이동거리, 총요금, 승객 수 등에 결측치가 있는 행 삭제
df = df.dropna(subset=["PULocationID", "DOLocationID", "trip_distance", "total_amount","fare_amount", "passenger_count"])

df = df.filter((col("trip_distance") > 0) & (col("trip_distance") < 300))  # 운행거리 0~300 해당하는 값만 남기기
df = df.filter((col("total_amount") > 0)) # 운행 요금 0 넘는 값만 남기기
df = df.filter(col("passenger_count") > 0) #승객 수 1명 이상인 값만 남기기

# 날짜가 24년 1월인 것만 남기기
df = df.filter(
    (year(col("tpep_pickup_datetime")) == 2024) & 
    (month(col("tpep_pickup_datetime")) == 1)
)

# 데이터 개수 확인 2,723,989
print(f"총 레코드 수: {df.count()}")


time.sleep(600)  # Spark UI 유지
spark.stop()