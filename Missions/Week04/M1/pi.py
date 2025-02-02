import sys
from random import random
from operator import add

from pyspark.sql import SparkSession
from pyspark.sql import Row

def f(_: int) -> float:
    x = random() * 2 - 1
    y = random() * 2 - 1
    return 1 if x ** 2 + y ** 2 <= 1 else 0

if __name__ == "__main__":

    spark = SparkSession\
        .builder\
        .appName("PythonPi")\
        .getOrCreate()

    #partitions = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    #n = 100000 * partitions

    n = 1000000 # 100만 개

    count = spark.sparkContext.parallelize(range(n)).map(f).reduce(lambda a, b: a + b)
    pi = 4.0 * count / n
    print("Pi is roughly %f" % pi)

    # 결과를 DataFrame으로 변환
    df = spark.createDataFrame([(pi,)], ["Estimated Pi"])

    #result = Row(num_samples=n, pi_estimate=pi)
    #df = spark.createDataFrame([result])

    # CSV로 저장
    output_path = "/opt/spark/output/pi_estimate.csv"  # 저장할 경로
    df.write.mode("overwrite").csv(output_path, header=True)
    #df.coalesce(1).write.mode("overwrite").format("csv").option("header", "true").save(output_path)
    #df.write.csv(output_path, mode='overwrite', header = True)
    #df.coalesce(1).write.csv(output_path, mode="overwrite") csv 밑에 _SUCCESS 생김
    #df.write.mode("overwrite").csv(output_path, header=True) csv 밑에 _SUCCESS 생김

    spark.stop()   
