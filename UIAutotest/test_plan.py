#!/usr/bin/env python
#-*-encoding:utf-8-*-

__author__ = 'shouke'

import time
import  re

from common.log import logger
from common.seleniumutil import selenium_util
from common.globalvar import test_platform_db
from common.globalvar import test_reporter
from test_case import TestCase


class TestPlan:
    def __init__(self, plan_id, plan_name, project_id, project_name, home_page, broswers):
        self.plan_id = plan_id
        self.plan_name = plan_name
        self.project_id = project_id
        self.project_name = project_name
        self.home_page = home_page
        self.broswers = broswers

    def run(self, debug):
        try:
            # 获取开始运行时间
            timestamp_for_start = time.time()
            start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

            logger.info('计划运行的浏览器有：%s' % (self.broswers))

            logger.info('正在查询测试计划关联的测试用例')
            query = 'SELECT node_id, node_path, node_name FROM `website_ui_case_tree_test_plan` WHERE plan_id = %s AND sub_node_num = 0 ORDER BY `order` ASC'
            data = (self.plan_id, )
            result = test_platform_db.select_many_record(query, data)
            if result[0] and result[1]:
                records = result[1]

                browser_list_for_failure = []
                mark = False # 用于标记是否有运行用例出错的浏览器
                host_port = re.findall('[https|http]+://[^/]+', self.home_page) # 获取http地址 形如 http://www.baidu.com, http://www.baidu.com:8080
                if host_port:
                    host_port = host_port[0]
                else:
                    return [False, '项目主页填写错误']
                for browser in self.broswers:
                    execution_num = str(int(time.time())) # 执行编号

                    if not  debug:
                        data = (execution_num, self.project_id, self.plan_id, self.project_name, self.plan_name, browser, start_time, '', '', 0, 0, 0, 0, '')
                        logger.info('正在往测试报告-测试概况插入计划执行概要记录')
                        test_reporter.insert_report_for_summary(data)

                    logger.info('正在获取浏览器驱动')
                    result = selenium_util.set_driver(browser)
                    if not result[0] and not debug: # 设置驱动出错
                        logger.error('获取浏览器驱动出错，跳过该浏览器的执行')
                        data = ('', '', 0, 0, 0, 0, result[1], execution_num, self.plan_id)
                        test_reporter.update_report_for_summary(data)
                        continue
                    try:
                        browser_driver = selenium_util.get_driver()
                        selenium_util.maximize_window()
                        logger.info('正在打开项目主页：%s' % self.home_page)
                        selenium_util.get(self.home_page)
                        selenium_util.implicitly_wait(20)

                        flag = False  # 用于标记是在每个浏览器下运行时，是否出现了运行出错的用例
                        logger.info('======================正在【%s】浏览器下运行测试用例======================' % browser)
                        for record in records:
                            case_id, case_path, case_name = record
                            test_case = TestCase(execution_num, self.plan_id, case_id, case_path, case_name, host_port)
                            logger.info('======================开始运行测试用例[名称：%s, ID:%s]======================' % (case_name, case_id))
                            result = test_case.run(debug)
                            if not result[0]:
                                flag = True # 有运行出错的用例

                        if flag:
                            mark = True
                            remark = '部分用例运行出错'
                            browser_list_for_failure.append(browser)
                        else:
                            remark = ''
                    except Exception as e:
                        logger.error('运行出错：%s' % e)
                        remark = '%s' % e
                        mark = True
                    finally:
                        browser_driver.close()
                        browser_driver.quit()

                        if not debug:
                            end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) # 结束运行时间

                            # 记录运行截止时间
                            timestamp_for_end = time.time()
                            time_took = int(timestamp_for_end - timestamp_for_start)
                            logger.info('测试用例执行完毕，正在更新测试报告-测试概况表')
                            days, hours, minutes, seconds = str(time_took//86400), str((time_took%86400)//3600), str(((time_took%86400)%3600)//60), str(((time_took%86400)%3600)%60)
                            time_took = days + '天 '+ hours +'小时 '+ minutes + '分 ' +  seconds +'秒' # 运行耗时

                            case_pass_num = test_reporter.get_case_num_by_run_result(execution_num, self.plan_id, '成功')   # 运行成功用例数
                            case_fail_num = test_reporter.get_case_num_by_run_result(execution_num, self.plan_id,  '失败')   # 运行失败用例数
                            case_block_num = test_reporter.get_case_num_by_run_result(execution_num,self.plan_id,  '阻塞')  # 运行被阻塞用例数
                            case_total_num = case_block_num + case_fail_num + case_pass_num

                            data = (end_time, time_took, case_total_num, case_pass_num, case_fail_num, case_block_num, remark, execution_num, self.plan_id)
                            test_reporter.update_report_for_summary(data)
                if mark:
                    return [False, '测试计划在浏览器%s下运行失败' % str(browser_list_for_failure)]
                else:
                    return [True, '执行成功']
            elif result[0] and not result[1]:
                reason = '未查找到同测试计划关联的用例'
                logger.warn(reason)
                return [False, reason]
            else:
                reason = '查找同测试计划[名称：%s, ID：%s]关联的用例失败：%s' % (self.plan_name, self.plan_id, result[1])
                logger.error(reason)
                return [False, reason]
        except Exception as e:
            logger.error('%s' % e)
            return [False, '%s' % e]

