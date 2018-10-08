"""
Unit tests for himarename.py
"""
import unittest
from unittest import mock
from pathlib import PurePath
from himarename import get_json_list

__author__ = 'wuqingyi22@gmail.com'
__version__ = '0.1.0'


class HimalayaRenamerTestCase(unittest.TestCase):

    @mock.patch('himarename.Path.is_file')
    @mock.patch('himarename.os')
    def test_get_json_list(self, mock_os, mock_path_isfile):

        mock_path_isfile.return_value = True
        mock_os.listdir.return_value = ['abc.def', '1214314list.json', '12313info.json', '1sadfa4list.json']
        files = get_json_list('any_path')
        mock_os.listdir.assert_called_with('any_path')

        assert files == [PurePath('any_path').joinpath('1214314list.json'),
                         PurePath('any_path').joinpath('1sadfa4list.json')]
