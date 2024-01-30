"""
Pulls files from Divvy Bike Share's S3 bucket and unzips them to a local storage
"""


import os
import zipfile
import requests


def get_url(years_to_download):
    """
    This section assumes the file naming convention pattern based on visual
    review of https://divvy-tripdata.s3.amazonaws.com/index.html shared by
    Divvy.

     On the next few lines we'll build a list for files for the list of years.
        https://divvy-tripdata.s3.amazonaws.com/<year><month>-divvy-tripdata.zip

     The endpoint doesn't require authentication, thence this is a simple GET
     request to download the data.
     The code will add validation (Try, Catch) based on the response Code to
     avoid interruptions.
    """
    list_zip_files_urls = [
        f"https://divvy-tripdata.s3.amazonaws.com/{y}{m:02d}-divvy-tripdata.zip"
        for y in years_to_download for m in range(1, 13)]
    return list_zip_files_urls


def download_zip_files(zip_files_urls: list, local_dir_path: str):
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
            if not r.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(r.content)
            else:
                print(f'Error downloading file status code: {file_name}, '
                      f'{r.status_code}')
        except requests.exceptions.RequestException as e:
            raise RuntimeWarning(f"Error downloading file: {file_name}") \
                from e


def unzip_files(local_path_of_zip_files: str):
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


def create_local_dir(local_data_path: str) -> bool:
    """
    Create local directory for datafiles if it does not exist.
    :return: bool
    """
    if not os.path.exists(local_data_path):
        os.makedirs(local_data_path)
        return True
    return False


def get_files(local_dir: str, years_to_download: list):
    """
    :param local_dir:
    :param years_to_download:
    :return:
    """
    list_zip_files_urls = get_url(years_to_download)
    print("Downloading files...")
    download_zip_files(list_zip_files_urls, local_dir)
    create_local_dir(local_dir)
    print("Unzipping files...")
    unzip_files(local_dir)


def __dir__():
    return [name for name, val in globals().items() if
            callable(val) and name[0] != "_"]
