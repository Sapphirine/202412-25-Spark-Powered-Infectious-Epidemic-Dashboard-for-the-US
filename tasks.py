from pyspark import SparkConf, SparkContext
from pyspark.sql import Row
from pyspark.sql.types import *
from pyspark.sql import SparkSession
from datetime import datetime
import pyspark.sql.functions as func
from pyspark.sql.functions import col, lag, lit
from pyspark.sql.window import Window
from pyspark.sql.functions import avg, stddev
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.sql.functions import datediff, to_date, expr, round
from pyspark.ml.regression import DecisionTreeRegressor

output_path = "F:\\Columbia\\24 Fall\\EECS6893 Big Data Analytics\\Project\\StreamProcessing\\results\\"

# Main:
spark = SparkSession.builder \
        .appName("test") \
        .config(conf = SparkConf())\
        .config("spark.driver.memory", "4g") \
        .config("spark.executor.memory", "4g") \
        .getOrCreate()

# Get the current Spark config
conf = SparkConf()
print(conf.get("spark.driver.memory"))
print(conf.get("spark.executor.memory"))


fields = [
        StructField("date", DateType(),False),
        StructField("county", StringType(),False),
        StructField("state", StringType(),False),
        StructField("cases", IntegerType(),False),
        StructField("deaths", IntegerType(),False),
]
schema = StructType(fields)

rdd0 = spark.sparkContext.textFile("us-counties-max-new.txt")
rdd1 = rdd0.map(lambda x:x.split("\t")).map(lambda p: Row(datetime.strptime(p[0], "%Y-%m-%d"), p[1], p[2], int(p[3]), int(p[4])))

schemaUsInfo = spark.createDataFrame(rdd1, schema)

schemaUsInfo.createOrReplaceTempView("usInfo")

# 1. Cumulative total cases and deaths based on days
df = schemaUsInfo.groupBy("date").agg(func.sum("cases"),func.sum("deaths")).sort(schemaUsInfo["date"].asc())


df1 = df.withColumnRenamed("sum(cases)", "cases").withColumnRenamed("sum(deaths)", "deaths")
# df1.repartition(1).write.json(output_path+"result1.json")


# TempView
df1.createOrReplaceTempView("ustotal")


# 2. New cases and deaths based on days
df2 = spark.sql("select t1.date,t1.cases-t2.cases as caseIncrease"
                ",t1.deaths-t2.deaths as deathIncrease from ustotal "
                "t1,ustotal t2 where t1.date = date_add(t2.date,1)")
df2.sort(df2["date"].asc()).repartition(1).write.json(output_path+"result2.json")
# df2.sort(df2["date"].asc())


# 3. Total cases, deaths and death rate based on states
df3 = spark.sql("select date,state,sum(cases) as totalCases,sum(deaths) as totalDeaths,round(sum(deaths)/sum(cases),4) "
                "as deathRate from usInfo  where date = to_date('2022-05-13','yyyy-MM-dd') group by date,state")

df3.sort(df3["totalCases"].desc()).repartition(1).write.json(output_path+"result3.json")

df3.createOrReplaceTempView("eachStateInfo")

# 4. First 10 states with the most cases
df4 = spark.sql("select date,state,totalCases from eachStateInfo  order by totalCases desc limit 10")
df4.repartition(1).write.json(output_path+"result4.json")

# 5. First 10 states with the most deaths
df5 = spark.sql("select date,state,totalDeaths from eachStateInfo  order by totalDeaths desc limit 10")
df5.repartition(1).write.json(output_path+"result5.json")

# 6. First 10 states with the least cases
df6 = spark.sql("select date,state,totalCases from eachStateInfo  order by totalCases asc limit 10")
df6.repartition(1).write.json(output_path+"result6.json")

# 7. First 10 states with the least deaths
df7 = spark.sql("select date,state,totalDeaths from eachStateInfo  order by totalDeaths asc limit 10")
df7.repartition(1).write.json(output_path+"result7.json")

# 8. Total Death Rate
df8 = spark.sql("select 1 as sign,date,'USA' as state,round(sum(totalDeaths)/sum(totalCases),4) as deathRate from "
                "eachStateInfo group by date union select 2 as sign,date,state,deathRate from eachStateInfo").cache()
df8.sort(df8["sign"].asc(),df8["deathRate"].desc()).repartition(1).write.json(output_path+"result8.json")


