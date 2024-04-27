"""
## Description
write pyspark code to perform SCD Type-2 operation without using Delta (or) CDC logics

## Datasets
### Input Datasets
>>>>> Input Dataframe <<<<<
+------+-------------+-----------+--------------+------------+
|emp_id|employee_name|designation|eff_start_date|eff_end_date|
+------+-------------+-----------+--------------+------------+
|     1|          XXX|      Eng 1|    2000-01-01|  2005-06-30|
|     2|          YYY|      Eng 3|    2002-04-01|  2007-08-20|
|     1|          XXX|      Eng 2|    2005-06-30|  2099-12-31|
|     2|          YYY|      Eng 4|    2007-08-20|  2099-12-31|
+------+-------------+-----------+--------------+------------+

>>>>> Incremental Dataframe <<<<<
+------+-------------+-----------+--------------+------------+
|emp_id|employee_name|designation|eff_start_date|eff_end_date|
+------+-------------+-----------+--------------+------------+
|     1|          XXX|      Eng 3|    2008-04-15|        NULL|
|     2|          YYY|  Manager 1|    2010-10-10|        NULL|
+------+-------------+-----------+--------------+------------+

### Output Datasets
>>>>> Final Dataframe <<<<<
+------+-------------+-----------+--------------+------------+---------+
|emp_id|employee_name|designation|eff_start_date|eff_end_date|is_active|
+------+-------------+-----------+--------------+------------+---------+
|     1|          XXX|      Eng 1|    2000-01-01|  2005-06-30|    false|
|     1|          XXX|      Eng 2|    2005-06-30|  2008-04-15|    false|
|     1|          XXX|      Eng 3|    2008-04-15|  2099-12-31|     true|
|     2|          YYY|      Eng 3|    2002-04-01|  2007-08-20|    false|
|     2|          YYY|      Eng 4|    2007-08-20|  2010-10-10|    false|
|     2|          YYY|  Manager 1|    2010-10-10|  2099-12-31|     true|
+------+-------------+-----------+--------------+------------+---------+

## Functions Used
* Lead Window Function
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.window import Window

spark = (
    SparkSession.builder.appName("Pyspark SCD Type-2 Tutorial")
    .enableHiveSupport()
    .getOrCreate()
)
sc = spark.sparkContext
sc.setLogLevel("ERROR")


if __name__ == "__main__":
    # Input Dataframe with columns: "emp_id", "employee_name", "designation", "eff_start_date", "eff_end_date"
    input_df = (
        spark.createDataFrame([
            {"emp_id": 1, "employee_name": "XXX", "designation": "Eng 1", "eff_start_date": "2000-01-01", "eff_end_date": "2005-06-30"},
            {"emp_id": 2, "employee_name": "YYY", "designation": "Eng 3", "eff_start_date": "2002-04-01", "eff_end_date": "2007-08-20"},
            {"emp_id": 1, "employee_name": "XXX", "designation": "Eng 2", "eff_start_date": "2005-06-30", "eff_end_date": "2099-12-31"},
            {"emp_id": 2, "employee_name": "YYY", "designation": "Eng 4", "eff_start_date": "2007-08-20", "eff_end_date": "2099-12-31"}
        ])
        .select("emp_id", "employee_name", "designation", "eff_start_date", "eff_end_date")
    )
    print(">>>>> Input Dataframe <<<<<")
    input_df.show()

    # Incremental Dataframe with columns: "emp_id", "employee_name", "designation", "eff_start_date"
    incr_df = (
        spark.createDataFrame([
            {"emp_id": 1, "employee_name": "XXX", "designation": "Eng 3", "eff_start_date": "2008-04-15"},
            {"emp_id": 2, "employee_name": "YYY", "designation": "Manager 1", "eff_start_date": "2010-10-10"}
        ])
        .withColumn("eff_end_date", f.lit(None))
        .select("emp_id", "employee_name", "designation", "eff_start_date", "eff_end_date")
    )
    print(">>>>> Incremental Dataframe <<<<<")
    incr_df.show()

    # Apply Window function to rearrange Input Dataframe based on "emp_id" and order by "eff_start_date"
    window_func = Window.partitionBy("emp_id").orderBy("eff_start_date")

    # 1. Combine Input Dataframe and Incremental Dataframe
    # 2. Apply Lead function and get "eff_start_date" of leading record and set "eff_end_date" of current record using Window Function
    # 3. Add column "is_active" to verify the latest records
    input_df = (
        input_df
        .union(incr_df)
        .withColumn("eff_end_date", f.lead("eff_start_date").over(window_func))
        .withColumn("is_active", f.when(f.coalesce("eff_end_date").isNull(), True).otherwise(False))
        .na.fill({"eff_end_date": "2099-12-31"})
    )
    print(">>>>> Final Dataframe <<<<<")
    input_df.show()
