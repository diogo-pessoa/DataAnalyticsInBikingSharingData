"""
Mock Tests for http crawler pulling data from AWS S3 (Divvy Bike Share)
TODO review csv tests, consider moving to separate file
"""
import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock, mock_open

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

    @patch('divvy_bike_share_data_analysis.data_loader.get_url')
    @patch('divvy_bike_share_data_analysis.data_loader.download_zip_files')
    @patch('divvy_bike_share_data_analysis.data_loader.create_local_dir')
    @patch('divvy_bike_share_data_analysis.data_loader.unzip_files')
    # TODO skip test for now - needs to be updated after moving to class
    @unittest.skip("skipping test")
    def test_get_files_calls_all_functions(self, mock_unzip_files,
                                           mock_create_local_dir,
                                           mock_download_zip_files,
                                           mock_get_url):
        """
        Assert get_files calls all functions.
        :param mock_unzip_files:
        :param mock_create_local_dir:
        :param mock_download_zip_files:
        :param mock_get_url:
        :return:
        """
        data_loader.load_dataset_to_local_fs('test_dir', [2020])
        mock_get_url.assert_called_once_with([2020])
        mock_download_zip_files.assert_called_once()
        mock_create_local_dir.assert_called_once_with('test_dir')
        mock_unzip_files.assert_called_once_with('test_dir')

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open,
           read_data='"""header1","header2","header3"\n"row1","row2","row3"')
    def test_removes_quotes_from_csv_headers(self, mock_file, mock_listdir,
                                             mock_exists):
        """
        Assert _sanitize_csv_headers_inplace removes quotes from csv headers.
        :param mock_file:
        :param mock_listdir:
        :param mock_exists:
        :return:
        """
        mock_listdir.return_value = ['test.csv']
        mock_exists.return_value = True

        with tempfile.TemporaryDirectory() as temp_dir:
            # pylint: disable=protected-access
            data_loader._sanitize_csv_headers_inplace(temp_dir)

        mock_file.assert_called_with(os.path.join(temp_dir, 'test.csv'), 'w')
        mock_file().writelines.assert_called_once_with(
            ['header1,header2,header3\n', 'row1,row2,row3'])

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_skips_non_csv_files(self, mock_listdir, mock_exists):
        """
        Assert _sanitize_csv_headers_inplace skips non-csv files.
        :param mock_listdir:
        :param mock_exists:
        :return:
        """
        mock_listdir.return_value = ['test.txt']
        mock_exists.return_value = True

        with tempfile.TemporaryDirectory() as temp_dir:
            # pylint: disable=protected-access
            data_loader._sanitize_csv_headers_inplace(temp_dir)

        mock_exists.assert_not_called()

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_skips_non_existent_files(self, mock_listdir, mock_exists):
        """
        Assert _sanitize_csv_headers_inplace skips non-existent files.
        :param mock_listdir:
        :param mock_exists:
        :return:
        """
        mock_listdir.return_value = ['test.csv']
        mock_exists.return_value = False

        with tempfile.TemporaryDirectory() as temp_dir:
            # pylint: disable=protected-access
            data_loader._sanitize_csv_headers_inplace(temp_dir)

        mock_exists.assert_called_once_with(os.path.join(temp_dir, 'test.csv'))

    @patch('os.listdir')
    def test_handles_empty_directory(self, mock_listdir):
        """
        Assert _sanitize_csv_headers_inplace handles empty directory.
        :param mock_listdir:
        :return:
        """
        mock_listdir.return_value = []

        with tempfile.TemporaryDirectory() as temp_dir:
            # pylint: disable=protected-access
            data_loader._sanitize_csv_headers_inplace(temp_dir)

        mock_listdir.assert_called_once_with(temp_dir)


if __name__ == '__main__':
    unittest.main()
