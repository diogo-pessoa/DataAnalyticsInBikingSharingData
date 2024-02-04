import os

from google.cloud import bigquery
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame

from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()


def _start_spark_big_query_session():
    # Start the Spark session
    spark = SparkSession.builder.appName('BigQuery Integration').config(
        'spark.jars.packages',
        'com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.21.0'
        '').getOrCreate()
    return spark


def create_dataset(dataset: DataFrame):
    table = os.environ.get('TABLE_NAME')
    bigquery_dataset_id = os.environ.get('BG_DATASET_ID')
    client = bigquery.Client()
    spark_session = _start_spark_big_query_session()
    spark_session.write.format('bigquery').option(table,
                                                  bigquery_dataset_id).save()
