#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'laiyu'

import time
import re

from common.log import logger
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumUtil:
    def __init__(self):
        self.driver = None

    # 设置驱动
    def set_driver(self, browser_type):
        try:
            browser_type = browser_type.lower()
            if 'ie' == browser_type:
                self.browser_type = 'Ie'
                self.driver = webdriver.Ie()
            elif '谷歌' == browser_type:
                self.browser_type = 'Chrome'
                self.driver = webdriver.Chrome()
            elif '火狐' == browser_type:
                self.browser_type = 'Firefox'
                self.driver = webdriver.Firefox()
            return [True, '']
        except Exception as e:
            logger.error('设置浏览器驱动出错：%s' % e)
            return [False, '设置浏览器驱动出错：%s' % e]

    def get_driver(self):
        return self.driver

    def debug_info(self):
        print(self.driver.window_handles)
        print(self.driver.current_window_handle)

    # 打开网址
    def get(self, url):
        try:
            self.driver.get(url)
            return [True, '']
        except Exception as e:
            return [False, '打开网址：%s 失败,原因：%s' % (url, e)]

    # 模拟浏览器 后退
    def back(self):
        try:
            self.driver.back()
            return [True, '']
        except Exception as e:
            return [False, '模拟浏览器后退，失败，原因：%s' % e]

    # 浏览器 前进
    def forward(self):
        try:
            self.driver.forward()
            return [True, '']
        except Exception as e:
            return [False, '模拟浏览器前进，失败，原因：%s' % e]

    # 退出
    def close(self):
        try:
            # self.driver.close()
            self.driver.quit()
        except Exception as e:
            return [False, '%s' % e]

    # 智能等待
    def implicitly_wait(self, second):
        try:
            self.driver.implicitly_wait(second)
            return [True, 'success']
        except Exception as e:
            return [False, '%s' % e]

    # 休眠
    def sleep(self, second):
        try:
            time.sleep(second)
            return [True, 'success']
        except Exception as e:
           return [False, e]

    #浏览器最大化
    def maximize_window(self):
        try:
            self.driver.maximize_window()
            return [True, 'success']
        except Exception as e:
            return [False, '%s' % e]

    # 打开web站点
    def get(self, web_url):
        try:
            self.driver.get(web_url)
            return [True, 'success']
        except Exception as e:
            return [False, '%s' % e]

    # 获取页面标题
    def get_page_title(self):
        try:
            page_title = self.driver.title
            logger.info('当前页面标题为：%s' % page_title)
            return [True, page_title]
        except Exception as e:
            return [False, '获取页面标题失败']



    # 根据id查找元素
    def find_element_by_id(self, id):
        try:
            element = self.driver.find_element_by_id(id)
            return [True, element]
        except Exception as e:
            return [False, '%s' % e]

    # 根据xpath查找元素
    def find_element_by_xpath(self, xpath):
        try:
            element = self.driver.find_element_by_xpath(xpath)
            return [True, element]
        except Exception as e:
            return [False, '%s' % e]

    # 根据name查找元素
    def find_element_by_name(self, name):
        try:
            element = self.driver.find_element_by_name(name)
            return [True, element]
        except Exception as e:
            return [False, '%s' % e]

    # 根据link查找元素
    def find_element_by_link(self, link):
        try:
            element = self.driver.find_element_by_link(link)
            return [True, element]
        except Exception as e:
            return [False, '%s' % e]

    # 根据link_text查找元素
    def find_element_by_link_text(self, link_text):
        try:
            element = self.driver.find_element_by_link_text(link_text)
            return [True, element]
        except Exception as e:
            return [False, '%s' % e]

    # 根据partial_link_text查找元素
    def find_element_by_link_text(self, partial_link_text):
        try:
            element = self.driver.find_element_by_partial_link_text(partial_link_text)
            return [True, element]
        except Exception as e:
            return [False, '%s' % e]

    # 根据css selector查找元素
    def find_element_by_css_selector(self, css_selector):
        try:
            element = self.driver.find_element_by_css_selector(css_selector)
            return [True, element]
        except Exception as e:
            return [False, '%s' % e]

    # 根据tag_name查找元素
    def find_element_by_tag_name(self,tag_name):
        try:
            element = self.driver.find_element_by_tag_name(tag_name)
            return [True, element]
        except Exception as e:
            return [False, '%s' % e]

    # 根据标签class name查找(查找单个)
    def find_element_by_class_name(self, class_name):
        try:
            element = self.driver.find_element_by_class_name(class_name)
            return [True, element]
        except Exception as e:
            return [False, '%s' % e]

    # 根据标签class name查找，查找多个
    def find_element_by_class_name(self, class_name):
        try:
            elements = self.driver.find_element_by_class_name(class_name)
            return [True, elements]
        except Exception as e:
            return [False, '%s' % e]

    # 鼠标移动到界面元素上
    def move_to_element(self, element):
        try:
            chain = ActionChains(self.driver)
            chain.move_to_element(element).perform()
            logger.info('移动操作成功')
            return [True, '移动操作成功']
        except Exception as e:
            logger.error('移动操作失败：%s' % e)
            return [False, '移动操作失败：%s' % e]

    # 拖动滚动条至元素可见
    def scroll_to_element_for_visible(self, element):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            return [True, '拖动滚动条至元素可见成功']
        except Exception as e:
            return [False, '拖动滚动条至元素可见失败：%s' % e]

    #用Js的方式拖动垂直滚动条到底部、顶部：
    def scroll_to_top_or_bottom(self, direction):
        try:
           if direction == '底部':
               js = 'document.documentElement.scrollTop=10000'
           elif direction == '顶部':
               js = 'document.documentElement.scrollTop=0'
           self.driver.execute_script(js)
           return [True, '拖动滚动条至%s成功' % direction]
        except Exception as e:
            return [False, '拖动滚动条至元素可见失败：%s' % e]

    # 切换到指定名称的窗口
    def switch_to_window_by_name(self, name):
        try:
            self.driver.switch_to.window(name)
            return [True, '']
        except Exception as e:
            return [False, '%s' % e]

    # 切换到指定标题名称的窗口(标题相同的话，按先后顺序取一个)
    def switch_to_window_by_title(self, title):
        try:
            # current_handle = self.driver.current_window_handle
            handles = self.driver.window_handles
            logger.info('当前窗口句柄有：%s' % handles)
            for handle in handles:
                self.driver.switch_to_window(handle)
                logger.info("存在的窗口标题：%s" % self.driver.title)
                page_title = self.driver.title
                if page_title == title:
                   self.driver.switch_to_window(handle)
                   return [True, '']
            return [False, '未找到当前页面标题为“%s”的窗口' % title]
        except Exception as e:
            return [False, '%s' % e]


    # 切换到指定URL的窗口(标题相同的话，按先后顺序取一个)
    def switch_to_window_by_url(self, url):
        try:
            handles = self.driver.window_handles
            # logger.info('当前窗口句柄有：%s' % handles)
            for handle in handles:
                self.driver.switch_to_window(handle)
                url_for_handle = self.driver.current_url
                logger.info('存在的窗口URL：%s' % url_for_handle)
                if url_for_handle == url:
                   self.driver.switch_to_window(handle)
                   return [True, '']
            return [False, '未找到当前URL为“%s”的窗口' % url]
        except Exception as e:
            return [False, '%s' % e]

    # 关闭当前窗口
    def close_current_window(self):
        try:
            self.driver.close()
            handles = self.driver.window_handles
            if handles: # 如果存在其它窗口，默认切换至前一次新开的窗口
                self.driver.switch_to_window(handles[len(handles)-1])
            return [True, '']
        except Exception as e:
            return [False, '%s' % e]


    def switch_to_frame(self, frame):
        try:
            self.driver.switch_to_frame(frame)
            logger.info('切换至frame（id/name/xpath = %s）成功' % frame)
            return [True, 'success']
        except Exception as e:
            logger.error('切换至frame（id/name/xpath = %s）失败' % frame)
            return [False, '%s' % e]


    # 截图
    def get_screenshot_as_file(self,filepath):
        try:
            self.driver.get_screenshot_as_file(filepath)
            return [True, '截图成功']
        except Exception as e:
            return [False, '截图失败：%s' % e]


    # # 根据元素定位器的不同，自动选择适配的定位器，查找元素
    # def find_element_by_locator_adapter(self, selector):
    #     logger.info('正在根据元素定位器：%s查找元素' % selector)
    #     selector =  re.findall('.+\s*=\s*.+', selector)
    #     if not selector:
    #         logger.error('%s为无效定位器(定位器必须满足xx=xxx格式)' % selector)
    #         return [False,'未找到元素，请检查定位器是否合法(格式：xx=xxx)' % selector]
    #     else:
    #         selector = selector[0]
    #         index = selector.find('=')
    #         adapter = selector[0: index].replace(' ', '').lower()
    #         selector = selector[index + 1:].strip(' ')
    #         logger.info('查找元素采用的适配器：%s' % adapter)
    #         logger.info('查找元素采用的选择器：%s' % selector)
    #     try:
    #         if adapter == 'id':
    #             logger.info('find_element_by_id：%s' % selector)
    #             result = selenium_util.find_element_by_id(selector)
    #             return result
    #         elif adapter == 'xpath':
    #             logger.info('find_element_by_xpath：%s' % selector)
    #             result =  selenium_util.find_element_by_xpath(selector)
    #             return result
    #         elif adapter == 'name':
    #             logger.info('find_element_by_name：%s' % selector)
    #             result =  selenium_util.find_element_by_name(selector)
    #             return result
    #         elif adapter == 'link_text':
    #             logger.info('find_element_by_link_text：%s' % selector)
    #             result = selenium_util.find_element_by_link_text(selector)
    #             return result
    #         elif adapter == 'partial_link_text':
    #             logger.info('find_element_by_partial_link_text：%s' % selector)
    #             result = selenium_util.find_element_by_partial_link_text(selector)
    #             return result
    #         elif adapter == 'css':
    #             logger.info('find_element_by_css_selector：%s' % selector)
    #             result =  selenium_util.find_element_by_css_selector(selector)
    #             return  result
    #         elif adapter == 'tag_name':
    #             logger.info('find_element_by_tag_name：%s' % selector)
    #             result = selenium_util.find_element_by_tag_name(selector)
    #             return result
    #         elif adapter == 'class_name':
    #             logger.info('find_element_by_class_name：%s' % selector)
    #             result = selenium_util.find_element_by_class_name(selector)
    #             return result
    #         else:
    #             logger.warn('非法适配器：%s:' % adapter)
    #             return [False, '非法适配器：%s:' % adapter]
    #     except Exception as e:
    #         logger.error('定位元素出错，%s' % e)
    #         return [False, '定位元素出错，%s' % e]


    # 根据元素定位器的不同，自动选择适配的定位器，查找元素
    def find_element_by_locator_adapter(self, selector, timeout=30):
        logger.info('正在根据元素定位器：%s查找元素' % selector)
        selector =  re.findall('.+\s*=\s*.+', selector)
        if not selector:
            logger.error('%s为无效定位器(定位器必须满足xx=xxx格式)' % selector)
            return [False,'未找到元素，请检查定位器是否合法(格式：xx=xxx)' % selector]
        else:
            selector = selector[0]
            index = selector.find('=')
            adapter = selector[0: index].replace(' ', '').lower()
            selector = selector[index + 1:].strip(' ')
            logger.info('查找元素采用的适配器：%s' % adapter)
            logger.info('查找元素采用的选择器：%s' % selector)
        try:
            if adapter == 'id':
                logger.info('find_element_by_id：%s' % selector)
                try:
                    element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.ID, selector)))
                    return [True, element]
                except Exception as e:
                    return [False, '%s' % e]
            elif adapter == 'xpath':
                logger.info('find_element_by_xpath：%s' % selector)
                try:
                    element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, selector)))
                    return [True, element]
                except Exception as e:
                    return [False, '%s' % e]
            elif adapter == 'name':
                logger.info('find_element_by_name：%s' % selector)
                try:
                    element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.NAME, selector)))
                    return [True, element]
                except Exception as e:
                    return [False, '%s' % e]
            elif adapter == 'link_text':
                logger.info('find_element_by_link_text：%s' % selector)
                try:
                    element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.LINK_TEXT, selector)))
                    return [True, element]
                except Exception as e:
                    return [False, '%s' % e]
            elif adapter == 'partial_link_text':
                logger.info('find_element_by_partial_link_text：%s' % selector)
                try:
                    element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, selector)))
                    return [True, element]
                except Exception as e:
                    return [False, '%s' % e]
            elif adapter == 'css':
                logger.info('find_element_by_css_selector：%s' % selector)
                try:
                    element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
                    return [True, element]
                except Exception as e:
                    return [False, '%s' % e]
            elif adapter == 'tag_name':
                logger.info('find_element_by_tag_name：%s' % selector)
                try:
                    element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.TAG_NAME, selector)))
                    return [True, element]
                except Exception as e:
                    return [False, '%s' % e]
            elif adapter == 'class_name':
                logger.info('find_element_by_class_name：%s' % selector)
                try:
                    element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, selector)))
                    return [True, element]
                except Exception as e:
                    return [False, '%s' % e]
            else:
                logger.warn('非法适配器：%s:' % adapter)
                return [False, '非法适配器：%s:' % adapter]
        except Exception as e:
            logger.error('定位元素出错，%s' % e)
            return [False, '定位元素出错，%s' % e]

selenium_util =  SeleniumUtil()

# 调试用
# selenium_util.set_driver('谷歌')
# selenium_util.get('http://10.202.95.88:8080/page/platform/home.html')
# try:
#     element = WebDriverWait(selenium_util.get_driver(), 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/section[3]/div/ul[1]/li[3]/figure')))
#     print(element.text)
# except Exception as e:
#     print('%s' % e)
# try:
#     print(element.get_attribute("value"))
# except Exception as e:
#     pass
# selenium_util.close()