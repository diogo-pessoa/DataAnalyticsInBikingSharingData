"""
Functions to clean and process bike stations data, including time trips started.
"""

from pyspark.sql import DataFrame
from pyspark.sql.functions import col


def get_unique_bike_stations_ids(trip_data: DataFrame) -> DataFrame:
    """
    TODO: Add docstring, tests and type hints.
    :param trip_data:
    :return:
    """
    grouped_stations_by_matching_id = trip_data.select('start_station_id',
                                                       'start_station_name',
                                                       'end_station_id',
                                                       'end_station_name').distinct().dropna()
    conflicting_stations = grouped_stations_by_matching_id.filter(
        col("start_station_name") != col("end_station_name"))
    grouped_stations_by_matching_id.exceptAll(conflicting_stations).show()

    bike_stations = grouped_stations_by_matching_id[
        "start_station_id", "start_station_name"].distinct().withColumnRenamed(
        "start_station_id", "station_id").withColumnRenamed(
        "start_station_name", "station_name")

    return bike_stations


def categorize_time_of_day(hour):
    """
    return label for hour of day
    :param hour:
    :return: string
    """
    if 5 <= hour < 12:
        return 'Morning'
    if 12 <= hour < 17:
        return 'Afternoon'
    if 17 <= hour < 21:
        return 'Evening'
    return 'Night'
