from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, unix_timestamp, expr, hour
import time


# Spark 세션 생성 - Java Heap space 부족 방지
spark = SparkSession.builder \
    .appName("NYC_Taxi_Data_Analysis") \
    .config("spark.driver.memory", "4g") \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.extraJavaOptions", "--add-opens=java.base/javax.security.auth=ALL-UNNAMED") \
    .config("spark.driver.extraJavaOptions", "--add-opens=java.base/javax.security.auth=ALL-UNNAMED") \
    .getOrCreate()

# 데이터 병합 - 24년 1월 ~ 24년 11월 그린 택시 데이터
# Spark는 경로에 여러 Parquet 파일이 존재할 경우 자동으로 병합한다. 
df = spark.read.parquet("./data/green_tripdata_*.parquet")

# 데이터 개수 확인 - 총 606,224개
print(f"총 레코드 수: {df.count()}")

# 데이터 스키마 확인
df.printSchema()

# 데이터 샘플 조회
df.show(5)

# 데이터 정제
# 탑승시간과 하차시간을 timestamp형식으로 변환
# 데이터 전송여부를 이진값으로 변환(Y - 1, N - 0)
df = df.withColumn("lpep_pickup_datetime", col("lpep_pickup_datetime").cast("timestamp")) \
       .withColumn("lpep_dropoff_datetime", col("lpep_dropoff_datetime").cast("timestamp")) \
       .withColumn("store_and_fwd_flag", when(col("store_and_fwd_flag") == "Y", 1).otherwise(0))

# 승차지점 지역ID, 하차지점 지역ID, 이동거리, 총요금에 결측치가 있는 행 삭제
df = df.dropna(subset=["PULocationID", "DOLocationID", "trip_distance", "total_amount"])

# [비정상 데이터 제거]
# 거리가 0 이하거나 200마일 이상인 데이터 삭제
# 총 요금이 0 이하인 데이터 삭제
# 승객이 0명인 데이터 삭제
df = df.filter((col("trip_distance") > 0) & (col("trip_distance") < 200))  
df = df.filter((col("total_amount") > 0))  
# df_cleaned = df.filter(~((col("fare_amount") > 0) & (col("payment_type") == 3))) 기본 요금이 0보다 큰데 결제 유형이 무료 승차인 데이터 삭제
df = df.filter(col("passenger_count") > 0) 



# 정제한 데이터 저장
cleaned_parquet_path = "./output/green_tripdata_2024.parquet"
cleaned_csv_path = "./output/green_tripdata_2024.csv"

df = df.repartition(20)  # 20개의 파티션으로 나눠서 저장
df.write.mode("overwrite").parquet(cleaned_parquet_path)
df.write.mode("overwrite").csv(cleaned_csv_path, header=True)

print("데이터 정제 완료, 저장 경로:")
print(f" - Parquet: {cleaned_parquet_path}")
print(f" - CSV: {cleaned_csv_path}")

#time.sleep(600)  # Spark UI 유지
spark.stop()