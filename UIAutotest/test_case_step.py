#!/usr/bin/env python
#-*-encoding:utf-8-*-

__author__ = 'shouke'

import time

from common.log import logger
from common.seleniumutil import selenium_util
from common.globalvar import test_reporter
from common.globalvar import test_platform_db
from common.assertion import myassertion

class TestCaseStep:
    def __init__(self, execution_num, plan_id, case_id, step_id, order, object_type, page_name, op_object, exec_operation, input_params, output_params,
                 assert_type, assert_pattern, run_times, try_for_failure, object_id, home_page):
        self.execution_num = execution_num
        self.plan_id = plan_id
        self.case_id = case_id
        self.step_id = step_id
        self.order = order
        self.object_type = object_type
        self.page_name = page_name
        self.op_object = op_object
        self.exec_operation = exec_operation
        self.input_params = input_params
        self.output_params = output_params
        self.assert_type = assert_type
        self.assert_pattern = assert_pattern
        self.run_times = run_times
        self.try_for_failure = try_for_failure
        self.object_id = object_id
        self.home_page = home_page

    def run(self, debug):
        try:
            # selenium_util.debug_info()
            # 获取开始运行时间
            start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            if self.object_type == '页面元素':
                logger.info('正在查找页面元素选择器')
                temp_result = self.query_element_selectors()
                if temp_result[0]:
                    selector1, selector2 = temp_result[1]
                    for run_times in range(0, self.run_times + 1):
                        logger.info('正在运行第%s次' % str(run_times+1))
                        for try_times in range(0, self.try_for_failure+1):
                            temp_result = self.operate_page_element(selector1, selector2, self.exec_operation, self.input_params)
                            if temp_result[0]:
                                logger.info('运行成功')
                                result = [True, '成功', '']
                                break
                            else:
                                logger.warn('运行失败：%s，正在进行第%s次重试' % (temp_result[1],str(try_times+1)))
                                result = [temp_result[0], '失败', temp_result[1]]
                else:
                    result = [False, '失败', temp_result[1]]
            elif self.object_type == '系统函数':
                result = self.exec_system_func(self.op_object, self.input_params)
                if not result[0]:
                    logger.error('执行出错，原因：%s' % result[2])
            elif self.object_type == '数据库':
                # logger.info('步骤操作对象为数据库')
                result = [False, '失败', '暂时不支持']

            assert_result = self.exec_assert()
            if result[0] and assert_result[0]:
                result = [True, '成功', '']
            else:
                if not result[0]:
                    result = [False, '失败', '步骤运行失败：' + result[2]]
                elif assert_result[0]:
                     result = [False, '失败', '断言失败：' + assert_result[1]]
        except Exception as e:
            result = [False, '失败', '%s' % e]
        finally:
            if not debug:
                logger.info('======================正在记录用例步骤运行结果到测试报告-用例步骤执行明细表======================')
                data = (self.execution_num, self.plan_id, self.case_id, self.step_id,self.order, self.page_name, self.op_object, self.exec_operation, self.input_params, self.output_params,
                                                self.assert_type, self.assert_pattern, self.run_times, self.try_for_failure, result[1], result[2], start_time, 0)
                test_reporter.insert_report_for_case_step(data)
            return  result

    # 执行页面元素操作
    def query_element_selectors(self):
        try:
            result = test_platform_db.select_one_record('SELECT selector1, selector2 FROM `website_page_element` WHERE  id = %s', (self.object_id,))
            if result[0] and result[1]:
                record = result[1]
                return [True, record]
            elif result[0] and not result[1]:
                return [False, '未找到元素选择器']
            else:
                logger.error('查找元素选择器失败：%s' % result[1])
                return [False, '查找元素选择器失败：%s' % result[1]]
        except Exception as e:
            logger.error('%s' % e)
            return [False, '%s' % e]

    # 查找元素
    def find_element(self, selector1, selector2):
        # 优先使用selector1查找
        result = selenium_util.find_element_by_locator_adapter(selector1)
        if result[0]: #如果找到了
            logger.info('找到元素：%s' % result[1])
            return result
        else:
            logger.info('用选择器1:%s未找到元素，开始用选择器2:%s查找' % (selector1, selector2))
            result = selenium_util.find_element_by_locator_adapter(selector2)
            if result[0]: #如果找到了
                logger.info('找到元素：%s' % result[1])
            else:
                logger.warn('未找到元素：%s' % result[1])
            return  result

    # 执行元素操作
    def operate_page_element(self, selector1, selector2, exec_operation, input_params):
        if exec_operation == '输入':
            try:
                result = self.find_element(selector1, selector2)
                if result[0]:
                    if input_params:
                        result[1].send_keys(input_params)
                        logger.info('输入数据成功')
                        return [True, '输入数据成功']
                    else:
                        logger.warn('输入参数为空')
                        return [False, '输入参数为空']
                else:
                    return [False, '输入数据失败:%s' % result[1]]
            except Exception as e:
                logger.error('执行输入操作出错:%s' % e)
                return [False, '%s' % e]
        elif exec_operation == '清空':
            try:
                result = self.find_element(selector1, selector2)
                if result[0]:
                    result[1].clear()
                    logger.info('清空数据成功')
                    return [True, '清空数据成功']
                else:
                    logger.error('清空数据失败：%s' % result[1])
                    return [False, '清空数据失败：%s' % result[1]]
            except Exception as e:
                logger.error('执行输入操作出错:%s' % e)
                return [True, '%s' % e]
        elif exec_operation == '点击':
            try:
                result = self.find_element(selector1, selector2)
                if result[0]:
                    element = result[1]

                    end_time = time.time() + 30 # 设置30秒的超时时间
                    while True:
                        if element.is_enabled():
                            element.click()
                            logger.info('点击操作成功')
                            return [True, '点击成功']

                        if time.time() > end_time:
                            logger.error('等待元素可点击超时30秒')
                            break

                    logger.error('点击操作失败：等待元素可点击超时30秒')
                    return [False, '点击操作失败：元素不可点击']
                else:
                    logger.error('点击操作失败：%s' % result[1])
                    return [False, '点击操作失败：%s' % result[1]]
            except Exception as e:
                logger.error('点击操作出错:%s' % e)
                return [False, '%s' % e]
        elif exec_operation == '鼠标移动到':
            try:
                result = self.find_element(selector1, selector2)
                if result[0]: # 找到元素
                    result = selenium_util.move_to_element(result[1])
                else:
                    result = [False, '"鼠标移动到"失败：%s' % result[1]]
                return result
            except Exception as e:
                logger.error('执行“鼠标移动到”操作失败:%s' % e)
                return [False, '%s' % e]
        elif exec_operation == '拖动滚动条至元素可见':
            try:
                result = self.find_element(selector1, selector2)
                if result[0]: # 找到元素
                    result = selenium_util.scroll_to_element_for_visible(result[1])
                else:
                    result = [False, '拖动滚动条至元素可见失败:%s' % result[1]]
                return  result
            except Exception as e:
                logger.error('拖动滚动条至元素可见失败:%s' % e)
                return [False, '%s' % e]
        else:
            logger.error('不支持的操作')
            return [False, '不支持的操作']

    # 执行断言
    def exec_assert(self):
        if self.assert_type == '存在元素':
            result = myassertion.assert_element_exists(selenium_util, self.assert_pattern)
        elif self.assert_type == '页面标题包含':
            result = myassertion.assert_page_title_contain_str(selenium_util, self.assert_pattern)
        elif self.assert_type == '页面标题等于':
            result = myassertion.assert_page_title_equal_str(selenium_util, self.assert_pattern)
        elif self.assert_type == '页面url包含':
            result = myassertion.assert_url_visited_contain_str(self.assert_pattern)
        elif self.assert_type == '页面url等于':
            result = myassertion.assert_url_visited_equal_str(self.assert_pattern)
        elif self.assert_type == '元素文本包含':
            result = myassertion.assert_element_text_contain_str(self.assert_pattern)
        elif self.assert_type == '元素文本等于':
            result = myassertion.assert_element_text_equal_str(self.assert_pattern)
        else:
            return [True, '']
        return result

    # 执行系统函数
    def exec_system_func(self, function_name, arg=''):
        try:
            if function_name == '跳转到URL':
                if not (arg.startswith('http://') or arg.startswith('https://')):
                    arg = self.home_page + '/' + arg.lstrip('/')
                result = selenium_util.get(arg)
            elif function_name == '浏览器前进':
                result = selenium_util.forward()
            elif function_name == '浏览器后退':
                result  = selenium_util.back()
            elif function_name == '智能等待':
                second = int(arg)
                result = selenium_util.implicitly_wait(second)
            elif function_name == '死等待':
                second = int(arg)
                time.sleep(int(second))
                result = [True, '成功', '']
            elif function_name == '切换至窗口ByName':
                result = selenium_util.switch_to_window_by_name(arg)
            elif function_name == '切换至窗口ByPageTitle':
                result = selenium_util.switch_to_window_by_title(arg)
            elif function_name == '切换至窗口ByUrl':
                if not (arg.startswith('http://') or arg.startswith('https://')):
                    arg = self.home_page + '/' + arg.lstrip('/')
                result = selenium_util.switch_to_window_by_url(arg)
            elif function_name == '关闭当前窗口':
                result = selenium_util.close_current_window()
            elif function_name == '拖动垂直滚动条':
                result = selenium_util.scroll_to_top_or_bottom(arg)
            else:
                return [False, '失败', '不支持的函数']

            if result[0]:
                return [True, '成功', '']
            else:
                return [False, '失败', result[1]]
        except Exception as e:
            logger.error('%s' % e)
            return [False, '失败', '执行函数出错：%s' % e]

