"""
Bike Stations Tests for Divvy Bike Share Data Analysis
"""
import unittest

from pyspark.sql import SparkSession

from divvy_bike_share_data_analysis import bike_stations


class BikeStationsTestCase(unittest.TestCase):
    """
    Tests for bike_stations.py
    """

    def test_get_unique_bike_stations_ids_returns_correct_dataframe(self):
        """
        Assert get_unique_bike_stations_ids returns correct dataframe.
        """
        spark = SparkSession.builder.getOrCreate()
        data = [("1", "Station A", "2", "Station B"),
                ("1", "Station A", "3", "Station C"),
                ("2", "Station B", "1", "Station A"),
                ("2", "Station B", "3", "Station C"),
                ("3", "Station C", "1", "Station A"),
                ("3", "Station C", "2", "Station B")]
        df = spark.createDataFrame(data,
                                   ["start_station_id", "start_station_name",
                                    "end_station_id", "end_station_name"])
        result = bike_stations.get_unique_bike_stations_ids(df)
        expected_data = [("1", "Station A"), ("2", "Station B"),
                         ("3", "Station C")]
        expected_df = spark.createDataFrame(expected_data,
                                            ["station_id", "station_name"])
        assert result.collect() == expected_df.collect()

    def test_categorize_time_of_day_returns_correct_category(self):
        """
        Assert categorize_time_of_day returns correct category.
        """
        assert bike_stations.categorize_time_of_day(6) == 'Morning'
        assert bike_stations.categorize_time_of_day(12) == 'Afternoon'
        assert bike_stations.categorize_time_of_day(18) == 'Evening'
        assert bike_stations.categorize_time_of_day(22) == 'Night'

    def test_categorize_time_of_day_handles_edge_cases(self):
        """
        Assert categorize_time_of_day handles edge cases.
        """
        assert bike_stations.categorize_time_of_day(5) == 'Morning'
        assert bike_stations.categorize_time_of_day(11) == 'Morning'
        assert bike_stations.categorize_time_of_day(12) == 'Afternoon'
        assert bike_stations.categorize_time_of_day(16) == 'Afternoon'
        assert bike_stations.categorize_time_of_day(17) == 'Evening'
        assert bike_stations.categorize_time_of_day(20) == 'Evening'
        assert bike_stations.categorize_time_of_day(21) == 'Night'
        assert bike_stations.categorize_time_of_day(4) == 'Night'


if __name__ == '__main__':
    unittest.main()
