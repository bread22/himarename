"""


"""

import os
import json
import re
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.easymp4 import EasyMP4

__author__ = 'wuqingyi22@gmail.com'

HIMALAYA_DNLD_DIR = r'C:\Users\qingywu\Documents\temp\music'


def get_json_list(path):
    """ Get JSON file list

    Get a list of JSON files from given path

    :param path:                (str) a path to look for
    :return file_list:          (list) a list of file names (*list.json, created by himalaya) with absolute path
    """
    file_list = os.listdir(path)
    file_list = [os.path.join(path, fname) for fname in file_list
                 if os.path.isfile(os.path.join(path, fname)) and re.search(r'.*?list.json', fname)]

    return file_list


def parse_list_json(json_file):
    """
    Example for track info from json file:
    {
        "isDownloading": false,
        "downloadBarValue": 7379979.0,
        "downloadBarMaximum": 7379979.0,
        "downloadStatus": 1,
        "isLiked": false,
        "isFollowed": false,
        "isFavorited": false,
        "isLike": false,
        "isNew": false,
        "trackId": 69910711,
        "uid": 17133850,
        "playUrl64": "http://fdfs.xmcdn.com/group38/M02/CD/F6/wKgJolp0WWXw_w4wASMMlrf4i6M441.mp3",
        "playUrl32": "http://fdfs.xmcdn.com/group39/M06/D4/1A/wKgJnlp0dpKS5In8AJGGtkxGxDc972.mp3",
        "downloadUrl": "http://download.xmcdn.com/group39/M00/D2/B8/wKgJn1p0cJ2Q-MXRAJGIXaANddg929.aac",
        "playPathAacv164": "http://audio.xmcdn.com/group38/M02/CE/22/wKgJo1p0WVSgZohtASaDm4XcUGI691.m4a",
        "playPathAacv224": "http://audio.xmcdn.com/group38/M02/CE/22/wKgJo1p0WVHwk5hRAHCcC89uhJI399.m4a",
        "downloadAacUrl": "http://download.xmcdn.com/group38/M02/CE/22/wKgJo1p0WVHwk5hRAHCcC89uhJI399.m4a",
        "title": "宋徽宗之谜 15 囚徒生活之谜",
        "duration": 2384.2,
        "processState": 2,
        "createdAt": 1517576613000,
        "created_at": 1517576613000,
        "cover_path": "http://imagev2.xmcdn.com/group36/M04/9F/40/wKgJUlpLJ0vCJiltAAAOxTuTMfU358.jpg!op_type=3&columns=100&rows=100",
        "coverSmall": "http://imagev2.xmcdn.com/group36/M04/9F/40/wKgJUlpLJ0vCJiltAAAOxTuTMfU358.jpg!op_type=3&columns=100&rows=100",
        "coverMiddle": "http://fdfs.xmcdn.com/group36/M04/9F/40/wKgJUlpLJ0vCJiltAAAOxTuTMfU358_web_large.jpg",
        "coverLarge": "http://fdfs.xmcdn.com/group36/M04/9F/40/wKgJUlpLJ0vCJiltAAAOxTuTMfU358_mobile_large.jpg",
        "nickname": "有龍则靈",
        "smallLogo": "http://fdfs.xmcdn.com/group27/M02/1A/C8/wKgJW1kNWLrziHoUAAEZRGSEz78541_mobile_small.jpg",
        "userSource": 1,
        "albumId": 12375186,
        "albumTitle": "宋徽宗之谜",
        "albumImage": "http://imagev2.xmcdn.com/group36/M04/9F/40/wKgJUlpLJ0vCTEy7AAAOxTuTMfU150.jpg!op_type=5&upload_type=album&device_type=wp&name=medium",
        "orderNum": 14,
        "opType": 1,
        "isPublic": true,
        "likes": 3,
        "count_like": 3,
        "playTimes": 2427,
        "playtimes": 2427,
        "count_play": 2427,
        "comments": 0,
        "count_comment": 0,
        "shares": 0,
        "status": 1,
        "downloadSize": 9537629,
        "downloadAacSize": 7379979,
        "isRelay": false,
        "activityId": 0,
        "categoryId": 0,
        "refUid": 0,
        "id": 69910711,
        "updatedAt": 0,
        "favoritesCounts": 0,
        "playsCounts": 2427,
        "commentsCounts": 0,
        "sharesCounts": 0,
        "timeline": 1538679305014,
        "albumCoverSmall": "http://fdfs.xmcdn.com/group36/M04/9F/40/wKgJUlpLJ0vCTEy7AAAOxTuTMfU150_mobile_small.jpg",
        "downloadType": 0,
        "downloadTime": 0,
        "albumCoverMiddle": "http://fdfs.xmcdn.com/group36/M04/9F/40/wKgJUlpLJ0vCTEy7AAAOxTuTMfU150_mobile_meduim.jpg",
        "sequnceId": "92682057a06c45159d2e5bcb8cc7decb",
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
    :param json_file:       (str) a json file with absolute path
    :return tracks:         (dict) a dict with primary key is files names in input json_file
    """
    _eyed3_key_mapping = {
        'albumTitle': 'album',
        'title': 'title',
        'orderNum': 'tracknumber',
        'albumId': 'albumId',
        'trackId': 'filename'
    }

    with open(json_file, encoding='utf8') as fp:
        track_infos = json.load(fp)

    tracks = dict()
    for track in track_infos:
        single_track = tracks.setdefault(track['trackId'], dict())
        for k, v in _eyed3_key_mapping.items():
            single_track[v] = track[k]

    return tracks


