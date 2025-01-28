from pyspark import SparkContext, SparkConf
import sys

if __name__ == "__main__":
    conf = SparkConf().setAppName("Pi Estimation")
    sc = SparkContext(conf=conf)

    # Number of samples
    num_samples = int(sys.argv[1]) if len(sys.argv) > 1 else 1000000

    def inside_circle(_):
        import random
        x, y = random.random(), random.random()
        return x**2 + y**2 < 1

    count = sc.parallelize(range(0, num_samples)).filter(inside_circle).count()
    pi = 4.0 * count / num_samples

    print(f"Estimated value of π is {pi}")
    sc.stop()