# 9. Weird behavior abruptly increase or decrease
# Calculate Z-score
df9 = df2.withColumn("caseZscore", (col("caseIncrease") - avg("caseIncrease").over(Window.partitionBy().orderBy("date")
        .rowsBetween(-7, 0))) / stddev("caseIncrease").over(Window.partitionBy().orderBy("date").rowsBetween(-7, 0)))
df9 = df9.withColumn("deathZscore", (col("deathIncrease") - avg("deathIncrease").over(Window.partitionBy().orderBy("date")
        .rowsBetween(-7, 0))) / stddev("deathIncrease").over(Window.partitionBy().orderBy("date").rowsBetween(-7, 0)))

# abnormal
df9 = df9.withColumn("abnormalIncrease", (col("caseZscore") > 2) | (col("deathZscore") > 2))
df9 = df9.withColumn("abnormalDecrease", (col("caseZscore") < -2) | (col("deathZscore") < -2))


df9.select("date", "caseIncrease", "deathIncrease", "abnormalIncrease", "abnormalDecrease") \
   .sort("date") \
   .repartition(1) \
   .write \
   .json(output_path + "result9.json")

# 10. Simple Prediction
reference_date = "2020-01-01"
df10 = df1.filter((col("date") >= to_date(lit(reference_date))) & (col("date") <= to_date(lit("2022-04-15"))) )

reference_date_D = to_date(lit(reference_date))

df10 = df10.withColumn("days_since_reference", datediff("date", reference_date_D))

vector_assembler = VectorAssembler(inputCols=["days_since_reference"], outputCol="features")
df10 = vector_assembler.transform(df10)

# linear regression
lr_cases = LinearRegression(featuresCol="features", labelCol="cases", predictionCol="predicted_cases", regParam=0.1
                            , elasticNetParam=0.5)

lr_deaths = LinearRegression(featuresCol="features", labelCol="deaths", predictionCol="predicted_deaths", regParam=0.1
                             , elasticNetParam=0.5)


# train
model_cases = lr_cases.fit(df10)
model_deaths = lr_deaths.fit(df10)

# days reference
prediction_dates_df = spark.createDataFrame([(day,) for day in range(835, 866)], ["days_since_reference"])

# add cases/deaths columns
prediction_dates_df = prediction_dates_df.withColumn("cases", lit(0)).withColumn("deaths", lit(0))

prediction_data = vector_assembler.transform(prediction_dates_df)

# inference
predictions = model_cases.transform(prediction_data)
predictions = model_deaths.transform(predictions)

predictions = predictions.withColumn("days_since_reference", predictions["days_since_reference"].cast("int"))
predictions = predictions.withColumn("date", expr(f"date_add('{reference_date}', days_since_reference)"))
predictions = predictions.withColumn("predicted_cases", round("predicted_cases", 0))
predictions = predictions.withColumn("predicted_deaths", round("predicted_deaths", 0))
predictions = predictions.withColumn("predicted_cases", col("predicted_cases").cast("int"))
predictions = predictions.withColumn("predicted_deaths", col("predicted_deaths").cast("int"))

# stored as a json file
predictions.select("date", "predicted_cases", "predicted_deaths")\
            .write.json(output_path + "result10.json", mode="overwrite")


# Decision Tree Regressor for cases
dt_cases = DecisionTreeRegressor(featuresCol="features", labelCol="cases", predictionCol="predicted_cases")

# Decision Tree Regressor for deaths
dt_deaths = DecisionTreeRegressor(featuresCol="features", labelCol="deaths", predictionCol="predicted_deaths")

# Train the models
model_cases_dt = dt_cases.fit(df10)
model_deaths_dt = dt_deaths.fit(df10)

# Predictions
predictions_dt = model_cases_dt.transform(prediction_data)
predictions_dt = model_deaths_dt.transform(predictions_dt)

predictions_dt = predictions_dt.withColumn("days_since_reference", predictions_dt["days_since_reference"].cast("int"))
predictions_dt = predictions_dt.withColumn("date", expr(f"date_add('{reference_date}', days_since_reference)"))
predictions_dt = predictions_dt.withColumn("predicted_cases", round("predicted_cases", 0))
predictions_dt = predictions_dt.withColumn("predicted_deaths", round("predicted_deaths", 0))
predictions_dt = predictions_dt.withColumn("predicted_cases", col("predicted_cases").cast("int"))
predictions_dt = predictions_dt.withColumn("predicted_deaths", col("predicted_deaths").cast("int"))

predictions_dt.select("date", "predicted_cases", "predicted_deaths")\
            .write.json(output_path + "result11.json", mode="overwrite")