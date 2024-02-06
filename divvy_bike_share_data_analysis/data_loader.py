"""
Pulls files from Divvy Bike Share's S3 bucket and unzips them to a local storage
"""

import os
import zipfile

import requests


def _get_url(years_to_download):
    """
    This section assumes the file naming convention pattern based on visual
    review of https://divvy-tripdata.s3.amazonaws.com/index.html shared by
    Divvy.
    Path:
        https://divvy-tripdata.s3.amazonaws.com/<year><month>-divvy-tripdata.zip
    """
    list_zip_files_urls = [
        f"https://divvy-tripdata.s3.amazonaws.com/{y}{m:02d}-divvy-tripdata.zip"
        for y in years_to_download for m in range(1, 13)]
    return list_zip_files_urls


def _download_zip_files(zip_files_urls: list, local_dir_path: str):
    """
    downloads zip the files to the local path.
    :param local_dir_path:
    :param zip_files_urls:
    :return: None
    """
    file_url: str
    for file_url in zip_files_urls:
        file_name = file_url.split('/')[-1]
        file_path = os.path.join(local_dir_path, file_name)
        csv_file_path = file_path.replace('.zip', '.csv')
        if os.path.exists(file_path) or os.path.exists(csv_file_path):
            print(f'{file_name} already exists. Skipping Download.')
            continue
        try:
            print(f'Requesting file: {file_name}')
            r = requests.get(file_url, timeout=10)
            if r.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(r.content)
            else:
                print(f'Error downloading file status code: {file_name}, '
                      f'{r.status_code}')
        except requests.exceptions.RequestException as e:
            raise RuntimeWarning(f"Error downloading file: {file_name}") \
                from e


def _unzip_files(local_path_of_zip_files: str):
    """
    Unzip the files to the local path.
    :param local_path_of_zip_files:
    :return: None
    """

    if not os.listdir(local_path_of_zip_files):
        print("No files to unzip")
        return None

    for filename in os.listdir(local_path_of_zip_files):
        if filename.endswith('.zip'):
            # Construct the full path to the file
            file_path: str = os.path.join(local_path_of_zip_files, filename)
            # Open the zip file
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    # Extract all the contents into the directory
                    zip_ref.extractall(local_path_of_zip_files)
                    print(f"Extracted: {filename}")
            except zipfile.BadZipFile as e:
                print(f"Bad Zip File: {filename}")
                print(e)
            # Delete the zip file
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted: {filename}")
    return None


def _create_local_dir(local_data_path: str) -> bool:
    """
    Create local directory for datafiles if it does not exist.
    :return: bool
    """
    if not os.path.exists(local_data_path):
        os.makedirs(local_data_path)
        return True
    return False


def load_dataset_to_local_fs(local_dir: str, years_to_download: list):
    """
    Loads the dataset to local file system. This Function only groups the
    functions call. To Pull the divvy .csv S3 bucket and unzips them to a local
    storage.
    :param local_dir:
    :param years_to_download:
    :return:
    """
    _create_local_dir(local_dir)
    list_zip_files_urls = _get_url(years_to_download)
    print("Downloading files...")
    _download_zip_files(list_zip_files_urls, local_dir)
    print("Unzipping files...")
    _unzip_files(local_dir)
    _sanitize_csv_headers_inplace(local_dir)


def _sanitize_csv_headers_inplace(path_to_csvs):
    """
    Removes double quotes from csv headers inplace.
    :param path_to_csvs:
    :return:
    """
    for csv_file in [f for f in os.listdir(path_to_csvs) if f.endswith('.csv')]:
        file_path = os.path.join(path_to_csvs, csv_file)
        if os.path.exists(file_path):
            # Open the file in read mode and read lines
            with open(file_path, 'r', encoding='utf8') as file:
                lines = file.readlines()

            # Remove the double quotes from each line
            lines = [line.replace('"', '') for line in lines]

            # Open the file in write mode and write back the lines
            with open(file_path, 'w', encoding='utf8') as file:
                file.writelines(lines)


def __dir__():
    return [name for name, val in globals().items() if
            callable(val) and name[0] != "_"]
