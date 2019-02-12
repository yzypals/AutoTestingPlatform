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

    # 判断当前页面标题是否包含指定字符串
    def assert_page_title_contain_str(self, selenium_util, target_str):
        result = selenium_util.get_page_title()
        if result[0]:
            if target_str in  result[1]:
                return [True, '']
            else:
                return [False, '页面标题不包含给定字符串：%s' % target_str]
        else:
            return result


    # 判断当前页面标题完全匹配指定字符串
    def assert_page_title_equal_str(self, selenium_util, target_str):
        result = selenium_util.get_page_title()
        if result[0]:
            if result[1] == target_str:
                return [True, '']
            else:
                return [False, '页面标题不等于给定字符串：%s' % target_str]
        else:
            return result

    # 判断当前访问的页面url是否包含指定字符串
    def assert_url_visited_contain_str(self, target_str):
        try:
            current_url = self.driver.current_url
            if target_str in current_url:
                return [True, '']
            else:
                return [False, '当前页面访问的URL不包含给定字符串：%s' % target_str]
        except Exception as e:
            return [False, '%s' % e]


    # 判断当前访问的页面url是否完全匹配指定字符串
    def assert_url_visited_equal_str(self, target_str):
        try:
            current_url = self.driver.current_url
            if target_str == current_url:
                return [True, '']
            else:
                return [False, '当前页面访问的URL不等于给定字符串：%s' % target_str]
        except Exception as e:
            return [False, '%s' % e]

    # 判断当前元素文本内容是否包指定字符串
    def assert_element_text_contain_str(self, selenium_util, element_selector, target_str):
        try:
            result = selenium_util.find_element_by_locator_adapter(element_selector)
            if result[0]: #如果找到了
                text_of_element = result[1].text
                logger.info('获取到的元素[%s]文本内容为：%s' % (result[1], text_of_element))
                if target_str in text_of_element:
                    return [True, '']
                else:
                    return [False, '元素[%s]文本内容不包含给定字符串：%s' % (result[1], text_of_element)]
            else:
                logger.warn('未找到元素：%s' % result[1])
                return [False, '未找到元素：%s' % result[1]]
        except Exception as e:
            return [False, '%s' % e]

    # 判断当前元素文本内容是否等于指定字符串
    def assert_element_text_equal_str(self, selenium_util, element_selector, target_str):
        try:
            result = selenium_util.find_element_by_locator_adapter(element_selector)
            if result[0]: #如果找到了
                text_of_element = result[1].text
                logger.info('获取到的元素[%s]文本内容为：%s' % (result[1], text_of_element))
                if target_str == text_of_element:
                    return [True, '']
                else:
                    return [False, '元素[%s]文本内容不等于给定字符串：%s' % (result[1], text_of_element)]
            else:
                logger.warn('未找到元素：%s' % result[1])
                return [False, '未找到元素：%s' % result[1]]
        except Exception as e:
            return [False, '%s' % e]

myassertion = Assertion()