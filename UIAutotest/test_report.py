#!/usr/bin/env python
#-*-encoding:utf-8-*-

__author__ = 'shouke'

from common.log import logger


class TestReport:
    def __init__(self, db):
        self.db = db

    def get_case_num_by_run_result(self, execution_num, plan_id, status):
        logger.info('正在查询运行状态为：%s的用例记录数' %  status)
        query = "SELECT COUNT(id) FROM `website_ui_test_report_for_case` WHERE run_result = '%s' and plan_id = %s AND execution_num =%s"
        data = (status,plan_id, execution_num)
        result = self.db.select_one_record(query, data)
        if result[0] and result[1]:
            case_num = result[1][0]
            return case_num
        elif result[0] and not result[1]:
            logger.error('未查询到运行状态为：%s的用例' % status)
            return  0
        else:
            logger.error('查询状态为%s用例数出错:%s,退出程序' % result[1])
            exit(1)

    def insert_report_for_summary(self, data):
        insert_query = "INSERT INTO `website_ui_test_report_for_summary`" \
                                       "(execution_num, project_id, plan_id, project_name, plan_name, browser," \
                                       "start_time, end_time, time_took, case_total_num, case_pass_num, case_fail_num, case_block_num, remark) " \
                                       "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s)"
        result = self.db.execute_insert(insert_query, data)
        if not result[0]:
           logger.error('往测试报告-测试概况插入运行记录失败：%s,提前退出程序' % result[1])
           exit(1)

    def update_report_for_summary(self, data):
        update_query = "UPDATE `website_ui_test_report_for_summary` SET end_time='%s', time_took='%s', " \
                       "case_total_num=%s, case_pass_num=%s, case_fail_num=%s, case_block_num=%s, remark='%s' WHERE execution_num='%s' AND plan_id=%s"
        result = self.db.execute_update(update_query, data)
        if not result[0]:
            logger.error('更新测试报告-测试概况表失败：%s,即将退出程序' % result[1])
            exit(1)

    def insert_report_for_case(self, data):
        insert_query = "INSERT INTO `website_ui_test_report_for_case`" \
                                       "(execution_num, plan_id, case_id, case_path, case_name, run_result, remark, run_time, time_took) " \
                                       "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        result = self.db.execute_insert(insert_query, data)
        if not result[0]:
           logger.error('往测试报告-测试用例执行明细表插入运行记录失败：%s,提前退出程序' % result[1])
           exit(1)


    def insert_report_for_case_step(self, data):
        insert_query = "INSERT INTO `website_ui_test_report_for_case_step`(execution_num, plan_id, case_id, step_id, `order`, page, object, exec_operation, input_params, " \
                       "output_params, assert_type, check_pattern, run_times, try_for_failure, run_result, remark, run_time, run_id) " \
                       "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        result = self.db.execute_insert(insert_query, data)
        if not result[0]:
           logger.error('往测试报告-测试用例步骤执行明细表插入运行记录失败：%s,提前退出程序' % result[1])
           exit(1)
