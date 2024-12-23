from pyspark.sql.types import StructType, StringType, IntegerType
from pyspark.sql import SparkSession
from pyspark.sql.functions import split
from pyspark.sql import functions as F
from pyspark.sql.functions import lag, col, sum as F_sum
from pyspark.sql.functions import window
from pyspark.sql.functions import to_timestamp, to_date, lpad, concat, lit, from_unixtime
from pyspark.sql.window import Window

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("KafkaStreamProcessing") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()

# Kafka consumer configuration
kafka_params = {
    "kafka.bootstrap.servers": "localhost:9092",
    "startingOffsets": "earliest"
}

# Kafka topic
topic = "covid"
output_path = "./results"
checkpoint_path = "./checkpoint"

# Initialize Kafka consumer
# consumer = Consumer(kafka_params)
# consumer.subscribe([topic])

# Define JSON data schema
schema = StructType() \
    .add("date", StringType()) \
    .add("county", StringType()) \
    .add("state", StringType()) \
    .add("cases", IntegerType()) \
    .add("deaths", IntegerType())

# Read Kafka data stream and perform stream processing
# Creating a Streaming DataFrame to Read Data from Kafka
kafka_stream_df = spark.readStream.format("kafka") \
    .options(**kafka_params) \
    .option("subscribe", topic) \
    .load()

kafka_stream_df = kafka_stream_df.withColumn("date", split(split("value", ",")[0], ":")[1]) \
    .withColumn("county", split(split("value", ",")[1], ":")[1]) \
    .withColumn("state", split(split("value", ",")[2], ":")[1]) \
    .withColumn("cases", split(split("value", ",")[3], ":")[1]) \
    .withColumn("deaths", split(split("value", ",")[4], ":")[1])

kafka_stream_df = kafka_stream_df.withColumn("year", split("date", "/")[0]) \
    .withColumn("month", lpad(split("date", "/")[1], 2, "0")) \
    .withColumn("day", lpad(split("date", "/")[2], 2, "0")) \
    .withColumn("date", concat("year", lit("-"), "month", lit("-"), "day")) \
    .withColumn("timestamp", concat(lit("2024-04-01 00:"), "month", lit(":"), "day")) \
    .withColumn("timestamp", to_timestamp("timestamp", "yyyy-MM-dd HH:mm:ss"))

kafka_stream_df = kafka_stream_df.withColumn("cases", kafka_stream_df["cases"].cast("int")) \
    .withColumn("deaths", kafka_stream_df["deaths"].cast("int"))

# print Schema
kafka_stream_df.printSchema()

'''
# Streaming processing: Group by date and calculate the total number of cases and deaths
result_df = kafka_stream_df \
    .groupBy("timestamp") \
    .agg(sum("cases").alias("total_cases"), sum("deaths").alias("total_deaths")) \
'''

'''

'''

window_spec = Window.partitionBy("date").orderBy("timestamp")

result_df = kafka_stream_df \
    .withWatermark("timestamp", "60 seconds") \
    .groupBy("date") \
    .agg(F.sum("cases").alias("total_cases"), F.sum("deaths").alias("total_deaths"))

query = result_df \
    .writeStream \
    .outputMode('append') \
    .format("json") \
    .option("path", output_path) \
    .option("checkpointLocation", checkpoint_path) \
    .start()
'''
query = result_df \
    .writeStream \
    .outputMode('append') \
    .format("console") \
    .start()
'''
query.awaitTermination()

result_df2 = result_df \
    .withColumn("cases_diff", col("total_cases") - lag("total_cases", 1).over(window_spec)) \
    .withColumn("deaths_diff", col("total_deaths") - lag("total_deaths", 1).over(window_spec))

query2 = result_df \
    .writeStream \
    .outputMode('append') \
    .format("json") \
    .option("path", output_path) \
    .option("checkpointLocation", checkpoint_path) \
    .start()

query2.awaitTermination()
