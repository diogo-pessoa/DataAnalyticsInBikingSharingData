"""
Mock Tests for http crawler pulling data from AWS S3 (Divvy Bike Share)
TODO review csv tests, consider moving to separate file
"""
import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from divvy_bike_share_data_analysis import data_loader


class DataLoaderTestCase(unittest.TestCase):
    """
    Tests for data_loader.py
    """

    @patch('os.makedirs')
    def test_create_local_dir_creates_directory_when_not_exists(self,
                                                                mock_makedirs):
        """
        Assert create_local_dir creates directory when it does not exist.
        :param mock_makedirs:
        :return:
        """
        # pylint: disable=protected-access
        assert data_loader._create_local_dir('test_dir')
        mock_makedirs.assert_called_once_with('test_dir')

    @patch('os.makedirs')
    def test_create_local_dir_does_not_create_directory_when_exists(self,
                                                                    mock_makedirs):
        """
        TODO check for merging both creat_dirs tests asserting all into one
        Assert create_local_dir does not create directory when it exists.
        :param mock_makedirs:
        :return:
        """
        with patch('os.path.exists', return_value=True):
            # pylint: disable=protected-access
            assert not data_loader._create_local_dir('test_dir')
        mock_makedirs.assert_not_called()

    @patch('requests.get')
    def test_download_zip_files_downloads_file_when_not_exists(self, mock_get):
        """
        Assert download_zip_files downloads file when it does not exist.
        :param mock_get:
        :return:
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b'test content'
        with patch('builtins.open', new_callable=MagicMock):
            # pylint: disable=protected-access
            data_loader._download_zip_files(['http://test.com/test.zip'],
                                            'test_dir')

    @patch('requests.get')
    def test_download_zip_files_skips_download_when_file_exists(self, mock_get):
        """
        Assert download_zip_files skips download when file exists.
        :param mock_get:
        :return:
        """
        with patch('os.path.exists', return_value=True):
            # pylint: disable=protected-access
            data_loader._download_zip_files(['http://test.com/test.zip'],
                                            'test_dir')
        mock_get.assert_not_called()

    @patch('zipfile.ZipFile')
    def test_unzip_files_extracts_zip_files(self, mock_zipfile):
        """
        Assert unzip_files extracts zip files.
        :param mock_zipfile:
        :return:
        """
        mock_zipfile.return_value.__enter__.return_value.extractall = (
            MagicMock())
        with patch('os.listdir', return_value=['test.zip']), patch('os.remove'):
            # pylint: disable=protected-access
            data_loader._unzip_files('test_dir')

    def test_get_url_returns_correct_urls(self):
        """
        Assert get_url returns correct urls.
        :return:
        """
        # pylint: disable=protected-access
        urls = data_loader._get_url([2020])
        assert urls == [(f"https://divvy-tripdata.s3.amazonaws.com/2020"
                         f"{m:02d}-divvy-tripdata.zip") for m in range(1, 13)]

    def test_csv_headers_sanitize_on_valid_file(self):
        """
        Assert if csv content quotes are removed.
        """
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp:
            temp.write(b'"header1","header2"\n"val1","val2"')
            temp.close()
            # pylint: disable=protected-access
            data_loader._sanitize_csv_headers_inplace(tempfile.gettempdir())
            with open(temp.name, 'r', encoding='utf8') as file:
                lines = file.readlines()
            assert lines[0] == 'header1,header2\n'
            assert lines[1] == 'val1,val2'
            os.remove(temp.name)

    def test_csv_headers_sanitize_on_empty_file(self):
        """
        Assert if csv content quotes are removed.
        """
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp:
            temp.close()
            # pylint: disable=protected-access
            data_loader._sanitize_csv_headers_inplace(tempfile.gettempdir())
            with open(temp.name, 'r', encoding='utf8') as file:
                lines = file.readlines()
            assert lines == []
            os.remove(temp.name)


if __name__ == '__main__':
    unittest.main()
