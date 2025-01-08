from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, current_timestamp, when, expr

# JDBC JAR Path
jdbc_jar_path = "/home/hr295/spark/jars/postgresql-42.6.0.jar"

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("test") \
    .config("spark.jars", jdbc_jar_path) \
    .getOrCreate()

# File path
csv_file_path = "file:///home/hr295/reporter_dt.csv"

# Read the CSV file into a DataFrame
df = spark.read.csv(csv_file_path, header=True, inferSchema=True)

# Add new columns: is_read and is_read_time
df1 = df.withColumn("is_read", lit(None).cast("string")) \
        .withColumn("is_read_time", current_timestamp())

# PostgreSQL connection properties
pgsql_properties = {
    "user": "postgres",                 # Replace with your PostgreSQL username
    "password": "access",               # Replace with your PostgreSQL password
    "driver": "org.postgresql.Driver"   # JDBC driver class
}

# PostgreSQL JDBC URL
jdbc_url = "jdbc:postgresql://192.168.1.77:5432/sample_database"

# Write the DataFrame to the PostgreSQL table
df1.write.jdbc(url=jdbc_url, table="curated_reporter_dt", mode="overwrite", properties=pgsql_properties)

# Add new columns: is_processed and is_processed_time
df2 = df1.withColumn(
    "is_processed", when(df1["is_read"].isNull(), lit("True")).otherwise(lit("False"))
).withColumn(
    "is_processed_time", expr("is_read_time + INTERVAL 2 minutes")
)

# Write the updated DataFrame to the PostgreSQL table
df2.write.jdbc(url=jdbc_url, table="updated_reporter_dt", mode="overwrite", properties=pgsql_properties)

# Create a temporary view for querying
df2.createOrReplaceTempView("Test")

# Display selected columns from the temporary view
spark.sql("SELECT is_read, is_read_time, is_processed, is_processed_time FROM Test").show(10, False)

# Stop the SparkSession
spark.stop()

