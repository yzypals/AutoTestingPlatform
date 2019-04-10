#!/usr/bin/env python
#-*-encoding:utf-8-*-

__author__ = 'shouke'

from .common.log import logger
from .test_plan import TestPlan


class TestProject:
    def __init__(self, project_id, project_name, protocol, host, port, global_headers, plan_id_list, test_platform_db, log_websocket_consumer):
        self.project_id = project_id
        self.project_name = project_name
        self.protocol = protocol
        self.host = host
        self.port = port
        self.global_headers = global_headers
        self.plan_id_list = plan_id_list
        self.test_platform_db = test_platform_db
        self.log_websocket_consumer = log_websocket_consumer

    def sync_case_tree_node_info_for_testplans(self):
        temp_var = ''
        def find_case_fullpath(node_id):
            nonlocal  temp_var
            query = "SELECT parent_id, text FROM `website_api_case_tree` WHERE id = %s"
            data = (node_id, )
            result = self.test_platform_db.select_one_record(query, data)

            if result[0] and result[1]:
                parent_id, text = result[1]
                temp_var = find_case_fullpath(parent_id) + '->' + text
                return temp_var
            elif result[0] and not result[1]:
                return temp_var
            else:
                msg = '查询出错，退出程序'
                logger.error(msg)
                self.log_websocket_consumer.error(msg)
                exit()
        try:
            msg = '待运行计划ID列表：%s' % self.plan_id_list
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            msg = '正在查询与测试计划关联的用例树节点'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            if len(self.plan_id_list) == 1:
                plan_id_list = '(' + str(self.plan_id_list[0]) + ')'
            else:
                plan_id_list = str(tuple(self.plan_id_list))

            query = 'SELECT node_id FROM `website_api_case_tree_test_plan` WHERE plan_id IN ' + plan_id_list + ' GROUP BY node_id'
            data = ''
            result = self.test_platform_db.select_many_record(query, data)
            if result[0] and result[1]:
                records = result[1]

                result = [False, '没有找到测试计划关联的节点']
                for record in records:
                    msg = '正在查找用例树节点信息'
                    logger.info(msg)
                    self.log_websocket_consumer.info(msg)
                    # mysql 查询 count(NULL值) = 0
                    query = "SELECT t1.text, t1.parent_id, COUNT(t2.id) FROM `website_api_case_tree` AS t1 " \
                            "LEFT JOIN `website_api_case_tree` AS t2 ON t2.parent_id = t1.id WHERE t1.id = %s"
                    node_id = int(record[0])
                    data = (node_id,)
                    result = self.test_platform_db.select_one_record(query, data)

                    if result[0] and result[1]:
                        text, parent_id, sub_node_num = result[1]
                        sub_node_num = sub_node_num
                        node_path = (find_case_fullpath(parent_id) + '').lstrip('->')
                        msg = '正在更新测试计划用例树节点关联表记录'
                        logger.info(msg)
                        self.log_websocket_consumer.info(msg)
                        query = "UPDATE website_api_case_tree_test_plan SET node_path='%s', sub_node_num=%s WHERE plan_id IN %s AND node_id = %s"
                        data = (node_path, sub_node_num, plan_id_list, node_id)
                        result = self.test_platform_db.execute_update(query, data)
                        if not result[0]:
                            msg = '更新测试计划用例树节点关联表记录失败：%s' % result[1]
                            logger.error(msg)
                            self.log_websocket_consumer.error(msg)
                            return [False, result[1]]
                        else:
                            result = [True, '']
                    elif result[0] and not result[1]:
                        msg = '用例树节点 %s 不存在' % node_id
                        logger.warn(msg)
                        self.log_websocket_consumer.warn(msg)
                        continue
                    else:
                        msg = '查询用例树节点[ID:%s]信息出错，退出程序' % node_id
                        logger.error(msg)
                        self.log_websocket_consumer.error(msg)
                        exit()
                    temp_var = ''
                return  result
            elif result[0] and not result[1]:
                msg = '未查找到与测试计划关联的用例树节点'
                logger.error(msg)
                self.log_websocket_consumer.error(msg)
                result = [False, '未查找到与测试计划关联的用例树节点']
            else:
                msg = '查找与测试计划关联的用例树节点失败:%s' % result[1]
                logger.error(msg)
                self.log_websocket_consumer.error(msg)
                result = [False,  '查找与测试计划关联的用例树节点失败:%s' % result[1]]
            return result
        except Exception as e:
            msg = '%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
            result = [False, '同步更新与待运行测试计划关联的用例树节点信息失败：%s' % e]
            return result


    def run(self, debug):
        try:
            if_plan_run_fail = False
            plan_id_list_for_failure = [] # 存放执行失败、未执行的测试计划的ID及原因简介

            msg = '======================正在同步更新与待运行测试计划关联的所有用例树节点信息======================'
            logger.info(msg)
            logger.info(msg)
            result = self.sync_case_tree_node_info_for_testplans()
            if not result[0]:
                msg = '同步更新与待运行测试计划关联的所有用例树节点信息失败'
                logger.error(msg)
                self.log_websocket_consumer.error(msg)
                return result
            else:
                msg = '同步更新与待运行测试计划关联的所有用例树节点信息成功'
                logger.info(msg)
                self.log_websocket_consumer.info(msg)

            for plan_id in self.plan_id_list:
                 msg = '正在查询测试计划[ID：%s]相关信息' % plan_id
                 logger.info(msg)
                 self.log_websocket_consumer.info(msg)
                 result = self.test_platform_db.select_one_record('SELECT plan_name,valid_flag FROM `website_api_test_plan` WHERE id = %s', (plan_id,))
                 if result[0] and result[1]:
                     plan_name, valid_flag = result[1]
                     if valid_flag == '启用':
                         msg = '======================开始运行测试计划[名称：%s, ID：%s]======================' % (plan_name, plan_id)
                         logger.info(msg)
                         self.log_websocket_consumer.info(msg)
                         test_plan = TestPlan(plan_id, plan_name, self.project_id, self.project_name, self.protocol, self.host, self.port, self.global_headers, self.test_platform_db, self.log_websocket_consumer)
                         result = test_plan.run(debug)
                         if not result[0]:
                             plan_id_list_for_failure.append('计划ID：%s，失败原因：%s   ' % (plan_id, result[1]))
                     else:
                         msg = '测试计划已被禁用，跳过执行'
                         logger.warn(msg)
                         self.log_websocket_consumer.warn(msg)
                         plan_id_list_for_failure.append('计划ID：%s，失败原因：%s   ' % (plan_id, msg))
                 elif result[0] and not result[1]:
                     msg = '未查询到计划相关信息'
                     logger.warn(msg)
                     self.log_websocket_consumer.warn(msg)
                     plan_id_list_for_failure.append('计划ID：%s，失败原因：%s   ' % (plan_id, msg))
                 else:
                     logger.warn(result[1])
                     self.log_websocket_consumer.warn(result[1])
                     plan_id_list_for_failure.append('计划ID：%s，失败原因：%s   ' % (plan_id, result[1]))

            if plan_id_list_for_failure:
                return [False, '项目运行失败：%s' % ''.join(plan_id_list_for_failure)]
            else:
                return [True, '项目运行成功']
        except Exception as e:
            msg = '项目运行失败：%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
            return [False, '项目运行失败：%s' % e]
