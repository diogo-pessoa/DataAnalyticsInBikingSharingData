"""
Mock tests for data_to_pyspark.py
"""
import os
import unittest

import pyspark
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import (StringType, IntegerType, FloatType,
                               TimestampType, StructType)

from divvy_bike_share_data_analysis.utils_pyspark import (create_spark_session,
                                                          load_schema)


class UtilsPySparkTestCase(unittest.TestCase):
    """
    Mock tests for data_to_pyspark.py
    """

    def test_create_spark_session_returns_spark_session(self):
        """
        Assert SparkSession
        :return:
        """
        session = create_spark_session()
        assert isinstance(session, SparkSession)

    def test_load_schema_with_valid_file(self):
        """
        Assert schema is loaded correctly into a Spark StructType. Each
        column with their respective Spark StructField.
        """
        schema_path = 'valid_schema.yaml'
        with open(schema_path, 'w', encoding='utf8') as f:
            f.write(
                'columns:\n  column1: string\n  column2: integer\n  column3: '
                'float\n  column4: datetime')
        schema = load_schema(schema_path)
        expected_schema = StructType(
            [pyspark.sql.types.StructField('column1', StringType()),
             pyspark.sql.types.StructField('column2', IntegerType()),
             pyspark.sql.types.StructField('column3', FloatType()),
             pyspark.sql.types.StructField('column4', TimestampType())])
        assert schema == expected_schema
        os.remove(schema_path)

    def test_load_schema_with_nonexistent_file(self):
        """
        Assert FileNotFoundError is raised when schema file does not exist.
        """
        schema_path = 'nonexistent_schema.yaml'
        with pytest.raises(FileNotFoundError):
            load_schema(schema_path)


if __name__ == '__main__':
    unittest.main()
