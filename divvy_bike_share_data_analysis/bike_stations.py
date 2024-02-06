"""
Functions to clean and process bike stations data, including time trips started.
"""

from pyspark.sql import DataFrame
from pyspark.sql.functions import col


def get_unique_bike_stations_ids(trip_data: DataFrame) -> DataFrame:
    """
    select only bike stations with unique ids and names, and drop nulls and
    duplicates.
    Apply filtering on this subset with conflicting start and end names,
    except conflicting stations names.

    returns a DataFrame with unique bike stations ids and names. Based on
    unique Start Station Id and Start Station Names.
    # TODO - Future improvement, Sanity check station Ids on both start and
    # end to decide which is more likely to be valid.
    :param trip_data:
    :return:
    """

    trip_data_clean = trip_data.dropna().distinct()
    start_stations = (trip_data_clean.select(
        "start_station_id",
        "start_station_name").withColumnRenamed(
        "start_station_id",
        "station_id").withColumnRenamed(
        "start_station_name",
        "station_name"))
    end_stations = trip_data_clean.select(
        "end_station_id",
        "end_station_name").withColumnRenamed(
        "end_station_id", "station_id")
    non_conflicting_stations = start_stations.join(end_stations,
                                                   on="station_id",
                                                   how="left").filter(
        col("station_name") == col("end_station_name")).drop(
        "end_station_name")

    return non_conflicting_stations.distinct()


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


def categorize_day_of_week(day_of_week):
    """
    return label for day of week (working days or weekend)
    :param  pyspark.sql.functions: from 1 for a Sunday through to 7  Saturday
    :return: string
    """
    if 2 <= day_of_week <= 5:
        return 'Workday'
    return 'non-Workday'
