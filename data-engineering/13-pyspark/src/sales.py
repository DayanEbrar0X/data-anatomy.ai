from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (SparkSession.builder.master("local[4]")
         .config("spark.ui.enabled", "false")
         .getOrCreate())
spark.sparkContext.setLogLevel("ERROR")

sales = (spark.range(100_000_000, numPartitions=4)
    .withColumn("store", F.col("id") % 50)
    .withColumn("amt", F.abs(F.hash("id")) % 500))
print("partitions:", sales.rdd.getNumPartitions())

big = sales.filter(F.col("amt") >= 100)
top = (big.groupBy("store")
          .agg(F.sum("amt").alias("revenue"))
          .orderBy(F.desc("revenue")))
print("plan built, nothing ran yet")
rows = top.take(3)                     # action
for r in rows:
    print(f"store {r.store:>2}: ${r.revenue:,}")
print("top store:", rows[0].store)
