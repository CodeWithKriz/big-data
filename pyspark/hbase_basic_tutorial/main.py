from pyspark.sql import SparkSession

# Prerequisites:
# 1. setup python
# 2. setup apache spark
# 3. setup apache zookeeper
# 4. setup apache hbase
# 5. create hbase table named 'test_table' and column family 'personal_data'

# Run Command:
# spark-submit --packages org.apache.hbase.connectors.spark:hbase-spark:1.0.1 main.py

def write(spark):
	print(f">>> hbase write <<<")
	data = [
		(1, "pyspark1", 67, "2001-01-01"), 
		(2, "pyspark2", 79, "2002-01-02"), 
		(3, "pyspark3", 71, "2002-01-03")
	]
	columns = ["id", "name", "age", "dob"]
	df = spark.createDataFrame(data, columns)
	df.show()

	(
		df.write.format("org.apache.hadoop.hbase.spark")
		.option("spark.hbase.conf.dir", "/path/to/hbase-<version>/conf")
		.option("spark.hbase.connection", "org.apache.hadoop.hbase.HBaseConfiguration")
		.option("hbase.spark.use.hbasecontext", "false")
		.option("hbase.defaults.for.version.skip", "true")
		.option("hbase.table", "test_table")
		.option("hbase.columns.mapping", "id STRING :id, name STRING personal_data:name, age INT personal_data:age, dob STRING personal_data:dob")
		.option("spark.hadoop.validateOutputSpecs", "false")
		.save()
	)
	print("hbase write complete")


def read(spark):
	print(f">>> hbase read <<<")
	df = (
		spark.read.format("org.apache.hadoop.hbase.spark")
		.option("spark.hbase.conf.dir", "/path/to/hbase-<version>/conf")
		.option("spark.hbase.connection", "org.apache.hadoop.hbase.HBaseConfiguration")
		.option("hbase.spark.use.hbasecontext", "false")
		.option("hbase.defaults.for.version.skip", "true")
		.option("hbase.table", "test_table")
		.option("hbase.columns.mapping", "id STRING :id, name STRING personal_data:name, age INT personal_data:age, dob STRING personal_data:dob")
		.option("spark.hadoop.validateOutputSpecs", "false")
		.load()
	)
	df.show()
	print("hbase read complete")


if __name__ == "__main__":
	spark = (
		SparkSession.builder.appName("Hbase example")
		.enableHiveSupport()
		.getOrCreate()
	)
	sc = spark.sparkContext
	sc.setLogLevel("ERROR")
	write(spark=spark)
	read(spark=spark)
	spark.stop()
