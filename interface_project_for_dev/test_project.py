#!/usr/bin/env python
#-*-encoding:utf-8-*-

__author__ = 'shouke'

from common.log import logger
from common.globalvar import test_platform_db
from test_plan import TestPlan


class TestProject:
    def __init__(self, project_id, project_name, protocol, host, port, global_headers, plan_id_list):
        self.project_id = project_id
        self.project_name = project_name
        self.protocol = protocol
        self.host = host
        self.port = port
        self.global_headers = global_headers
        self.plan_id_list = plan_id_list

    def sync_case_tree_node_info_for_testplans(self):
        temp_var = ''
        def find_case_fullpath(node_id):
            nonlocal  temp_var
            query = "SELECT parent_id, text FROM `website_api_case_tree` WHERE id = %s"
            data = (node_id, )
            result = test_platform_db.select_one_record(query, data)

            if result[0] and result[1]:
                parent_id, text = result[1]
                temp_var = find_case_fullpath(parent_id) + '->' + text
                return temp_var
            elif result[0] and not result[1]:
                return temp_var
            else:
                logger.error('查询出错，退出程序')
                exit()
        try:
            logger.info('待运行计划ID列表：%s' % self.plan_id_list)

            logger.info('正在查询与测试计划关联的用例树节点')
            if len(self.plan_id_list) == 1:
                plan_id_list = '(' + str(self.plan_id_list[0]) + ')'
            else:
                plan_id_list = str(tuple(self.plan_id_list))

            query = 'SELECT node_id FROM `website_api_case_tree_test_plan` WHERE plan_id IN ' + plan_id_list + ' GROUP BY node_id'
            data = ''
            result = test_platform_db.select_many_record(query, data)
            if result[0] and result[1]:
                records = result[1]

                result = [False, '没有找到测试计划关联的节点']
                for record in records:
                    logger.info('正在查找用例树节点信息')
                    # mysql 查询 count(NULL值) = 0
                    query = "SELECT t1.text, t1.parent_id, COUNT(t2.id) FROM `website_api_case_tree` AS t1 " \
                            "LEFT JOIN `website_api_case_tree` AS t2 ON t2.parent_id = t1.id WHERE t1.id = %s"
                    node_id = int(record[0])
                    data = (node_id,)
                    result = test_platform_db.select_one_record(query, data)

                    if result[0] and result[1]:
                        text, parent_id, sub_node_num = result[1]
                        sub_node_num = sub_node_num
                        node_path = (find_case_fullpath(parent_id) + '').lstrip('->')
                        logger.info('正在更新测试计划用例树节点关联表记录')
                        query = "UPDATE website_api_case_tree_test_plan SET node_path='%s', sub_node_num=%s WHERE plan_id IN %s AND node_id = %s"
                        data = (node_path, sub_node_num, plan_id_list, node_id)
                        result = test_platform_db.execute_update(query, data)
                        if not result[0]:
                            logger.error('更新测试计划用例树节点关联表记录失败：%s' % result[1])
                            return [False, result[1]]
                        else:
                            result = [True, '']
                    elif result[0] and not result[1]:
                        logger.warn('用例树节点 %s 不存在' % node_id)
                        continue
                    else:
                        logger.error('查询用例树节点[ID:%s]信息出错，退出程序' % node_id)
                        exit()
                    temp_var = ''
                return  result
            elif result[0] and not result[1]:
                logger.error('未查找到与测试计划关联的用例树节点')
                result = [False, '未查找到与测试计划关联的用例树节点']
            else:
                logger.error('查找与测试计划关联的用例树节点失败:%s' % result[1])
                result = [False,  '查找与测试计划关联的用例树节点失败:%s' % result[1]]
            return result
        except Exception as e:
            logger.error('%s' % e)
            result = [False, '同步更新与待运行测试计划关联的用例树节点信息失败：%s' % e]
            return result


    def run(self, debug):
        try:
            if_plan_run_fail = False
            plan_id_list_for_failure = [] # 存放执行失败、未执行的测试计划的ID

            logger.info('======================正在同步更新与待运行测试计划关联的所有用例树节点信息======================')
            result = self.sync_case_tree_node_info_for_testplans()
            if not result[0]:
                logger.error('同步更新与待运行测试计划关联的所有用例树节点信息失败')
                return result
            else:
                logger.info('同步更新与待运行测试计划关联的所有用例树节点信息成功')

            for plan_id in self.plan_id_list:
                 logger.info('正在查询测试计划[ID：%s]相关信息' % plan_id)
                 result = test_platform_db.select_one_record('SELECT plan_name,valid_flag FROM `website_api_test_plan` WHERE id = %s', (plan_id,))
                 if result[0] and result[1]:
                     plan_name, valid_flag = result[1]
                     if valid_flag == '启用':
                         logger.info('======================开始运行测试计划[名称：%s, ID：%s]======================' % (plan_name, plan_id))
                         test_plan = TestPlan(plan_id, plan_name, self.project_id, self.project_name, self.protocol, self.host, self.port, self.global_headers)
                         result = test_plan.run(debug)
                         if not result[0]:
                             if_plan_run_fail = True
                             plan_id_list_for_failure.append(plan_id)
                     else:
                         logger.warn('测试计划已被禁用，跳过执行')
                         if_plan_run_fail = True
                         plan_id_list_for_failure.append(plan_id)
                         continue
                 elif result[0] and not result[1]:
                     logger.warn('运行失败:未查询到计划相关信息')
                     return [False, '运行失败:未查询到计划相关信息']
                 else:
                     return [False, '运行失败：%s' % result[1]]

            if if_plan_run_fail:
                return [False, '测试计划%s运行失败' % str(plan_id_list_for_failure)]
            else:
                return [True, '']
        except Exception as e:
            logger.error('%s' % e)
            return [False, '运行失败：%s' % e]
