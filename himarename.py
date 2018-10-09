"""


"""

import os
import json
import re
import configparser
import sys
import shutil
import logging
from pathlib import Path, PurePath

import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.easymp4 import EasyMP4

__author__ = 'wuqingyi22@gmail.com'
__version__ = '0.5.1'

logger = logging.getLogger(__name__)
config_ini = 'config.ini'


def get_json_list(path):
    """ Get JSON file list

    Get a list of JSON files from given path

    :param path:                (str) a path to look for
    :return file_list:          (list) a list of file names (*list.json, created by himalaya) with absolute path
    """
    file_list = os.listdir(path)
    file_list = [PurePath(path).joinpath(fname) for fname in file_list
                 if Path(PurePath(path).joinpath(fname)).is_file() and re.search(r'.*?list.json', fname)]

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
    :param json_file:       (Path) a json file with absolute path
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

    :param fp:          (Purepath) file with absolute path
    :param id3:         (dict) ID3 info in dict format
    :return:
    """
    logger.info('Updating ID3 for {0}'.format(fp))
    if Path(fp).is_file():
        try:
            audio_file = EasyID3(fp)
            audio_file['tracknumber'] = id3.get('tracknumber')
        except mutagen.id3._util.ID3NoHeaderError:
            logger.warning('No ID3 available, try MP4')
            try:
                audio_file = EasyMP4(fp)
                audio_file['tracknumber'] = str(id3.get('tracknumber') + 1)
            except mutagen.mp4.MP4StreamInfoError:
                logger.warning('Not an MP4 file, create ID3 tag')
                audio_file = mutagen.File(fp, easy=True)
                audio_file.add_tags()

        audio_file['album'] = id3.get('album')
        audio_file['title'] = id3.get('title')
        audio_file.save()
    else:
        raise SystemExit('Audio File {0} is not found'.format(fp))


def rename_with_id3(fp):
    """ Rename with ID3 info

    Read ID3/MP4 info from given audio file, and use ID3/MP4 info to rename it.

    format is tracknum_title

    :param fp:          (Purepath) audio file name with absolute path
    :return:
    """
    if Path(fp).is_file():
        try:
            audio_file = EasyID3(fp)
            new_name = '{0}_{1}{2}'.format(audio_file['tracknumber'], audio_file['title'], fp.suffix)
        except mutagen.id3._util.ID3NoHeaderError:
            audio_file = EasyMP4(fp)
            new_name = '{0}_{1}{2}'.format(audio_file['tracknumber'][0], audio_file['title'][0], fp.suffix)
        try:
            os.rename(fp, fp.parent.joinpath(new_name))
        except FileExistsError:
            msg = 'File {0} exists, overwirting.'.format(new_name)
            print(msg)
            logger.warning(msg)
            os.remove(fp.parent.joinpath(new_name))
            os.rename(fp, fp.parent.joinpath(new_name))

        logger.info('Renamed {0} to {1}'.format(fp, fp.parent.joinpath(new_name)))
    else:
        raise SystemExit('File {0} is not found'.format(fp))


def copy_file_to_tgt(src, dst, move=False):
    """ Copy file to target dir

    :param src:         (Purepath) source file
    :param dst:         (Purepath) destination file
    :param move:        (bool) whether to keep source file
    :return ret:        (bool) True if copy/move succeed, False otherwise
    """
    ret = True
    if src == dst:
        return ret

    try:
        if not move:
            shutil.copy(src, dst)
        else:
            shutil.move(src, dst)
    except OSError:
        logger.warning('Target file {0} is not writable'.format(dst))
        ret = False
    return ret


def load_config():
    """ Load configuration from config_ini

    :return himalaya_download_dir:  (str) path to himalaya download folder
    :return target_dir:             (str) path to folder that contains renamed files
    :return keep_original:          (bool) whether to keep original files in himalaya_download_dir

    """
    # Load configs from .ini file
    if not Path(config_ini).is_file():
        msg = '{0} is not found.'.format(config_ini)
        print(msg)
        logger.error(msg)
        raise SystemExit(msg)
    config = configparser.ConfigParser()
    try:
        config.read(config_ini)
    except configparser.MissingSectionHeaderError:
        msg = '{0} format is invalid, must have [DEFAULT] section'.format(config_ini)
        print(msg)
        logger.error(msg)
        raise SystemExit(msg)

    try:
        himalaya_download_dir = config.get('DEFAULT', 'HIMALAYA_DNLD_DIR')
        target_dir = config.get('DEFAULT', 'TARGET_DIR', fallback=himalaya_download_dir)
        keep_original = config.getboolean('DEFAULT', 'KEEP_ORIGINAL', fallback=True)
        verbose = config.getboolean('DEFAULT', 'VERBOSE', fallback=True)
    except KeyError as err:
        logger.error('Missing key in {0}'.format(config_ini))
        logger.error(err)
        raise SystemExit(str(err))

    # Process configuration to find errors
    if not Path(himalaya_download_dir).is_dir():
        msg = '{0} is no a valid folder'.format(Path(himalaya_download_dir))
        print(msg)
        logger.error(msg)
        raise SystemExit(msg)
    if target_dir == himalaya_download_dir and keep_original:
        msg = 'You must assign a different TARGET_DIR if you want to keep original files.'
        print(msg)
        logger.error(msg)
        raise SystemExit(msg)

    return Path(himalaya_download_dir), Path(target_dir), keep_original, verbose


def main():
    """ Main function
    1. Get all list.json file from himalaya_download_dir
    2. Update and rename each file in album_path
    3. Rename album_path
    :return:
    """

    logging.basicConfig(format='[%(asctime)s] [%(levelname)s]: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.INFO,
                        handlers=[logging.FileHandler('logfile.log', 'w', 'utf-8')])

    himalaya_download_dir, target_dir, keep_original, verbose = load_config()

    sys.stdout = open(os.devnull, mode='w', encoding='utf-8') if not verbose else sys.stdout

    # 1. Get all list.json file from himalaya_download_dir
    json_file_list = get_json_list(himalaya_download_dir)
    os.makedirs(target_dir, exist_ok=True)
    for jfile in json_file_list:
        tracks = parse_list_json(jfile)
        album_path = PurePath(himalaya_download_dir).joinpath(str(list(tracks.values())[0].get('albumId')))
        if not Path(album_path).is_dir():
            logger.warning('Source folder {0} does not exist.'.format(album_path))
            continue
        album_path_tgt = PurePath(target_dir).joinpath(str(list(tracks.values())[0].get('album')))
        os.makedirs(album_path_tgt, exist_ok=True)
        # 2. Copy/Move each file in album_path to album_path_tgt
        for file_id3 in tracks.values():
            files = os.listdir(album_path)
            try:
                src_file = [fn for fn in files if PurePath(fn).stem == file_id3.get('filename')][0]
            except IndexError:
                msg = 'File {0} does not exist, skip it.'.format(file_id3.get('filename'))
                logger.warning(msg)
                continue
            src_fp = album_path.joinpath(src_file)
            tgt_fp = album_path_tgt.joinpath(src_file)
            copy_file_to_tgt(src_fp, tgt_fp)
            # 3. Update ID3/MP4 for tgt_fp, and rename it accordingly
            update_id3(tgt_fp, file_id3)
            rename_with_id3(tgt_fp)
        # 4. Delete original files
        if not keep_original:
            shutil.rmtree(album_path)


if __name__ == "__main__":
    main()
