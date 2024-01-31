"""
Main file to orchestrate the data collection process.
"""

from divvy_bike_share_data_analysis import data_loader, \
    data_to_pyspark

# Collecting data to local directory
DATA_COLLECTION_DIR: str = '/Users/macbook/code/TechProject1/data_collection/'
data_loader.get_files(DATA_COLLECTION_DIR, [2020, 2021, 2022, 2023])

# creating pyspark session and pre-processing data
data_to_pyspark.load_data(DATA_COLLECTION_DIR)
