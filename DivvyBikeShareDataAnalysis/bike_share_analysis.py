import data_collection

print(dir(data_collection))
data_collection_dir = '/Users/macbook/code/TechProject1/data_collection/data'
data_collection.get_files(data_collection_dir, [2020, 2021, 2022, 2023])
