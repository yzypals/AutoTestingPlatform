#!/usr/bin/env python
#-*-encoding:utf-8-*-

__author__ = 'shouke'

from common.log import logger

class Assertion:
    def __init__(self):
        pass

    # 判断元素是否存在
    def assert_element_exists(self, selenium_util, element_selector):
        result = selenium_util.find_element_by_locator_adapter(element_selector)
        if result[0]: #如果找到了
            logger.info('找到元素：%s' % result[1])
        else:
            logger.warn('未找到元素：%s' % result[1])
        return result

    # 判断页面标题是否包含指定字符串
    def assert_page_title_contain_str(self, selenium_util, target_str):
        result = selenium_util.get_page_title()
        if result[0]:
            if result[1].find(target_str) != -1:
                return [True, '']
            else:
                return [False, '页面标题不包含字符串%s' % target_str]
        else:
            return result



myassertion = Assertion()