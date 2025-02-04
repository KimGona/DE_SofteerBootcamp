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


## Data Loading
df = spark.read.parquet("./input/yellow_tripdata_2024-01.parquet")
rdd = df.rdd  # DataFrame을 RDD로 변환

# 데이터 개수 확인: 2,964,624
print(f"총 레코드 수: {rdd.count()}")

# RDD의 첫 번째 row 구조 확인
print(rdd.first())

# RDD 데이터 샘플 출력
print(rdd.take(5))

## Data cleaning
# 1️. None 값 제거
columns_to_check = ["fare_amount", "passenger_count", "trip_distance"]
rdd_filtered = rdd.filter(lambda row: all(row[col] is not None for col in columns_to_check))

# 2. 값 체크하여 필터링
rdd_filtered = rdd_filtered.filter(lambda row: row["fare_amount"] > 0) #운임 필터링
rdd_filtered = rdd_filtered.filter(lambda row: row["passenger_count"] > 0) # 승객 수 필터링
rdd_filtered = rdd_filtered.filter(lambda row: row["trip_distance"] > 0) # 운행 거리 필터링
rdd_filtered = rdd_filtered.filter(
    lambda row: row.tpep_pickup_datetime.year == 2024 and row.tpep_pickup_datetime.month == 1
)
## Data transformation

# 여기에도 캐시 사용하면 빨라진다.
#rdd_filtered.cache()

## Data Aggregation

# 총 트립 수
total_trips = rdd_filtered.count()
print(f"total number of trips: {total_trips}")

# 총 수익
total_revenue = rdd_filtered.map(lambda row: row["total_amount"]).sum()
print(f"total revenue: ${total_revenue:.2f}")

# 평균 이동 거리
avg_trip_distance = rdd_filtered.map(lambda row: row["trip_distance"]).mean()
print(f"Average trip distance: {avg_trip_distance:.2f} miles")

# 일별 트립 수
trips_per_day = (
    rdd_filtered.map(lambda row: (row["tpep_pickup_datetime"].date(), 1))
               .reduceByKey(lambda a, b: a + b)
               .collect()
)

print("Numebr of trips per day:")
for date, count in sorted(trips_per_day):
    print(f"{date}: {count} 건")

# 일별 총 수익
revenue_per_day = (
    rdd_filtered.map(lambda row: (row["tpep_pickup_datetime"].date(), row["total_amount"]))
               .reduceByKey(lambda a, b: a + b)
               .collect()
)

print("Total revenue per day:")
for date, revenue in sorted(revenue_per_day):
    print(f"{date}: ${revenue:.2f}")


# RDD → DataFrame 변환
df_filtered = spark.createDataFrame(rdd_filtered)

# 저장 경로 설정
cleaned_parquet_path = "./output/yellow_tripdata_2024-01.parquet"
cleaned_csv_path = "./output/yellow_tripdata_2024-01.csv"

# 데이터 저장
df_filtered.repartition(20).write.mode("overwrite").parquet(cleaned_parquet_path)
df_filtered.repartition(20).write.mode("overwrite").csv(cleaned_csv_path, header=True)

print("데이터 정제 완료, 저장 경로:")
print(f" - Parquet: {cleaned_parquet_path}")
print(f" - CSV: {cleaned_csv_path}")

time.sleep(1000)  # Spark UI 유지
spark.stop()