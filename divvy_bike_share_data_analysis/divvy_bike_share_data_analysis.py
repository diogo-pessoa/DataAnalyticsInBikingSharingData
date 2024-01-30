"""
Main file to orchestrate the data collection process.
"""
import data_collection

print(dir(data_collection))
DATA_COLLECTION_DIR = '/Users/macbook/code/TechProject1/data_collection/data'
data_collection.get_files(DATA_COLLECTION_DIR, [2020, 2021, 2022, 2023])
