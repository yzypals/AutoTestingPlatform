#!/usr/bin/env python
#-*- encoding:utf-8 -*-

__author__ = 'shouke'

import  os
import base64
from ...common.log import logger

import sys
import os

__all__ = ['__read_file', '__base64encode']


def __read_file(args_list, log_websocket_consumer):
    '''读取文件'''

    try:
        if len(args_list) == 3:
            filepath, mode, encoding = args_list
        else:
            filepath, mode = args_list
            encoding = None

        co_filepath = sys._getframe().f_code.co_filename
        head, tail = os.path.split(co_filepath)
        head = os.path.join(head, '../../testdata/')
        filepath = os.path.join(head, filepath)
        filepath = os.path.normpath(filepath)

        msg = '待读取的文件路径为：%s' % filepath
        logger.info(msg)
        log_websocket_consumer.info(msg)
        if not os.path.exists(filepath):
            msg = '文件 %s 不存在' % filepath
            logger.error(msg)
            log_websocket_consumer.error(msg)
            return None
        else:
            if mode in ('r', 'r+', 'rw'):
                file_content = ''
            elif mode in ('rb', 'rb+'):
                file_content = b''
            else:
                msg = '文件打开方式只支持 r, r+, rw, rb, rb+'
                logger.error(msg)
                log_websocket_consumer.error(msg)
                return None

            with open(filepath, mode, encoding=encoding) as f:
                if file_content  == b'':
                    file_content = f.read()
                else:
                    for line in f:
                        file_content += line
        return file_content
    except Exception as e:
        msg  = '读取文件 %s 出错：%s' % (filepath, e)
        logger.error(msg)
        log_websocket_consumer.error(msg)
        return None


def __base64encode(args_list, log_websocket_consumer):
    try:
        if len(args_list) == 2:
            bytes, altchars = args_list
        else:
            bytes = args_list[0]
            altchars = None
        return base64.b64encode(bytes, altchars)
    except Exception as e:
        msg = 'base64编码失败：%s' % e
        logger.error(msg)
        log_websocket_consumer.error(msg)
        return  None

