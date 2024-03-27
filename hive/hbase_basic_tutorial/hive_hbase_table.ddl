// create hive table named 'test_table' in 'hbase' database
// storage location as HBase storage
// HBase table and column mappings for HBase table named 'test_table' and column family 'personal_data'

CREATE EXTERNAL TABLE hbase.test_table(id int, name string, age int, dob string)
STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
WITH SERDEPROPERTIES ("hbase.columns.mapping" = ":key,personal_data:name,personal_data:age,personal_data:dob")
TBLPROPERTIES("hbase.table.name" = "test_table");

// once hive table is created, insert data into hive table
// inserted data will be saved in HBase storage
