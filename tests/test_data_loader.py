"""
Mock Tests for http crawler pulling data from AWS S3 (Divvy Bike Share)
"""

from unittest.mock import patch, MagicMock

from divvy_bike_share_data_analysis.data_loader import get_url, \
    download_zip_files, unzip_files, create_local_dir, get_files


@patch('os.makedirs')
def test_create_local_dir_creates_directory_when_not_exists(mock_makedirs):
    """
    Assert create_local_dir creates directory when it does not exist.
    :param mock_makedirs:
    :return:
    """
    assert create_local_dir('test_dir')
    mock_makedirs.assert_called_once_with('test_dir')


@patch('os.makedirs')
def test_create_local_dir_does_not_create_directory_when_exists(mock_makedirs):
    """
    TODO check for merging both creat_dirs tests asserting all into one
    Assert create_local_dir does not create directory when it exists.
    :param mock_makedirs:
    :return:
    """
    with patch('os.path.exists', return_value=True):
        assert not create_local_dir('test_dir')
    mock_makedirs.assert_not_called()


@patch('requests.get')
def test_download_zip_files_downloads_file_when_not_exists(mock_get):
    """
    Assert download_zip_files downloads file when it does not exist.
    :param mock_get:
    :return:
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b'test content'
    with patch('builtins.open', new_callable=MagicMock):
        download_zip_files(['http://test.com/test.zip'], 'test_dir')


@patch('requests.get')
def test_download_zip_files_skips_download_when_file_exists(mock_get):
    """
    Assert download_zip_files skips download when file exists.
    :param mock_get:
    :return:
    """
    with patch('os.path.exists', return_value=True):
        download_zip_files(['http://test.com/test.zip'], 'test_dir')
    mock_get.assert_not_called()


@patch('zipfile.ZipFile')
def test_unzip_files_extracts_zip_files(mock_zipfile):
    """
    Assert unzip_files extracts zip files.
    :param mock_zipfile:
    :return:
    """
    mock_zipfile.return_value.__enter__.return_value.extractall = MagicMock()
    with patch('os.listdir', return_value=['test.zip']), patch('os.remove'):
        unzip_files('test_dir')


def test_get_url_returns_correct_urls():
    """
    Assert get_url returns correct urls.
    :return:
    """
    urls = get_url([2020])
    assert urls == [(f"https://divvy-tripdata.s3.amazonaws.com/2020"
                     f"{m:02d}-divvy-tripdata.zip") for m in range(1, 13)]


@patch('divvy_bike_share_data_analysis.data_loader.get_url')
@patch('divvy_bike_share_data_analysis.data_loader.download_zip_files')
@patch('divvy_bike_share_data_analysis.data_loader.create_local_dir')
@patch('divvy_bike_share_data_analysis.data_loader.unzip_files')
def test_get_files_calls_all_functions(mock_unzip_files, mock_create_local_dir,
                                       mock_download_zip_files, mock_get_url):
    """
    Assert get_files calls all functions.
    :param mock_unzip_files:
    :param mock_create_local_dir:
    :param mock_download_zip_files:
    :param mock_get_url:
    :return:
    """
    get_files('test_dir', [2020])
    mock_get_url.assert_called_once_with([2020])
    mock_download_zip_files.assert_called_once()
    mock_create_local_dir.assert_called_once_with('test_dir')
    mock_unzip_files.assert_called_once_with('test_dir')
