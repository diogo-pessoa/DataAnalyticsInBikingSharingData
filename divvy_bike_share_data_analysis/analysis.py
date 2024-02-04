"""
Main file to orchestrate the data collection process.
"""

from divvy_bike_share_data_analysis import data_loader, \
    utils_pyspark

# Collecting data to local directory
DATA_COLLECTION_DIR: str = '/Users/macbook/code/TechProject1/data_collection/'
data_loader.load_dataset_to_local_fs(DATA_COLLECTION_DIR, [2020, 2021, 2022, 2023])
# creating pyspark session and pre-processing data
utils_pyspark.load_dataset_to_spark(DATA_COLLECTION_DIR)
