import sys
from pyspark.sql import SparkSession

# Prerequisites:
# 1. setup python
# 2. setup apache spark
# 3. setup mysql server
# 5. create mysql table named 'test_table' and columns 'id', 'name', 'age', 'dob'

# Run Command:
# spark-submit --packages mysql:mysql-connector-java:8.0.33 main.py read "test.test_table"

jdbc_url = "jdbc:mysql://{}:{}?enabledTLSProtocols=TLSv1.2&allowMultiQueries=true&rewriteBatchedStatements=true&useAffectedRows=true&useUnicode=true&characterEncoding=utf-8&zeroDateTimeBehavior=convertToNull".format("127.0.0.1","3306")
username = "MySQL-User"
password = "MySQL-Password"


def write(spark, table):
	print(f">>> mysql write : {table} <<<")
	data = [(1, "pyspark1", 67, "2001-01-01"), (2, "pyspark2", 79, "2002-01-02"), (3, "pyspark3", 71, "2002-01-03")]
	columns = ["id", "name", "age", "dob"]
	df = spark.createDataFrame(data, columns)
	df.show()
	max_id = df.count()
	print(max_id)

	(
		df.write.format("jdbc").option("url", jdbc_url)
		.option("driver", "com.mysql.jdbc.Driver")
		.option("dbtable", table)
		.option("port", 3306)
		.option("user", username)
		.option("password", password)
		.option("partitionColumn", "id")
		.option("numPartitions", ((max_id // 10000) + 1))
		.option("lowerBound", 1)
		.option("upperBound", max_id)	
		.mode("append").save()
	)
	print("mysql write complete")


def read(spark, table):
	print(f">>> mysql read : {table} <<<")
	df = (
		spark.read.format("jdbc").option("url", jdbc_url)
		.option("driver", "com.mysql.jdbc.Driver")
		.option("dbtable", table)
		.option("port", 3306)
		.option("user", username)
		.option("password", password)
		.load()
	)
	df.show()
	print("mysql read complete")


def main(mode, table):
	spark = (
		SparkSession.builder.appName("MySQL example")
		.enableHiveSupport()
		.getOrCreate()
	)
	sc = spark.sparkContext
	sc.setLogLevel("ERROR")

	access_mode = {
		"read": read,
		"write": write
	}
	access_mode[mode](spark=spark, table=table)
	spark.stop()

if __name__ == "__main__":
	main(mode=sys.argv[1], table=sys.argv[2])
