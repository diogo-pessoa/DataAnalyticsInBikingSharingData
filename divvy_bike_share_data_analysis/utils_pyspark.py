"""
This module is used to load data into spark session.
The load_data function loads data into spark session, calls the load_schema (
assumes the schema file is in the same directory as the data) and returns the
dataframe.
"""
import os.path

import pyspark.sql.types
import yaml
from pyspark.sql import SparkSession
from pyspark.sql.types import (StructType, StringType, IntegerType, FloatType,
                               TimestampType)


def create_spark_session():
    """
    Create a spark session.
    """
    spark = SparkSession.builder.master("local").appName(
        "Divvy Bike Share Data Analysis").getOrCreate()
    return spark


def load_schema(schema_path):
    """
    Load schema from schema file into spark StructType.
    :param schema_path:
    :return: schema_yaml_path
    """
    struct_field_type_mapping = {"string": StringType(),
                                 "integer": IntegerType(), "float": FloatType(),
                                 "datetime": TimestampType()}
    if schema_path and os.path.isfile(schema_path):
        try:
            with open(schema_path, 'r', encoding='utf8') as stream:
                schema_yaml = yaml.safe_load(stream)
                columns = schema_yaml['columns']
                fields = [pyspark.sql.types.StructField(name,
                                                        struct_field_type_mapping[
                                                            dtype]) for
                          name, dtype in columns.items()]
                return StructType(fields)
        except yaml.YAMLError as yaml_error:
            raise yaml.YAMLError(
                f"Schema file {schema_path} does not exist.") from yaml_error
    else:
        raise FileNotFoundError(f"Schema file {schema_path} does not exist.")


def load_dataset_to_spark(data_path: str) -> (pyspark.sql.dataframe.DataFrame):
    """
    Load data into spark session.
    :param data_path:
    :param spark_session:
    """
    local_spark_session = create_spark_session()
    schema = load_schema(os.path.join(data_path, 'divvy-tripdata-schema.yaml'))
    df = local_spark_session.read.csv(data_path, schema=schema)
    return df


def load_data_to_spark_big_query_enabled(data_path: str) -> (
pyspark.sql.dataframe.DataFrame):
    """
    Load data into spark session with google big query enabled.
    :param data_path:
    :param spark_session:
    """
    local_spark_session = (SparkSession.builder.appName(
        'BigQuery Integration').config(
        'spark.jars.packages',
       'com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.21.0')
                           .getOrCreate())
    # local_spark_session.conf.set("materializationDataset","<dataset>") #
    # Review if bug in spark big query connector is affecting this method.
    schema = load_schema(os.path.join(data_path, 'divvy-tripdata-schema.yaml'))
    df = local_spark_session.read.csv(data_path, schema=schema)
    return df
