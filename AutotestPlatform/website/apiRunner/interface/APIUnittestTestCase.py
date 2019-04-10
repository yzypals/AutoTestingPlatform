#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import urllib.request
import json
import chardet
import re
#from html.parser import HTMLParser

from collections import OrderedDict
import platform
import copy

python_version = platform.python_version()
if python_version < '3.5':
    from html.parser import HTMLParser
else:
    from html import unescape

from ..common.log import logger
from ..unittesttestcase import MyUnittestTestCase

__all__ = ['APIUnittestTestCase']

class APIUnittestTestCase(MyUnittestTestCase):
    def test_api_for_urlencode(self): # 针对请求体为url编码的：b'id=1318&password=e10adc3949ba59abbe56e057f20f883e'
        try:
            method = self.request_method.lower()
            try:
                input_params_copy = copy.deepcopy(self.input_params)
                # 兼容旧版程序，旧数据， 吧json形式的数据，转为url编码 形如：把  {"id":1318,"password":"e10adc3949ba59abbe56e057f20f883e"} 转为  b'id=1318&password=e10adc3949ba59abbe56e057f20f883e'
                if self.input_params:
                    self.input_params = json.loads(self.input_params, object_pairs_hook=OrderedDict)
                    self.input_params = urllib.parse.urlencode(self.input_params)  # 将参数转为url编码字符串# 注意，此处params为必须为字典类型的数据
            except Exception as e:
                result = input_params_copy.split('安全模式')[:]
                if len(result) > 1:
                    self.input_params, safe = result
                else:
                    self.input_params = result[0]
                    safe = ''
                self.input_params = self.input_params.strip()
                safe = safe.replace(' ', '').strip()
                if safe == '':
                    self.input_params = urllib.parse.quote(self.input_params, safe='&=')  # 将参数转为url编码字符串
                elif safe != '' and safe != '无':
                    msg = '配置的安全模式为：%s' % safe
                    logger.info(msg)
                    self.log_websocket_consumer.info(msg)
                    self.input_params = urllib.parse.quote(self.input_params, safe=safe)
                elif safe == '无':
                    self.input_params = urllib.parse.quote(self.input_params)
        except Exception as e:
            msg = '%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
            msg = 'fail#%s' % e
            self.assertEqual(1, 0, msg=msg)

        if method == 'post':
            msg = '正在发起POST请求...'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            self.input_params = self.input_params.encode('utf-8')
            response = self.http.post(self.url_or_sql, self.input_params)
        elif method == 'get':
            msg = '正在发起GET请求...'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            response = self.http.get(self.url_or_sql, self.input_params)
        
        # if not response[0]:
        #     msg = 'fail#%s' % response[1]
        #     self.assertEqual(1, 0, msg=msg)

        body = response[0]
        if response[0]:
            encoding = chardet.detect(response[0])['encoding']

            msg = '检测到的编码为：%s, 正在对服务器返回body进行解码' % encoding
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            if encoding:
                if  encoding.lower() in ('gb2312', 'windows-1252',  'iso-8859-1'):
                    body = response[0].decode('gbk')  # decode函数对获取的字节数据进行解码
                elif encoding.lower() in ('utf-8', 'utf-8-sig', 'iso-8859-2'):
                    body = response[0].decode('utf-8')
                elif encoding.lower() == 'ascii':
                    body = response[0].decode('unicode_escape')
                else:
                    msg = '解码失败，未知编码:%s，不对body做任何解码' % encoding
                    logger.info(msg)
                    self.log_websocket_consumer.info(msg)
                    body = response[0]

                if python_version < '3.5':
                    parser = HTMLParser()
                    body = parser.unescape(body) # 处理html实体
                else:
                    body = unescape(body)

            header = response[1]
            code = response[2]
            msg = '服务器返回结果"响应体(body)": %s' % body
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            msg = '服务器返回结果"请求头(headers)": %s' % header
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            msg = '服务器返回结果"状态码(code)": %s' % code
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
        else:
            body, header,code = response[1], response[1], response[1]

        if self.response_to_check == 'body':
            msg = '正在提取目标返回结果值'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            self.save_result(body)

            msg = '正在执行断言'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            self.assert_result(body)

        elif self.response_to_check == 'header':
            msg = '正在提取目标返回结果值'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            self.save_result(header)

            msg = '正在执行断言'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            self.assert_result(header)
        elif self.response_to_check == 'code':
            msg = '正在提取目标返回结果值'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            self.save_result(code)

            msg = '正在执行断言'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            self.assert_result(code)


    def test_api_for_json(self): # 针对请求体为json格式（类型：字符串）的
        method = self.request_method.lower()
        if method == 'post':
            msg = '正在发起POST请求...'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            # self.input_params = json.dumps(self.input_params)  # 将参数转为json格式字符串
            # 替换键或者值的单引号为双引号
            match_list =  re.findall('["|\']\s*:\s*["|\']', self.input_params)
            for match in match_list:
                if match.find("'") != -1:
                    self.input_params = self.input_params.replace(match, match.replace("'", '"'))

            match_list =  re.findall('["|\']\s*}\s*,\s*["|\']', self.input_params)
            for match in match_list:
                if match.find("'") != -1:
                    self.input_params = self.input_params.replace(match, match.replace("'", '"'))

            self.input_params = self.input_params.encode('utf-8')
            response = self.http.post(self.url_or_sql, self.input_params)
        elif method == 'get':
            msg = '正在发起GET请求...'
            logger.info(msg)
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            self.input_params = urllib.parse.urlencode(self.input_params)
            response = self.http.get(self.url_or_sql, self.input_params)

        body = response[0]
        if response[0]:
            encoding = chardet.detect(response[0])['encoding']
            msg = '正在对服务器返回body进行解码'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            if encoding:
                if  encoding.lower() in ('gb2312', 'windows-1252',  'iso-8859-1'):
                    body = response[0].decode('gbk')  # decode函数对获取的字节数据进行解码
                elif encoding.lower() in ('utf-8', 'utf-8-sig', 'iso-8859-2'):
                    body = response[0].decode('utf-8')
                elif encoding.lower() == 'ascii':
                    body = response[0].decode('unicode_escape')
                else:
                    msg = '解码失败，未知编码:%s，不对body做任何解码' % encoding
                    logger.info(msg)
                    self.log_websocket_consumer.info(msg)
                    body = response[0]

                if python_version < '3.5':
                    parser = HTMLParser()
                    body = parser.unescape(body) # 处理html实体
                else:
                    body = unescape(body)
            header = response[1]
            code = response[2]
            msg = '服务器返回结果"响应体(body)": %s' % body
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            msg = '服务器返回结果"请求头(headers)": %s' % header
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            msg = '服务器返回结果"状态码(code)": %s' % code
        else:
            body, header,code = response[1], response[1], response[1]

        if self.response_to_check == 'body':
            msg = '正在提取目标返回结果值'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            self.save_result(body)

            msg = '正在执行断言'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            self.assert_result(body)

        elif self.response_to_check == 'header':
            msg = '正在提取目标返回结果值'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            self.save_result(header)

            msg = '正在执行断言'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            self.assert_result(header)
        elif self.response_to_check == 'code':
            msg = '正在提取目标返回结果值'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            self.save_result(code)

            msg = '正在执行断言'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            self.assert_result(code)


    def test_api_for_xml(self): # 针对请求体为webservice xml格式的
        method = self.request_method.lower()
        if method == 'post':
            msg = '正在发起POST请求...'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            self.input_params = self.input_params.encode('utf-8')
            response = self.http.post(self.url_or_sql, self.input_params)
        elif method == 'get':
            msg = '正在发起GET请求...'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            self.input_params = urllib.parse.urlencode(self.input_params)
            response = self.http.get(self.url_or_sql, self.input_params)

        body = response[0]
        if response[0]:
            encoding = chardet.detect(response[0])['encoding']
            msg = '正在对服务器返回body进行解码'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            if encoding:
                if  encoding.lower() in ('gb2312', 'windows-1252', 'iso-8859-1'):
                    body = response[0].decode('gbk')  # decode函数对获取的字节数据进行解码
                elif encoding.lower() in ('utf-8', 'utf-8-sig', 'iso-8859-2'):
                    body = response[0].decode('utf-8')
                elif encoding.lower() == 'ascii':
                    body = response[0].decode('unicode_escape')
                else:
                    msg = '解码失败，未知编码:%s，不对body做任何解码' % encoding
                    logger.info(msg)
                    self.log_websocket_consumer.info(msg)
                    body = response[0]

                if python_version < '3.5':
                    parser = HTMLParser()
                    body = parser.unescape(body) # 处理html实体
                else:
                    body = unescape(body)
                header = response[1]
                code = response[2]
                msg = '服务器返回结果"响应体(body)": %s' % body
                logger.info(msg)
                self.log_websocket_consumer.info(msg)
                msg = '服务器返回结果"请求头(headers)": %s' % header
                logger.info(msg)
                self.log_websocket_consumer.info(msg)
                msg = '服务器返回结果"状态码(code)": %s' % code
                logger.info(msg)
                self.log_websocket_consumer.info(msg)
        else:
            body, header,code = response[1], response[1], response[1]

        if self.response_to_check == 'body':
            msg = '正在提取目标返回结果值'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            self.save_result(body)

            msg = '正在执行断言'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            self.assert_result(body)

        elif self.response_to_check == 'header':
            msg = '正在提取目标返回结果值'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            self.save_result(header)

            msg = '正在执行断言'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            self.assert_result(header)
        elif self.response_to_check == 'code':
            msg = '正在提取目标返回结果值'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            self.save_result(code)

            msg = '正在执行断言'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            self.assert_result(code)

