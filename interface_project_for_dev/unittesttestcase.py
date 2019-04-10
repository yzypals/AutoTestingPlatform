#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import  unittest
import json
import re
import copy
import xml.etree.ElementTree as ET

from common.log import logger
from common.globalvar import other_tools
from common.globalvar import global_variable_dic

class MyUnittestTestCase(unittest.TestCase):
    def __init__(self,op_object, request_headers, request_method, url_or_sql, input_params, check_rule,
                check_pattern, response_to_check, output_params, http, case_step, methodName='runTest'):
        super(MyUnittestTestCase, self).__init__(methodName)
        self.op_object = op_object
        self.request_headers = request_headers
        self.request_method = request_method
        self.url_or_sql = url_or_sql
        self.input_params = input_params
        self.check_rule = check_rule
        self.check_pattern = check_pattern
        self.response_to_check = response_to_check
        self.output_params = output_params
        self.http = http
        self.case_step = case_step

    # 断言
    def assert_result(self, response_to_check):
        check_pattern = copy.deepcopy(self.check_pattern)
        if type(self.check_pattern) == type(''): # 如果是字符串，说明是第一次运行，否则说明非第一次运行，比如失败后重试，或者循环执行
            if self.check_pattern:
                logger.info('正在替换“校验模式”中的动态参数')
                self.check_pattern = self.case_step.replace_variable(self.check_pattern)

                logger.info('正在替换“校验模式”中的插件函数')
                self.check_pattern = self.case_step.replace_plugin_func(self.check_pattern)[0]
                try:
                    self.check_pattern = eval(self.check_pattern)
                except Exception as e:
                    logger.error('校验模式:\n%s \n填写错误：%s，停止断言输出' % (self.check_pattern, e))
                    self.assertEqual(1, 0, msg='fail#%s' % e)
                    return

                self.case_step.set_check_pattern(self.check_pattern)

        if self.check_rule == '':
            logger.warn('没有配置校验规则，返回程序')
            return
        elif self.check_rule != '':
            if self.check_rule == '包含成员':
                if type(response_to_check) not in [type(''), type([]), type(()), type(set()), type({})]:
                    logger.error('服务器返回内容为不可迭代对象')
                    self.assertEqual(1, 0, msg='fail#服务器返回内容为不可迭代对象')

                for item in self.check_pattern:
                    member = item['模式']
                    logger.info('校验规则为“包含成员：%s”' % member)
                    self.assertIn (member, response_to_check, msg=item['消息'])

            elif self.check_rule == '不包含成员':
                if type(response_to_check) not in [type(''), type([]), type(()), type(set()), type({})]:
                    logger.error('服务器返回内容为不可迭代对象')
                    self.assertEqual(1, 0, msg='fail#服务器返回内容为不可迭代对象')

                for item in self.check_pattern:
                    member = item['模式']
                    logger.info('校验规则为：“不包含成员：%s”' % member)
                    self.assertNotIn (member, response_to_check, msg=item['消息'])

            elif self.check_rule == '包含字符串':
                if type(response_to_check) in [type({}), type(set()), type(()), type([]), type(1), type(0.01)]:
                    response_to_check = str(response_to_check)
                elif type(response_to_check) != type(''):
                    logger.error('服务器返回内容不能转换为字符串')
                    self.assertEqual(1, 0, msg='fail#服务器返回内容不能转换为字符串')

                for item in self.check_pattern:
                    pattern_str = item['模式']
                    logger.info('校验规则为：“包含字符串：%s”' % pattern_str)
                    self.assertIn(pattern_str, response_to_check, item['消息'])

            elif self.check_rule == '不包含字符串':
                if type(response_to_check) in [type({}), type(set()), type(()), type([]), type(1), type(0.01)]:
                    response_to_check = str(response_to_check)
                elif type(response_to_check) != type(''):
                    logger.error('服务器返回内容不能转换为字符串')
                    self.assertEqual(1, 0, msg='fail#服务器返回内容不能转换为字符串')

                for item in self.check_pattern:
                    pattern_str = item['模式']
                    logger.info('校验规则为：“不包含字符串：%s”' % pattern_str)
                    self.assertNotIn(pattern_str, response_to_check, item['消息'])

            elif self.check_rule == '键值相等':
                if type(response_to_check) == type(''): # 字符串类型的字典、json串
                    try:
                        response_to_check = json.loads(response_to_check) # //转字符串为json
                    except Exception as e:
                        logger.error('服务器返回内容为不能转为json格式的字符串')
                        self.assertEqual(1, 0 ,msg='fail#服务器返回内容为不能转为json格式的字符串')
                elif type(response_to_check) == type([]): # 格式[{}]的json串
                    try:
                        response_to_check = response_to_check[0]
                        response_to_check = json.loads(response_to_check) # //转字符串为json
                    except Exception as e:
                        logger.error('服务器返回内容为不能转为json格式的列表')
                        self.assertEqual(1, 0 , msg='fail#服务器返回内容为不能转为json格式的列表')
                elif type(response_to_check) != type({}):
                    logger.error('服务器返回内容不能转为json格式')
                    self.assertEqual(1, 0, msg='fail#服务器返回内容不能转为json格式')

                for item in self.check_pattern:
                    pattern_dic = item['模式']
                    # 获取list方式标识的key,value层级值
                    dict_level_list = other_tools.get_dict_level_list(pattern_dic)

                    logger.info('要匹配的字典key,value层级为：%s' % dict_level_list)

                    last_value = other_tools.find_value_of_dic_key_final_level(dict_level_list, response_to_check)
                    logger.info('找到的对应字典层级的最后值为：%s' % last_value)

                    # 比较同层级，相同key对应的value值
                    self.assertEqual(dict_level_list[len(dict_level_list) -1], last_value, item['消息'])

            elif self.check_rule == '匹配正则表达式':
                if type(response_to_check) in [type({}), type(set()), type(()), type([]), type(1), type(0.01)]:
                    response_to_check = str(response_to_check)
                elif type(response_to_check) != type(''):
                    logger.error('服务器返回内容不能转换为字符串')
                    self.assertEqual(1, 0, msg='fail#服务器返回内容不能转换为字符串')

                for item in self.check_pattern:
                    pattern_str = item['模式']
                    pattern = re.compile(pattern_str)

                    logger.info('校验规则为：“匹配正则表达式：%s”' % pattern)
                    self.assertRegex(response_to_check, pattern, msg=item['消息'])

            elif self.check_rule == '不匹配正则表达式':
                if type(response_to_check) in [type({}), type(set()), type(()), type([]), type(1), type(0.01)]:
                    response_to_check = str(response_to_check)
                elif type(response_to_check) != type(''):
                    logger.error('服务器返回内容不为转换为字符串')
                    self.assertEqual(1, 0, msg='fail#服务器返回内容不能转换为字符串')

                for item in self.check_pattern:
                    pattern_str = item['模式']

                    logger.info('校验规则为：“不匹配正则表达式：%s”' % pattern_str)
                    self.assertNotRegex(response_to_check, pattern_str, msg=item['消息'])

            elif self.check_rule == '完全匹配字典':
                if type(response_to_check) == type(''): # 字符串类型的字典、json串
                    try:
                        response_to_check = json.loads(response_to_check) # //转字符串为json
                    except Exception as e:
                        logger.info('服务器返回内容为不能转为json格式的字符串')
                        self.assertEqual(1, 0 , msg='fail#服务器返回内容为不能转为json格式的字符串')
                if type(response_to_check) != type({}):
                    logger.error('服务器返回内容不为字典、字符串类型的字典')
                    self.assertEqual(1, 0 , msg='fail#服务器返回内容不为字典、字符串类型的字典')

                # 遍历条件列表 "条件":[{"模式":{"success":true}, "消息":"创建储值卡支付订单失败,返回结果和字典模式不匹配"}]
                for item in self.check_pattern:
                    pattern_dic = item['模式']
                    logger.info('校验规则为：“完全匹配字典：%s”' % pattern_dic)
                    self.assertDictEqual (response_to_check, pattern_dic, msg=item['消息'])

            elif self.check_rule == '完全匹配列表':
                if type(response_to_check) == type(''): # 字符串类型的列表
                    try:
                        response_to_check = eval(response_to_check)
                    except Exception as e:
                        logger.info('服务器返回内容为不能转换为列表的字符串')
                        self.assertEqual(1, 0 ,msg='fail#服务器返回内容不能转换为列表的字符串')
                if type(response_to_check) != type([]):
                    logger.info('服务器返回内容不为列表、字符串类型的列表')
                    self.assertEqual(1, 0, msg='fail#服务器返回内容不为列表、字符串类型的列表')

                for item in self.check_pattern:
                    pattern_list = item['模式']

                    logger.info('校验规则为：“完全匹配列表：%s”' % pattern_list)
                    self.assertListEqual (response_to_check, pattern_list, msg=item['消息'])

            elif self.check_rule == '完全匹配集合':
                if type(response_to_check) == type(''): # 字符串类型的集合
                    try:
                        response_to_check = eval(response_to_check)
                    except Exception as e:
                        logger.error('服务器返回内容为不能转换为集合的字符串')
                        self.assertEqual(1, 0 ,msg='fail#服务器返回内容为不能转换为集合的字符串')

                if type(response_to_check) != type(set()):
                    logger.error('服务器返回内容不为集合、字符串类型的集合')
                    self.assertEqual(1, 0, msg='fail#服务器返回内容不为集合、字符串类型的集合')

                for item in self.check_pattern:
                    pattern_set = item['模式']

                    logger.info('校验规则为：“完全匹配集合：%s' % pattern_set)
                    self.assertSetEqual (response_to_check, pattern_set, msg=item['消息'])

            elif self.check_rule == '完全匹配元组':
                if type(response_to_check) == type(''): # 字符串类型的元组
                    try:
                        response_to_check = eval(response_to_check)
                    except Exception as e:
                        logger.error('服务器返回内容为不能转换为元组的字符串')
                        self.assertEqual(1, 0 , msg='fail#服务器返回内容为不能转换为元组的字符串')

                if type(response_to_check) != type(()):
                    logger.error('服务器返回内容不为元组、字符串类型的元组')
                    self.assertEqual(1, 0, msg='fail#服务器返回内容不为元组、字符串类型的元组')

                for item in self.check_pattern:
                    pattern_tuple = item['模式']

                    logger.info('校验规则为：“完全匹配元组：%s”' % str(pattern_tuple))
                    self.assertTupleEqual(response_to_check, pattern_tuple, msg=item['消息'])
            elif self.check_rule == 'xpath断言':
                try:
                    root = ET.fromstring(response_to_check)
                except ET.ParseError as e:
                    logger.error('获取xml根节点失败')
                    self.assertEqual(1, 0, '%s' % e )

                for item in self.check_pattern:
                    pattern_dic = item['模式']
                    logger.info('校验规则为：“xpath断言：%s' % pattern_dic)
                    for key in pattern_dic.keys():
                        if key == '.':
                            content_to_check = root.text
                            expect_value = pattern_dic[key]
                        else:
                            xmlnsnamespace_dic = {}  # 存放 名称空间的定义
                            logger.info('正在获取xmlns定义')
                            match_result_list =re.findall('xmlns[^:]?=(.+?)[ |\>|\\\>]', response_to_check, re.MULTILINE)
                            if match_result_list:
                                xmlns = match_result_list[len(match_result_list) - 1]
                                xmlns = xmlns.strip(' ')
                                xmlns = '{' + xmlns + '}'
                                logger.info('xmlns定义为：%s' % xmlns)
                                xmlnsnamespace_dic['xmlns'] = xmlns

                            logger.info('正在获取"xmlns:xxx名称空间定义')
                            match_result_list = re.findall('xmlns:(.+?)=(.+?)[ |>]', response_to_check)
                            for ns in match_result_list:
                                xmlnsnamespace_dic[ns[0]] = '{' + ns[1] + '}'

                            logger.info("最后获取的prefix:uri为：%s" % xmlnsnamespace_dic)

                            logger.info('正在转换元素结点前缀')
                            key_copy = key
                            for dic_key in xmlnsnamespace_dic.keys():
                                namespace = dic_key + ':'
                                if namespace in key:
                                    uri = xmlnsnamespace_dic[dic_key]
                                    key = key.replace(namespace, uri)
                                    key = key.replace('"','')

                            logger.info('转换后用于查找元素的xpath：%s' % key)
                            try:
                                elements_list = root.findall(key)
                            except Exception as e:
                                logger.error('查找元素出错：%s' % e)
                                self.assertEqual(1, 0, msg='%s' % e)
                            logger.info('查找到的元素为：%s' % elements_list)

                            logger.info('正在进行断言')
                            if elements_list:
                                content_to_check = elements_list[0].text
                            else:
                                content_to_check = ''
                            expect_value = pattern_dic[key_copy]
                        logger.info('从服务器返回的提取的待检查数据的类型：%s' % type(content_to_check))
                        logger.info('用户期望值的数据类型：%s' % type(expect_value))
                        self.assertEqual(content_to_check, expect_value, msg=item['消息'])
            elif self.check_rule == 'db列值相等':
                for item in self.check_pattern:
                    member = item['模式']
                    logger.info('要检测的模式为：%s' % member)
                    self.assertEqual(member[0], member[1], msg = item['消息'])
            elif self.check_rule == 'db列值不相等':
                for item in self.check_pattern:
                    member = item['模式']
                    logger.info('要检测的模式为：%s' % member)
                    self.assertNotEqual(member[0], member[1], msg = item['消息'])

    # 按给定的 提取器，从web服务器返回内容中提取想要的内容
    def extrator(self, extrator_type, extrator, response_to_check=''):
        if extrator_type == 'dic': # 获取键值
            #  获取list方式标识的key,value层级值
            dict_level_list = other_tools.get_dict_level_list(extrator)

            logger.info('要提取的字典key,value层级为：%s' % dict_level_list)

            if type(response_to_check) == type(''): # 字符串类型的字典、json串
                try:
                    response_to_check = json.loads(response_to_check) # //转字符串为json
                except Exception as e:
                    logger.error('转换服务器返回内容为字典失败：%s' % e)
                    return ''

            if type(response_to_check) != type({}):
                logger.error('服务器返回内容不为字典、字符串类型的字典')
                return ''

            value_get = other_tools.find_value_of_dic_key_final_level(dict_level_list, response_to_check)
            logger.info('找到的对应字典层级key的值为：%s' % value_get)

            return value_get
        elif extrator_type  == 're': # 获取正则表达式匹配的内容
            if type(response_to_check) in [type({}), type(set()), type(()), type([]), type(1), type(0.01)]:
                response_to_check = str(response_to_check)
            elif type(response_to_check) != type(''):
                logger.error('服务器返回内容不能转为字符串')
                return []
            result = re.findall(extrator, response_to_check)
            return  result
        elif extrator_type == 'xpath':
            try:
                root = ET.fromstring(response_to_check)
            except ET.ParseError as e:
                logger.error('%s' % e)
                return []

            logger.info('xpath表达式为：%s' % extrator)
            if extrator == '.':
                value_get = [root.text]
            else:
                xmlnsnamespace_dic = {}  # 存放 前缀:对应uri
                logger.info('正在获取xmlns定义')
                match_result_list =re.findall('xmlns[^:]?=(.+?)[ |\>|\\\>]', response_to_check, re.MULTILINE)
                if match_result_list:
                    xmlns = match_result_list[len(match_result_list) - 1]
                    xmlns = xmlns.lstrip(' ')
                    xmlns = '{' + xmlns + '}'
                    logger.info('xmlns定义为：%s' % xmlns)
                    xmlnsnamespace_dic['xmlns'] = xmlns

                logger.info('正在获取"xmlns:xxx名称空间定义')
                match_result_list = re.findall('xmlns:(.+?)=(.+?)[ |>]', response_to_check)
                for ns in match_result_list:
                    xmlnsnamespace_dic[ns[0]] = '{' + ns[1] + '}'

                logger.info("最后获取的prefix:uri为：%s" % xmlnsnamespace_dic)

                logger.info('正在转换元素结点前缀')
                for dic_key in xmlnsnamespace_dic.keys():
                    namespace = dic_key + ':'
                    if namespace in extrator:
                        uri = xmlnsnamespace_dic[dic_key]
                        extrator = extrator.replace(namespace, uri)
                        extrator = extrator.replace('"','')

                logger.info('转换后用于查找元素的xpath：%s' % extrator)
                elements_list = []
                try:
                    elements_list = root.findall(extrator)
                except Exception as e:
                    logger.error('查找xpath元素出错:%s' % e)
                logger.info('查找到的元素为：%s' % elements_list)
                if elements_list:
                    value_get = elements_list
                else:
                    value_get = []
            return value_get
        else:
            logger.error('提取器填写错误')
            return []

    # 保存从服务器返回中提取的内容
    def save_result(self, response_to_check):
        if type(self.output_params) == type({}):
            for key in self.output_params.keys():
                key = key.lower()
                if key == 'dic': # 如果为字典,则用键值提取
                    for var_name, extrator in self.output_params[key].items():
                        logger.info('使用键值提取')
                        value_get = self.extrator('dic', extrator, response_to_check) # 获取键对应值
                        logger.info('获取到的变量的值为：%s' % value_get)

                        global_variable_dic[var_name] = value_get
                        logger.info('使用“键值提取”提取的自定义变量-值(key-value对)为:%s-%s' % (var_name, value_get))
                elif key == 're':
                    for var_name, extrator in self.output_params[key].items():
                        logger.info('使用正则表达式提取')
                        value_get = self.extrator('re', extrator, response_to_check)
                        logger.info('获取到的变量的值为：%s' % value_get)

                        index = 1
                        tmp_var_name = var_name
                        for item in value_get:
                            var_name = var_name + '_' + str(index)
                            global_variable_dic[var_name] = item # 如果变量已存在，会直接覆盖
                            index = index + 1
                            logger.info('使用“正则表达式提取”提取的自定义变量-值(key-value对)为:%s-%s' % (var_name, item))
                            var_name = tmp_var_name
                elif key == 'xpath':
                    for var_name, extrator in self.output_params[key].items():
                        logger.info('使用xpath提取')
                        value_get = self.extrator('xpath', extrator, response_to_check)
                        logger.info('获取到的变量的值为：%s' % value_get)
                        index = 1
                        for value in value_get:
                            tmp_var_name = var_name + '_' + str(index)
                            logger.info('使用“xpath提取”提取的自定义变量-值(key-value对)为:%s-%s' % (tmp_var_name, value.text))
                            global_variable_dic[tmp_var_name] = value.text
                            index = index + 1
                elif key == 'db':
                    logger.info('提取数据库查询结果')
                    for var_name, var_number in self.output_params[key].items():
                        var_number = int(var_number) #以防错误输入了字符串编号
                        index = var_number - 1
                        if index <= len(response_to_check) and index >=0:
                            global_variable_dic[var_name] = response_to_check[index]# 注意：如果已有存在值，则替换已经存在的值

                        logger.debug('提取的自定义变量-值(key-value)为:%s-%s' % (var_name, response_to_check[index]))

    def tearDown(self):
        pass

