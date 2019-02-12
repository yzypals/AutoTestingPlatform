#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'laifuyu'

import os

class Tools:
    def __init__(self):
        pass

    # 获取目录下的文件
    def get_files_in_dirpath(self, dirpath):
        file_list_for_dirpath = []
        # 收集目录下的所有文件
        def collect_files_in_dirpath(dirpath):
            nonlocal file_list_for_dirpath
            if not os.path.exists(dirpath):
                print('路径：%s 不存在，退出程序' % dirpath)
                exit()
            for name in os.listdir(dirpath):
                full_path = os.path.join(dirpath, name)
                if os.path.isdir(full_path):
                    collect_files_in_dirpath(full_path)
                else:
                    file_list_for_dirpath.append(full_path)
        collect_files_in_dirpath(dirpath)
        return file_list_for_dirpath

