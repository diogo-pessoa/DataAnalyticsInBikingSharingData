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
        with open(schema_path, 'r', encoding='utf8') as stream:
            schema_yaml = yaml.safe_load(stream)
            columns = schema_yaml['columns']
            fields = [pyspark.sql.types.StructField(name,
                                                    struct_field_type_mapping[
                                                        dtype]) for name, dtype
                      in columns.items()]
            return StructType(fields)
    return None


def load_data(data_path: str) -> (
        pyspark.sql.dataframe.DataFrame):
    """
    Load data into spark session.
    :param data_path:
    :param spark_session:
    """
    local_spark_session = create_spark_session()
    schema = load_schema(os.path.join(data_path, 'divvy-tripdata-schema.yaml'))
    df = local_spark_session.read.csv(data_path, header=True, schema=schema)
    print(df.printSchema())
    return df
