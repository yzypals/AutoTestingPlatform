#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import urllib.request
import http.cookiejar
import urllib.parse
import ssl
import configparser

from common.log import logger


# 添加cookie自动处理支持
cj = http.cookiejar.CookieJar()
cookie_handler = urllib.request.HTTPCookieProcessor(cj)

config = configparser.ConfigParser()

# 从配置文件中读取SSL协议版本
config.read('./conf/https.conf', encoding='utf-8')

# 添加ssl支持 # 注意，发起的请求要为443端口
ssl_or_tls_protocol = config['HTTPS']['SSL_OR_TLS_PROTOCOL'].lower()
if ssl_or_tls_protocol == 'v1':
    https_handler = urllib.request.HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
elif ssl_or_tls_protocol == 'v2':
    https_handler = urllib.request.HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_SSLv2))
elif ssl_or_tls_protocol == 'v23':
    https_handler = urllib.request.HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_SSLv23))
elif ssl_or_tls_protocol == 'v3':
    https_handler = urllib.request.HTTPSHandler(context=ssl.PROTOCOL_SSLv3)
opener = urllib.request.build_opener(cookie_handler, https_handler)
urllib.request.install_opener(opener)

class MyHttp:
    '''配置要测试接口服务器的ip、端口、域名等信息，封装http请求方法，http头设置'''

    def __init__(self, protocol, host, port, headers = {}):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.headers = headers  # http 头
        self.request_param = ''

    def set_host(self, host):
        self.host = host

    def get_host(self):
        return self.host

    def get_protocol(self):
        return self.protocol

    def set_protocol(self, protocol):
        self.protocol = protocol

    def set_port(self, port):
        self.port = port

    def get_port(self):
        return  self.port

    # 设置http头
    def set_headers(self, headers):
        self.headers = headers

    def get_headers(self):
        return  self.headers

    def get_request_param(self):
        return self.request_param

    # 封装HTTP GET请求方法
    def get(self, url, params=''):
        self.request_param = params # 存储下转换后的参数，供后续报告使用
        url = self.protocol + '://' + self.host + ':' + str(self.port)  + url + params

        logger.info('发起的请求为：GET %s' % url)
        logger.info('请求头为：%s' % str(self.headers))
        request = urllib.request.Request(url, headers=self.headers)
        exec_count = 0
        while exec_count <= 1:
            try:
                response = urllib.request.urlopen(request)
                response_body = response.read()
                response_header = response.getheaders()
                response_status_code = response.status
                response = [response_body, response_header, response_status_code]
                exec_count = 2
            except Exception as e:
                exec_count = exec_count + 1
                reason = '%s' % e
                response = [None, reason]
                print('发送请求失败，原因：%s,正在进行第%s次尝试' % (e, exec_count))
        return  response

    # 封装HTTP POST请求方法
    def post(self, url, data=b''):
        self.request_param = data # 存储下转换后的参数，供后续报告使用
        url = self.protocol + '://' + self.host + ':' + str(self.port)  + url

        logger.info('发起的请求为：POST %s' % url)
        logger.info('参数为：%s' % data)
        logger.info('请求头为：%s' % str(self.headers))
        request = urllib.request.Request(url, headers=self.headers, method='POST')
        exec_count = 0
        while exec_count <= 1:
            try:
                response = urllib.request.urlopen(request, data)
                response_body = response.read()
                response_header = response.getheaders()
                response_status_code = response.status
                response = [response_body, response_header, response_status_code]
                exec_count = 2
            except Exception as e:
                exec_count = exec_count + 1
                reason = '%s' % e
                response = [None, reason]
                print('发送请求失败，原因：%s,正在进行第%s次尝试' % (e, exec_count))
        return  response

    # 封装HTTP DELETE请求方法
    def delete(self, url, data=b''):
        url = self.protocol + '://' + self.host + ':' + str(self.port)  + url

        print('发起的请求为：DELETE %s' % url)
        print('参数为：%s' % data)
        logger.info('请求头为：%s' % str(self.headers))
        request = urllib.request.Request(url, headers=self.headers, method='DELETE')
        exec_count = 0
        while exec_count <= 1:
            try:
                response = urllib.request.urlopen(request, data)
                response_body = response.read()
                response_header = response.getheaders()
                response_status_code = response.status
                response = [response_body, response_header, response_status_code]
                exec_count = 2
            except Exception as e:
                exec_count = exec_count + 1
                reason = '%s' % e
                response = [None, reason]
                print('发送请求失败，原因：%s,正在进行第%s次尝试' % (e, exec_count))
        return  response

    # 封装HTTP xxx请求方法
    # 自由扩展
