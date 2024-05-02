from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import from_csv, from_json, col

sales_schema = StructType([
    StructField("fname", StringType(), False),
    StructField("lname", StringType(), False),
    StructField("url", StringType(), False),
    StructField("product", StringType(), False),
    StructField("cnt", IntegerType(), False),
])

spark = SparkSession.builder.appName("SparkStructuredStreaming").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "sales")
    .option("delimeter", ",")
    .option("startingOffsets", "latest")
    .load()
)

df.printSchema()
# df.writeStream.format("console").start().awaitTermination()

# for kafka stream value in json schema
# df1 = df.selectExpr("CAST(value AS STRING)").select(from_json(col("value"), sales_schema).alias("data")).select("data.*")

# for kafka stream value in csv schema
df1 = df.selectExpr("CAST(value AS STRING)").select(from_csv(col("value"), sales_schema.simpleString()).alias("data")).select("data.*")

df1.printSchema()
# df1.writeStream.format("console").start().awaitTermination()

def writeToCassandra(writeDF, _):
    (
        writeDF.write.format("org.apache.spark.sql.cassandra")
        .mode('append')
        .options(table="cust_data", keyspace="spark_kafka")
        .save()
    )

(
    df1.writeStream.option("spark.cassandra.connection.host", "localhost:9042")
    .foreachBatch(writeToCassandra)
    .outputMode("update")
    .start()
    .awaitTermination()
)
