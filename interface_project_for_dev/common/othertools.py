#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import os
import re

class OtherTools:
    def __init__(self):
        pass

    # 批量创建目录
    def mkdirs_once_many(self, path):
        path = os.path.normpath(path)  # 去掉路径最右侧的 \\ 、/
        path = path.replace('\\', '/') # 将所有的\\转为/，避免出现转义字符串

        head, tail = os.path.split(path)
        new_dir_path = ''  # 反转后的目录路径
        root = ''  #根目录

        if not os.path.isdir(path) and os.path.isfile(path):  # 如果path指向的是文件，则继续分解文件所在目录
            head, tail = os.path.split(head)

        if tail == '':
            return

        while tail:
            new_dir_path = new_dir_path + tail + '/'
            head, tail = os.path.split(head)
            root = head
        else:
            new_dir_path = root + new_dir_path
            # print(new_dir_path)

            # 批量创建目录
            new_dir_path = os.path.normpath(new_dir_path)
            head, tail = os.path.split(new_dir_path)
            temp = ''
            while tail:
                temp = temp + '/' + tail
                dir_path = root + temp
                if not os.path.isdir(dir_path):
                    os.mkdir(dir_path)
                head, tail = os.path.split(head)

    # 获取给定字典的key,value的list表示，形如[key_level1,key_level2,key_level3, ..., key_final_level, value_of_key_final_level]
    # 仅支持这样的字典： {"goods_type2":{"goods_name":"redapple"}}, 即每个层级只有一个key的字典
    def get_dict_level_list(self, pattern_dic):
        dict_level_list = []
        def get_dic_level(dic):
            nonlocal dict_level_list

            for key in dic.keys():
                value = dic.get(key)
                dict_level_list.append(key)  #用于存放层级及key值
                if type(value) == type({}):
                    get_dic_level(value)
                else:
                    dict_level_list.append(value)

        get_dic_level(pattern_dic)

        return dict_level_list

    # 根据get_dict_level_list函数返回的dict_level_list，在目标字典中查找 key_final_level对应的值
    def find_value_of_dic_key_final_level(self, dict_level_list, target_dict):
        key_index = 0
        def find_value_of_key_final_level(dict_level_list, target_dict):
            nonlocal  key_index
            keys_num = len(dict_level_list) -1 # 获取字典键的数量，dict_level_list中最后一个是字典的值

            # 在字典中查找对应层级，对应key的value值
            for key_level in dict_level_list[key_index: keys_num]:
                result = target_dict.get(key_level)
                if type(result) == type([]): # 获取的值为列表，形如[{"goodsId":1,"goods_name":"apple"},{"goodsId":2,"goods_name":"apple"}]
                    # 遍历列表,每个字典中查找
                    key_index = key_index + 1 # 进入到第二个层级，控制 取第二层级的key，在目标字典中查找
                    for dic_item in result:
                        result = find_value_of_key_final_level(dict_level_list, dic_item)
                        if result != None: # 找到了
                            break
                elif type(result) == type({}): # 获取的值为字典，形如{"goodsId":1,"goods_name":"apple"}
                    # 在该字典中查找
                    self.key_index = self.key_index + 1
                    result = find_value_of_key_final_level(dict_level_list, result)
                return  result

        return find_value_of_key_final_level(dict_level_list, target_dict)
#
# dic = {"goods_type2":{"goods_name":"redapple"}}
# tar = {
#     "fullname": "tester",
#     "goods_type1": [
#         {
#             "goodsId": 1,
#             "goods_name": "apple"
#         },
#         {
#             "goodsId": 2,
#             "goods_name": "apple"
#         }
#     ],
#     "goods_type2": [
#         {
#             "goodsId": 1,
#             "goods_name": "redapple"
#         },
#                 {
#             "goodsId": 1,
#             "goods_name": "redapple3"
#         }
#     ],
#     "goods_type3": {
#         "goodsId": 7
#     },
#     "goods_type4": 7,
#     "price": {
#         "apple": 10.5,
#         "pear": 8
#     }
# }
# print(OtherTools().find_value_of_dic_key_final_level(OtherTools().get_dict_level_list(dic), tar))
#
#
#
#
#
#
#
#


