"""
Helper Function to create and manage dataset in BigQuery
"""
import os

from dotenv import load_dotenv
from pyspark.sql import SparkSession

# Load environment variables from a .env file
load_dotenv()


def _start_spark_big_query_session():
    # Start the Spark session
    spark = SparkSession.builder.appName('BigQuery Integration').config(
        'spark.jars.packages',
        'com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.21.0'
        '').getOrCreate()
    return spark


def create_dataset():
    """
    Create a dataset in BigQuery
    :param dataset:
    :return:
    """
    table = os.environ.get('TABLE_NAME')
    bigquery_dataset_id = os.environ.get('BG_DATASET_ID')
    spark_session = _start_spark_big_query_session()
    spark_session.write.format('bigquery').option(table,
                                                  bigquery_dataset_id).save()
