"""
Unit tests for himarename.py
"""
import unittest
from unittest import mock
from unittest.mock import patch, mock_open, Mock
from pathlib import PurePath

import himarename
from himarename import get_json_list, parse_list_json, update_id3, rename_with_id3

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

    def test_parse_list_json(self):
        file_data = """[{
                        "isDownloading": false,
                        "downloadBarValue": 3899105.0,
                        "downloadBarMaximum": 3899105.0,
                        "downloadStatus": 1,
                        "isLiked": false,
                        "isFollowed": false,
                        "isFavorited": false,
                        "isLike": false,
                        "isNew": false,
                        "trackId": 25320005,
                        "uid": 10064765,
                        "playUrl64": "http://fdfs.xmcdn.com/group25/M08/4C/99/wKgJMVguYyLCnL98AJm9y0-aE_A444.mp3",
                        "playUrl32": "http://fdfs.xmcdn.com/group24/M05/4C/D3/wKgJMFguYxvA-mWtAEzfBQh4GdQ766.mp3",
                        "downloadUrl": "http://download.xmcdn.com/group22/M08/4C/F9/wKgJLlguaeGAK9ClAEzkTrQQ0FU751.aac",
                        "playPathAacv164": "http://audio.xmcdn.com/group25/M08/4C/99/wKgJMVguYyOTGmEAAJuWHsKKuek988.m4a",
                        "playPathAacv224": "http://audio.xmcdn.com/group23/M02/4C/F0/wKgJL1guY8Oh1YCkADt-4W9pFBo219.m4a",
                        "downloadAacUrl": "http://download.xmcdn.com/group23/M02/4C/F0/wKgJL1guY8Oh1YCkADt-4W9pFBo219.m4a",
                        "title": "话说宋朝161-机关算尽",
                        "duration": 1259.4,
                        "processState": 2,
                        "createdAt": 1479434993000,
                        "created_at": 1479434993000,
                        "cover_path": "http://imagev2.xmcdn.com/group16/M00/91/E2/wKgDaldfvZrRtYbRAAHGkIODx-0457.jpg!op_type=3&columns=100&rows=100",
                        "coverSmall": "http://imagev2.xmcdn.com/group16/M00/91/E2/wKgDaldfvZrRtYbRAAHGkIODx-0457.jpg!op_type=3&columns=100&rows=100",
                        "coverMiddle": "http://fdfs.xmcdn.com/group16/M00/91/E2/wKgDaldfvZrRtYbRAAHGkIODx-0457_web_large.jpg",
                        "coverLarge": "http://fdfs.xmcdn.com/group16/M00/91/E2/wKgDaldfvZrRtYbRAAHGkIODx-0457_mobile_large.jpg",
                        "nickname": "大宇茶馆",
                        "smallLogo": "http://fdfs.xmcdn.com/group9/M09/18/EC/wKgDYlbdeJbS6C81AAGipv1X_ak449_mobile_small.jpg",
                        "userSource": 1,
                        "albumId": 4520927,
                        "albumTitle": "话说宋朝",
                        "albumImage": "http://imagev2.xmcdn.com/group15/M03/90/90/wKgDZVdfvJ6QPUp6AAHGkIODx-0367.jpg!op_type=5&upload_type=album&device_type=wp&name=medium",
                        "orderNum": 160,
                        "opType": 1,
                        "isPublic": true,
                        "likes": 225,
                        "count_like": 225,
                        "playTimes": 146823,
                        "playtimes": 146823,
                        "count_play": 146823,
                        "comments": 86,
                        "count_comment": 86,
                        "shares": 0,
                        "status": 1,
                        "downloadSize": 5039182,
                        "downloadAacSize": 3899105,
                        "isRelay": false,
                        "activityId": 0,
                        "categoryId": 0,
                        "refUid": 0,
                        "id": 25320005,
                        "updatedAt": 0,
                        "favoritesCounts": 0,
                        "playsCounts": 146823,
                        "commentsCounts": 0,
                        "sharesCounts": 0,
                        "timeline": 1538949158637,
                        "albumCoverSmall": "http://fdfs.xmcdn.com/group15/M03/90/90/wKgDZVdfvJ6QPUp6AAHGkIODx-0367_mobile_small.jpg",
                        "downloadType": 0,
                        "downloadTime": 0,
                        "albumCoverMiddle": "http://fdfs.xmcdn.com/group15/M03/90/90/wKgDZVdfvJ6QPUp6AAHGkIODx-0367_mobile_meduim.jpg",
                        "sequnceId": "d26f2b37437c48f8876431e8cfbc29d6",
                        "isPaid": false,
                        "isFree": false,
                        "isAuthorized": false,
                        "priceTypeId": 0,
                        "price": 0.0,
                        "discountedPrice": 0.0,
                        "isVideo": false,
                        "isDraft": false,
                        "isRichAudio": false,
                        "type": 0,
                        "relatedId": 0,
                        "orderNo": 0,
                        "isHoldCopyright": false,
                        "canAccess": true
                    }, {
                        "isDownloading": false,
                        "downloadBarValue": 3987727.0,
                        "downloadBarMaximum": 3987727.0,
                        "downloadStatus": 1,
                        "isLiked": false,
                        "isFollowed": false,
                        "isFavorited": false,
                        "isLike": false,
                        "isNew": false,
                        "trackId": 25496548,
                        "uid": 10064765,
                        "playUrl64": "http://fdfs.xmcdn.com/group21/M07/56/E5/wKgJLVgyUNXDJPg-AJ09TdHbpzc266.mp3",
                        "playUrl32": "http://fdfs.xmcdn.com/group21/M07/56/E6/wKgJLVgyUNyR2sP8AE6exjJ93-A981.mp3",
                        "downloadUrl": "http://download.xmcdn.com/group22/M01/56/ED/wKgJLlgyUOyhd0xaAE6j_9xKtcs615.aac",
                        "playPathAacv164": "http://audio.xmcdn.com/group21/M07/56/E5/wKgJLVgyUNLCn39ZAJ8gIr7rpYg191.m4a",
                        "playPathAacv224": "http://audio.xmcdn.com/group21/M07/56/AE/wKgJKFgyUNChtkOJADzZD6GCLY4813.m4a",
                        "downloadAacUrl": "http://download.xmcdn.com/group21/M07/56/AE/wKgJKFgyUNChtkOJADzZD6GCLY4813.m4a",
                        "title": "话说宋朝162-死战不退",
                        "duration": 1288.06,
                        "processState": 2,
                        "createdAt": 1479692471000,
                        "created_at": 1479692471000,
                        "cover_path": "http://imagev2.xmcdn.com/group16/M00/91/E2/wKgDaldfvZrRtYbRAAHGkIODx-0457.jpg!op_type=3&columns=100&rows=100",
                        "coverSmall": "http://imagev2.xmcdn.com/group16/M00/91/E2/wKgDaldfvZrRtYbRAAHGkIODx-0457.jpg!op_type=3&columns=100&rows=100",
                        "coverMiddle": "http://fdfs.xmcdn.com/group16/M00/91/E2/wKgDaldfvZrRtYbRAAHGkIODx-0457_web_large.jpg",
                        "coverLarge": "http://fdfs.xmcdn.com/group16/M00/91/E2/wKgDaldfvZrRtYbRAAHGkIODx-0457_mobile_large.jpg",
                        "nickname": "大宇茶馆",
                        "smallLogo": "http://fdfs.xmcdn.com/group9/M09/18/EC/wKgDYlbdeJbS6C81AAGipv1X_ak449_mobile_small.jpg",
                        "userSource": 1,
                        "albumId": 4520927,
                        "albumTitle": "话说宋朝",
                        "albumImage": "http://imagev2.xmcdn.com/group15/M03/90/90/wKgDZVdfvJ6QPUp6AAHGkIODx-0367.jpg!op_type=5&upload_type=album&device_type=wp&name=medium",
                        "orderNum": 161,
                        "opType": 1,
                        "isPublic": true,
                        "likes": 232,
                        "count_like": 232,
                        "playTimes": 137500,
                        "playtimes": 137500,
                        "count_play": 137500,
                        "comments": 117,
                        "count_comment": 117,
                        "shares": 0,
                        "status": 1,
                        "downloadSize": 5153791,
                        "downloadAacSize": 3987727,
                        "isRelay": false,
                        "activityId": 0,
                        "categoryId": 0,
                        "refUid": 0,
                        "id": 25496548,
                        "updatedAt": 0,
                        "favoritesCounts": 0,
                        "playsCounts": 137500,
                        "commentsCounts": 0,
                        "sharesCounts": 0,
                        "timeline": 1538949167376,
                        "albumCoverSmall": "http://fdfs.xmcdn.com/group15/M03/90/90/wKgDZVdfvJ6QPUp6AAHGkIODx-0367_mobile_small.jpg",
                        "downloadType": 0,
                        "downloadTime": 0,
                        "albumCoverMiddle": "http://fdfs.xmcdn.com/group15/M03/90/90/wKgDZVdfvJ6QPUp6AAHGkIODx-0367_mobile_meduim.jpg",
                        "sequnceId": "b8fa1540add547939e5b794899ba3709",
                        "isPaid": false,
                        "isFree": false,
                        "isAuthorized": false,
                        "priceTypeId": 0,
                        "price": 0.0,
                        "discountedPrice": 0.0,
                        "isVideo": false,
                        "isDraft": false,
                        "isRichAudio": false,
                        "type": 0,
                        "relatedId": 0,
                        "orderNo": 0,
                        "isHoldCopyright": false,
                        "canAccess": true
                    }
                ]"""
        with patch("builtins.open", mock_open(read_data=file_data)) as mock_file:
            result = parse_list_json('some_file')
            correct_result = {
                25320005: {
                    'filename': 25320005, 'albumId': 4520927, 'tracknumber': 160,
                    'title': "话说宋朝161-机关算尽", 'album': '话说宋朝'},
                25496548: {
                    'filename': 25496548, 'albumId': 4520927, 'tracknumber': 161,
                    'title': '话说宋朝162-死战不退', 'album': '话说宋朝'}
            }
            mock_file.assert_called_with('some_file', encoding='utf8')
            self.assertEqual(result, correct_result)

    @mock.patch('himarename.mutagen.File')
    @mock.patch('himarename.EasyMP4')
    @mock.patch('himarename.EasyID3')
    @mock.patch('himarename.Path.is_file')
    def test_update_id3(self, mock_path_isfile, mock_easyid3, mock_easymp4, mock_mutagen_file):
        id3 = {'album': '', 'title': '', 'tracknumber': 0}

        mock_path_isfile.return_value = False
        self.assertRaises(SystemExit, update_id3, 'some_file', id3)

        mock_path_isfile.return_value = True
        update_id3('some_file', id3)
        mock_easyid3.assert_called_with('some_file')
        mock_easyid3.return_value.save.assert_called()

        mock_easyid3.side_effect = himarename.mutagen.id3._util.ID3NoHeaderError()
        update_id3('some_file', id3)
        mock_easymp4.assert_called_with('some_file')
        mock_easymp4.return_value.save.assert_called()

        mock_easyid3.side_effect = himarename.mutagen.id3._util.ID3NoHeaderError()
        mock_easymp4.side_effect = himarename.mutagen.mp4.MP4StreamInfoError()
        audio_file = mock_mutagen_file.return_value
        audio_file.add_tags.return_value = dict()
        update_id3('some_file', id3)
        mock_mutagen_file.assert_called_with('some_file', easy=True)
        mock_mutagen_file.return_value.save.assert_called()

    @mock.patch('himarename.os.remove')
    @mock.patch('himarename.os.rename')
    @mock.patch('himarename.EasyMP4')
    @mock.patch('himarename.EasyID3')
    @mock.patch('himarename.Path.is_file')
    def test_rename_with_id3(self, mock_path_isfile, mock_easyid3, mock_easymp4, mock_osrename, mock_osremove):
        fp = PurePath('some_file')

        mock_path_isfile.return_value = False
        self.assertRaises(SystemExit, rename_with_id3, fp)

        mock_path_isfile.return_value = True
        rename_with_id3(fp)
        mock_easyid3.assert_called_with(fp)
        mock_osrename.assert_called()

        mock_easyid3.side_effect = himarename.mutagen.id3._util.ID3NoHeaderError()
        rename_with_id3(fp)
        mock_easymp4.assert_called_with(fp)
        mock_osrename.assert_called()

        mock_osrename.side_effect = FileExistsError()
        self.assertRaises(FileExistsError, rename_with_id3, fp)
        mock_easymp4.assert_called_with(fp)
        mock_osrename.assert_called()
        mock_osremove.assert_called()
