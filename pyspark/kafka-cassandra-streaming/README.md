# Pre-requisites:

## Installations:
1. setup python
2. setup apache-spark
3. setup apache-zookeeper
4. setup apache-kafka
5. setup apache-cassandra

## Start Services:
1. $ZOOKEEPER_HOME/bin/zkServer.sh start
2. $KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties
3. $CASSANDRA_HOME/bin/cassandra -f

## Kafka Setup:
1. Create topic - sales:
`$KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic sales`
2. Launch Producer:
`$KAFKA_HOME/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic sales`
3. Launch Consumer:
`$KAFKA_HOME/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic sales --from-beginning`

# Cassandra Setup:

1. Launch Cassandra shell:
`cqlsh`
2. Create keyspace:
`create keyspace spark_kafka with replication ={'class':'SimpleStrategy','replication_factor':1};`
3. Create table:
`CREATE TABLE spark_kafka.cust_data (fname text, lname text, url text, product text, cnt counter, primary key (fname, lname, url, product));`
4. Select table:
`select * from spark_kafka.cust_data;`

# Spark Application:
1. Run spark job:
`spark-submit --packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,com.datastax.spark:spark-cassandra-connector_2.12:3.0.0 kafka-to-cassandra.py`
