from pyspark.sql.functions import col, to_timestamp
from pyspark.sql import functions as F

# Parquet 파일 읽기
df_parquet = spark.read.parquet('data/fhvhv_tripdata_2023-12.parquet')

# 시간 포맷 변환 (예: 'pickup_datetime'을 Timestamp로 변환)
df_cleaned = df_cleaned.withColumn("pickup_datetime", to_timestamp("pickup_datetime", "yyyy-MM-dd HH:mm:ss"))

# 비정상적인 데이터 필터링 (예: 음수의 여행 거리 및 시간)
df_cleaned = df_cleaned.filter((col("trip_duration") > 0) & (col("trip_distance") > 0))

print(df_cleaned)

# # 하차시간 - 탑승시간을 초 단위 계산: 평균 여행 시간 분석을 위해
# # 위 값을 분단위로 변환: 분 단위 시각화로 가독성 향상을 위해
# # 탑승시간에서 시간만 추출: peak hour분석용
# df = df.withColumn("trip_duration_sec",
#                    unix_timestamp(col("tpep_dropoff_datetime")) - unix_timestamp(col("tpep_pickup_datetime"))
#                   )
# df = df.filter((col("trip_duration_sec") < 18000)) # 비정상 데이터 제거 - 이동이 5시간 이상인 데이터 제거
# df = df.withColumn("trip_duration_min", col("trip_duration_sec") / 60.0)
# df = df.withColumn("pickup_hour", hour("tpep_pickup_datetime"))