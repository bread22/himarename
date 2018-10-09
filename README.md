# himarename 整理喜马拉雅FM下载文件
Rename himalaya Windows 10 App downloads with actual track information, and update ID3 tags

Written in Python3, with mutagen


# 简介

Windows 10上的喜马拉雅FM下载文件是用数字命名，而且缺少ID3信息。

好在喜马拉雅是用json来保存下载信息，这个程序根据list.json提供的信息对下载的音频文件进行重命名和加上ID3信息，并复制或移动到目标文件夹。

整理后的文件方便保存和使用，方便不喜欢喜马拉雅FM app的用户（比如我）。


# 使用

- 更改config.ini内容，并将config.ini置于himarename.exe相同文件夹下
- 将HIMALAYA_DNLD_DIR指向喜马拉雅FM下载目录
- 将TARGET_DIR指向整理后的目录
- 运行himarename.exe