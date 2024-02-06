"""
Bike Stations Tests for Divvy Bike Share Data Analysis
# TODO refactoring of unique bike stations ids in progress
"""

import unittest

from pyspark.sql.types import StringType, StructField, StructType

from divvy_bike_share_data_analysis.bike_stations import (
    get_unique_bike_stations_ids, categorize_time_of_day,
    categorize_day_of_week)
from divvy_bike_share_data_analysis.utils_pyspark import create_spark_session


@unittest.skip("Refactoring of unique bike stations ids in progress")
class BikeStationsTestCase(unittest.TestCase):
    """
    Tests for py

    """

    #pylint: disable=fixme
    # TODO refactoring of unique bike stations ids in progress
    @unittest.skip("Refactoring of unique bike stations ids in progress")
    def test_get_unique_bike_stations_ids_handles_conflicting_stations(self):
        """
        Assert Dataframes with unique names to ids relation
        """
        spark = create_spark_session()
        data = [("1", "Station A", "1", "Station A"),
                ("2", "Station B", "2", "Station C"),
                ("3", "Station C", "3", "Station C"),
                ("1", "Station A", "1", "Station A")]
        schema = StructType(
            [StructField("start_station_id", StringType(), True),
             StructField("start_station_name", StringType(), True),
             StructField("end_station_id", StringType(), True),
             StructField("end_station_name", StringType(), True)])
        df = spark.createDataFrame(data, schema)
        result = get_unique_bike_stations_ids(df)
        assert result.count() == 2

    def test_categorize_time_of_day_returns_correct_category(self):
        """
        Assert categorize_time_of_day returns correct category.
        """
        assert categorize_time_of_day(6) == 'Morning'
        assert categorize_time_of_day(12) == 'Afternoon'
        assert categorize_time_of_day(18) == 'Evening'
        assert categorize_time_of_day(22) == 'Night'

    def test_categorize_time_of_day_handles_edge_cases(self):
        """
        Assert categorize_time_of_day handles edge cases.
        """
        assert categorize_time_of_day(5) == 'Morning'
        assert categorize_time_of_day(11) == 'Morning'
        assert categorize_time_of_day(12) == 'Afternoon'
        assert categorize_time_of_day(16) == 'Afternoon'
        assert categorize_time_of_day(17) == 'Evening'
        assert categorize_time_of_day(20) == 'Evening'
        assert categorize_time_of_day(21) == 'Night'
        assert categorize_time_of_day(4) == 'Night'

    def test_label_categorize_day_of_week_working_days(self):
        """
        Test categorize_day_of_week returns correct label
        for working days.
        """
        self.assertEqual(categorize_day_of_week(2), 'Workday')
        self.assertEqual(categorize_day_of_week(5), 'Workday')

    def test_label_categorize_day_of_week_non_working_days(self):
        """
        Test categorize_day_of_week returns correct label
        for non-working days.
        """
        self.assertEqual(categorize_day_of_week(1), 'non-Workday')
        self.assertEqual(categorize_day_of_week(6), 'non-Workday')
        self.assertEqual(categorize_day_of_week(7), 'non-Workday')


if __name__ == '__main__':
    unittest.main()
