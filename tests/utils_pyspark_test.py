"""
Mock tests for data_to_pyspark.py
"""
import unittest
from unittest.mock import patch, MagicMock

import pyspark
import pytest
from pyspark.sql import SparkSession

from divvy_bike_share_data_analysis.utils_pyspark import (create_spark_session,
                                                          load_schema,
                                                          load_data)


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

    # TODO skip test for now - needs to be updated after moving to class
    @patch('os.path.isfile')
    @patch('builtins.open')
    @unittest.skip("skipping test")
    def test_load_schema_returns_struct_type_when_file_exists(self, mock_open,
                                                              mock_isfile):
        """
        Assert StructType
        :param mock_open:
        :param mock_isfile:
        :return:
        """
        mock_isfile.return_value = True
        mock_open.return_value.__enter__.return_value = MagicMock(spec=open)
        schema = load_schema('schema.yaml')
        assert isinstance(schema, pyspark.sql.types.StructType)

    @patch('os.path.isfile')
    def test_load_schema_returns_none_when_file_does_not_exist(self,
                                                               mock_isfile):
        """
        TODO: update test to test for exception in case schema is missing
        Assert Raises exception for missing files
        :param mock_isfile:
        :return:
        """
        mock_isfile.return_value = False
        schema = load_schema('schema.yaml')
        assert schema is None

    # TODO skip test for now - needs to be updated after moving to class
    @unittest.skip("skipping test")
    @patch('divvy_bike_share_data_analysis.load_csv_into_pyspark'
           '.create_spark_session')
    @patch('divvy_bike_share_data_analysis.load_csv_into_pyspark.load_schema')
    def test_load_data_returns_dataframe_when_schema_exists(self,
                                                            mock_load_schema,
                                                            mock_create_spark_session):
        """

        :param mock_load_schema:
        :param mock_create_spark_session:
        :return:
        """
        mock_load_schema.return_value = pyspark.sql.types.StructType()
        mock_create_spark_session.return_value = (
            SparkSession.builder.getOrCreate())
        df = load_data('data.csv')
        assert isinstance(df, pyspark.sql.dataframe.DataFrame)

    # TODO skip test for now - needs to be updated after moving to class
    @unittest.skip("skipping test")
    @patch('divvy_bike_share_data_analysis.load_csv_into_pyspark'
           '.create_spark_session')
    @patch('divvy_bike_share_data_analysis.load_csv_into_pyspark.load_schema')
    def test_load_data_raises_error_when_schema_does_not_exist(self,
                                                               mock_load_schema, ):
        """

        :param mock_load_schema:
        :param mock_create_spark_session:
        :return:
        """
        mock_load_schema.return_value = None
        with pytest.raises(Exception):
            load_data('data.csv')


if __name__ == '__main__':
    unittest.main()
