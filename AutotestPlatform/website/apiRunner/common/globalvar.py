#!/usr/bin/env python
#-*-encoding:utf-8-*-

__author__ = 'shouke'

from ..common.othertools import OtherTools
from ..function.plugin import pluginfunc

db_related_to_project_dic = {}  # 存放与项目关联的数据库对象
redis_related_to_project_dic = {}  # 存放与项目关联的Redis对象

global_variable_dic = {}     # 存放与项目关联的全局变量

global_plugin_func_name_list = dir(pluginfunc) # 存放支持的插件函数
global_plugin_func_name_list = [item for item in global_plugin_func_name_list if not item.endswith('_') and (item.startswith('__') or item.startswith('_'))]

other_tools = OtherTools()