def update_id3(fp, id3):
    """ Update file ID3 tag

    Try ID3 first, if not exist, try MP4, if still not exist, initialize an ID3.

    :param fp:          (str) file with absolute path
    :param id3:         (dict) ID3 info in dict format
    :return:
    """
    if os.path.isfile(fp):
        try:
            audio_file = EasyID3(fp)
            audio_file['tracknumber'] = id3.get('tracknumber')
        except mutagen.id3._util.ID3NoHeaderError:
            print('No ID3 available, try MP4')
            try:
                audio_file = EasyMP4(fp)
                audio_file['tracknumber'] = str(id3.get('tracknumber') + 1)
            except mutagen.mp4.MP4StreamInfoError:
                print('Not an MP4 file, create ID3 tag')
                audio_file = mutagen.File(fp, easy=True)
                audio_file.add_tags()

        audio_file['album'] = id3.get('album')
        audio_file['title'] = id3.get('title')
        audio_file.save()
    else:
        raise FileNotFoundError('Audio File {0} is not found'.format(fp))


def rename_with_id3(fp):
    """ Rename with ID3 info

    Read ID3 info from given audio file, and use ID3 info to rename it.

    format is track_num_title

    :param fp:          (str) audio file name with absolute path
    :return:
    """
    if os.path.isfile(fp):
        path = os.path.dirname(fp)
        ext = re.search(r'(.*)\.(\w+?)$', os.path.basename(fp)).group(2)
        try:
            audio_file = EasyID3(fp)
            new = '{0}_{1}.{2}'.format(audio_file['tracknumber'], audio_file['title'], ext)
        except mutagen.id3._util.ID3NoHeaderError:
            audio_file = EasyMP4(fp)
            new = '{0}_{1}.{2}'.format(audio_file['tracknumber'][0], audio_file['title'][0], ext)
        os.rename(fp, os.path.join(path, new))
        print('Renamed {0} to {1}'.format(os.path.basename(fp), new))
    else:
        raise FileNotFoundError('File {0} is not found'.format(fp))


def main():
    """ Main function
    1. Get all list.json file from HIMALAYA_DNLD_DIR
    2. Update and rename each file in album_path
    3. Rename album_path
    :return:
    """
    # 1. Get all list.json file from HIMALAYA_DNLD_DIR
    json_file_list = get_json_list(HIMALAYA_DNLD_DIR)
    for jfile in json_file_list:
        tracks = parse_list_json(jfile)
        album_path = os.path.join(HIMALAYA_DNLD_DIR, str(list(tracks.values())[0].get('albumId')))
        # 2. Update and rename each file in album_path
        for file_id3 in tracks.values():
            files = os.listdir(album_path)
            target_file = [fn for fn in files if re.match(str(file_id3.get('filename')), fn)][0]
            fp = os.path.join(album_path, target_file)
            update_id3(fp, file_id3)
            rename_with_id3(fp)
        # 3. Rename album_path
        os.rename(album_path, os.path.join(HIMALAYA_DNLD_DIR, str(list(tracks.values())[0].get('album'))))


main()
