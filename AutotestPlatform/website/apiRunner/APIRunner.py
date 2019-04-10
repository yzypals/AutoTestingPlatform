#!/usr/bin/env python
#-*-encoding:utf-8-*-

__author__ = 'shouke'

import time
import json

from .common.log import logger
from .test_case import TestCase
from .common.mydb import MyDB
from .running_plan import RunningPlan
from .common.redis_client import RedisClient
from .common.globalvar import db_related_to_project_dic
from .common.globalvar import redis_related_to_project_dic
from .common.globalvar import global_variable_dic
from .test_plan import TestPlan

from collections import OrderedDict

class APIRunner:
    def __init__(self, log_websocket_consumer):
        self.log_websocket_consumer = log_websocket_consumer
        self.test_platform_db = MyDB(log_websocket_consumer, db='TESTPLATFORM')

    def debug_case_or_suit(self, project_id, id):
        '''调试运行单个用例或者单个测试套件'''
        try:
            msg = '正在查询项目[ID：%s]相关信息' % project_id
            logger.info(msg)
            self.log_websocket_consumer.info(msg)

            result = self.test_platform_db.select_one_record('SELECT protocol, host, port, environment_id, valid_flag '
                                                             'FROM `website_api_project_setting` WHERE id = %s', (project_id,))
            if result[0] and result[1]:
                protocol, host, port, environment_id, valid_flag = result[1]

                msg = '正在查询与项目关联的数据库信息'
                logger.info(msg)
                self.log_websocket_consumer.info(msg);
                result = self.test_platform_db.select_many_record("SELECT db_type, db_alias, db_name, db_host, db_port, db_user, db_passwd "
                                                                  "FROM `website_database_setting` "
                                                                  "WHERE  locate('API%s', project_id) != 0 AND environment_id= '%s'" %  (project_id, environment_id))
                if result[0] and result[1]:
                    for record in result[1]:
                        db_type, db_alias, db_name, db_host, db_port, db_user, db_passwd = record
                        if db_type == 'MySQL':
                            mydb = MyDB(self.log_websocket_consumer, db_name=db_name, db_host=db_host, port=db_port, user=db_user, password=db_passwd, charset='utf8')
                            db_related_to_project_dic[db_alias] = mydb
                        elif db_type == 'Redis':
                            if not db_passwd.strip():
                                db_passwd = None
                            if db_name.strip() == '':
                                db_name = '0'
                            myredis = RedisClient(self.log_websocket_consumer, host=db_host, port=db_port, password=db_passwd, db=db_name, charset='utf-8')
                            redis_related_to_project_dic[db_alias] = myredis

                elif not result[0]:
                    msg = '查询项目相关的数据库配置信息出错：%s' % result[1]
                    logger.error(msg)
                    self.log_websocket_consumer.error(msg)
                    return [False, msg]

                logger.info('正在查询与项目关联的全局变量')
                result = self.test_platform_db.select_many_record("SELECT `name`, `value` "
                                                                  "FROM `website_global_variable_setting` "
                                                                  "WHERE  project_type='API项目' AND locate('%s', project_id) != 0 AND locate('%s', env_id) != 0 " % (project_id, environment_id))
                if result[0] and result[1]:
                    for record in result[1]:
                        name, value = record
                        name = name
                        global_variable_dic[name] = value
                elif not result[0]:
                    msg = '查询项目相关的全局变量配置信息出错：%s' % result[1]
                    logger.error(msg)
                    self.log_websocket_consumer.error(msg)
                    return [False, msg]

                try:
                    if 'global_headers' in global_variable_dic.keys():
                        global_headers =  global_variable_dic['global_headers']
                        # 防止用户输入了中文冒号，替换为英文冒号,不然经过global_headers.encode("utf-8").decode("latin1")这样编码转换，
                        # 会把"key"：中的中文冒号解码为非英文冒号，导致执行json loads函数时会报错；
                        # 另外，请求头从数据库读取，可能涉及到换行符，需要去掉
                        global_headers = global_headers.replace('：', ':').replace('\t', '')
                        global_headers = json.loads(global_headers, object_pairs_hook=OrderedDict)
                    else:
                        global_headers = {}
                except Exception as e:
                    msg = '%s' % e
                    logger.error(msg)
                    self.log_websocket_consumer.error(msg)
                    return [False, msg]

                msg = '正在查询ID:%s标识的用例(套件)相关信息' % id
                logger.info(msg)
                self.log_websocket_consumer.info(msg)
                query = 'SELECT id, text FROM `website_api_case_tree` WHERE project_id = %s AND id = %s' % (project_id, id)
                result = self.test_platform_db.select_one_record(query)

                if result[0] and result[1]:
                    record = result[1]
                    case_id, case_name = record
                    execution_num = str(int(time.time())) # 执行编号

                    query = 'SELECT id, text FROM `website_api_case_tree` WHERE project_id = %s AND parent_id = %s  ' \
                            'AND id NOT IN (SELECT parent_id FROM `website_api_case_tree` WHERE project_id=%s)' \
                            'ORDER BY `order` ASC' % (project_id, id, project_id)
                    result = self.test_platform_db.select_many_record(query)
                    if result[0] and result[1]:
                        msg = 'ID标识的是测试套件'
                        logger.info(msg)
                        self.log_websocket_consumer.info(msg)
                        records = result[1]
                        for record in records:
                            case_id, case_name = record
                            test_case = TestCase(execution_num, 0, case_id, '--', case_name, protocol, host, port, global_headers, self.log_websocket_consumer, self.test_platform_db)

                            msg = '======================开始运行测试用例[名称：%s, ID:%s]======================' % (case_name, case_id)
                            logger.info(msg)
                            self.log_websocket_consumer.info(msg)
                            result = test_case.run(True)
                            if not result[0]:
                                msg = '用例（ID:%s 名称：%s）运行出错：%s' % (case_id, case_name, result[2])
                                logger.error(msg)
                                self.log_websocket_consumer.error(msg)
                                return [False, msg]
                        return [True, '调试运行成功']
                    elif result[0] and not result[1]:
                        msg = 'ID标识的是测试用例，开始执行用例'
                        logger.info(msg)
                        self.log_websocket_consumer.info(msg)

                        test_case = TestCase(execution_num, 0, case_id, '--', case_name, protocol, host, port, global_headers, self.log_websocket_consumer, self.test_platform_db)

                        msg = '======================开始运行测试用例[名称：%s, ID:%s]======================' % (case_name, case_id)
                        logger.info(msg)
                        self.log_websocket_consumer.info(msg)

                        result = test_case.run(True)
                        if not result[0]:
                            msg = '用例（ID:%s 名称：%s）运行出错：%s' % (case_id, case_name, result[2])
                            logger.error(msg)
                            self.log_websocket_consumer.error(msg)
                            return [False, msg]
                        else:
                            return[True, '调试运行成功']
                    else:
                        msg = '查询出错:%s' % result[1]
                        logger.error(msg)
                        self.log_websocket_consumer.error(msg)
                        return [False, msg]

                elif result[0] and not result[1]:
                    reason = '未查找到相关信息，请检查项目ID(%s)，用例(套件)标识ID(%s)是否正确'
                    logger.warn(reason)
                    self.log_websocket_consumer.warn(reason)
                    return [False, reason]
                else:
                    msg = '查找相关信息失败：%s' % result[1]
                    logger.error(msg)
                    self.log_websocket_consumer.error(msg)
                    return [False, msg]
            elif result[0] and not result[1]:
                msg = '未查询到项目相关的信息'
                logger.error(msg)
                self.log_websocket_consumer.error(msg)
                return [False, msg]
            else:
                msg = '查询项目相关信息失败：%s' % result[1]
                logger.error(msg)
                self.log_websocket_consumer.error(msg)
                return [False, msg]
        except Exception as e:
            msg = '%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
            return [False, msg]
        finally:
            msg = '正在释放资源'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)

            msg = '正在关闭数据库连接'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)

            for key, db in db_related_to_project_dic.copy().items():
                db.close()
                del db_related_to_project_dic[key]
            self.test_platform_db.close()

            msg = '正在清理与项目关联的全局变量'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            global_variable_dic.clear()

    def debug_test_plan(self, plan_id):
        '''调试运行单个测试计划'''
        try:
            msg = '正在查询测试计划[ID：%s]相关信息' % plan_id
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            result = self.test_platform_db.select_one_record('SELECT plan_name, valid_flag, project_id, project_name FROM `website_api_test_plan` WHERE id = %s', (plan_id,))
            if result[0] and result[1]:
                plan_name, switch, project_id, project_name = result[1]

                msg = '正在查询与计划关联的项目相关信息'
                logger.info(msg)
                self.log_websocket_consumer.info(msg)
                result = self.test_platform_db.select_one_record('SELECT protocol, host, port, environment_id, valid_flag '
                                                                 'FROM `website_api_project_setting` WHERE id = %s', (project_id,))
                if result[0] and result[1]:
                    protocol, host, port, environment_id, valid_flag = result[1]
                    if valid_flag  == '启用':
                        msg = '正在查询与项目关联的数据库信息'
                        logger.info(msg)
                        self.log_websocket_consumer.info(msg)
                        result = self.test_platform_db.select_many_record("SELECT db_type, db_alias, db_name, db_host, db_port, db_user, db_passwd "
                                                                          "FROM `website_database_setting` "
                                                                          "WHERE locate('API%s', project_id) != 0 AND environment_id= '%s'" %  (project_id, environment_id))
                        if result[0] and result[1]:
                            for record in result[1]:
                                db_type, db_alias, db_name, db_host, db_port, db_user, db_passwd = record
                                if db_type == 'MySQL':
                                    mydb = MyDB(self.log_websocket_consumer, db_name=db_name, db_host=db_host, port=db_port, user=db_user, password=db_passwd, charset='utf8')
                                    db_related_to_project_dic[db_alias] = mydb
                                elif db_type == 'Redis':
                                    if not db_passwd.strip():
                                        db_passwd = None
                                    if db_name.strip() == '':
                                        db_name = '0'
                                    myredis = RedisClient(self.log_websocket_consumer, host=db_host, port=db_port, password=db_passwd, db=db_name, charset='utf-8')
                                    redis_related_to_project_dic[db_alias] = myredis
                        elif not result[0]:
                            msg = '查询项目相关的数据库配置信息出错：%s' % result[1]
                            logger.error(msg)
                            self.log_websocket_consumer.error(msg)
                            return [False, msg]

                        msg = '正在查询与项目关联的全局变量'
                        logger.info(msg)
                        self.log_websocket_consumer.info(msg)
                        result = self.test_platform_db.select_many_record("SELECT `name`, `value` "
                                                                          "FROM `website_global_variable_setting` "
                                                                          "WHERE  project_type='API项目' AND locate('%s', project_id) != 0 AND locate('%s', env_id) != 0 ", (project_id, environment_id))
                        if result[0] and result[1]:
                            for record in result[1]:
                                name, value = record
                                name = name
                                global_variable_dic[name] = value
                        elif not result[0]:
                            msg = '查询项目相关的全局变量配置信息出错：%s' % result[1]
                            logger.error(msg)
                            self.log_websocket_consumer.error(msg)
                            return [False, msg]

                        if 'global_headers' in global_variable_dic.keys():
                            global_headers =  global_variable_dic['global_headers']
                            # 防止用户输入了中文冒号，替换为英文冒号,不然经过global_headers.encode("utf-8").decode("latin1")这样编码转换，
                            # 会把"key"：中的中文冒号解码为非英文冒号，导致执行json loads函数时会报错；
                            # 另外，请求头从数据库读取，可能涉及到换行符，需要去掉
                            global_headers = global_headers.replace('：', ':').replace('\t', '')
                            global_headers = json.loads(global_headers, object_pairs_hook=OrderedDict)
                        else:
                            global_headers = {}

                        if switch == '启用':
                            msg = '======================开始运行测试计划[名称：%s, ID：%s]======================' % (plan_name, plan_id)
                            logger.info(msg)
                            self.log_websocket_consumer.info(msg)
                            test_plan = TestPlan(plan_id, plan_name, project_id, project_name, protocol, host, port, global_headers, self.test_platform_db, self.log_websocket_consumer)
                            result = test_plan.run(True)
                            if not result[0]:
                                msg = '调试运行失败：%s' % result[1]
                                logger.info(msg)
                                self.log_websocket_consumer.info(msg)
                                return [False, msg]
                            else:
                                return [True, '调试运行成功']
                        else:
                            msg = '测试计划已被禁用'
                            logger.warn(msg)
                            self.log_websocket_consumer.warn(msg)
                            return [False, msg]
                    else:
                        msg = '测试计划运行失败，计划关联的项目%s已被禁用' % project_name
                        logger.warn(msg)
                        self.log_websocket_consumer.warn(msg)
                        return [False, msg]
            elif result[0] and not result[1]:
                msg = '运行失败:未查询到计划相关信息'
                logger.warn(msg)
                self.log_websocket_consumer.warn(msg)
                return [False, msg]
            else:
                msg = '运行失败：%s' % result[1]
                logger.error(msg)
                self.log_websocket_consumer.error(msg)
                return [False, msg]
        except Exception as e:
            msg = '%s' % e
            logger.error(msg)
            self.log_websocket_consumer.error(msg)
            return [False, msg]
        finally:
            msg = '正在释放资源'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)

            msg = '正在关闭数据库连接'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            for key, db in db_related_to_project_dic.copy().items():
                db.close()
                del db_related_to_project_dic[key]
            self.test_platform_db.close()

            msg = '正在清理与项目关联的全局变量'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            global_variable_dic.clear()


    def run_running_plan(self, running_plan_no, debug=False): # debug True 调试模式
        '''(调试)运行单个运行计划'''
        try:
            msg = '当前运行计划编码为：%s， 正在查询该运行计划相关信息' % running_plan_no
            logger.info(msg)
            self.log_websocket_consumer.info(msg)

            result = self.test_platform_db.select_one_record('SELECT running_plan_name,project_id, project_name, plan_name, plan_id, valid_flag '
                                                             'FROM `website_running_plan` WHERE running_plan_num =%s', (running_plan_no,))
            if result[0] and result[1]:
                running_plan_name, project_id, project_name, plan_name, plan_id_list, valid_flag = result[1]
                plan_id_list = plan_id_list.split(',') # 转字符串表示的list为列表
                msg = '待运行项目：名称：%s，ID：%s，关联的测试计划有：%s' % (project_name, project_id, plan_name)
                logger.info(msg)
                self.log_websocket_consumer.info(msg)
                if valid_flag == '启用':
                    running_plan = RunningPlan(running_plan_no, running_plan_name, project_id, project_name, plan_name, plan_id_list, self.test_platform_db, self.log_websocket_consumer)
                    msg = '======================开始执行运行计划[名称：%s]======================' % running_plan_name
                    logger.info(msg)
                    self.log_websocket_consumer.info(msg)
                    result = running_plan.run(debug)
                    if not debug:
                        run_result = result[0]
                        if result[0]:
                            run_result = result[0]
                            mark = result[1]
                        else:
                            mark = result[2]
                            logger.error(mark)
                            self.log_websocket_consumer.error(mark)

                        msg = '正在更新数据库运行计划的运行状态'
                        logger.info(msg)
                        self.log_websocket_consumer.info(msg)
                        update_query = "UPDATE `website_running_plan` SET running_status ='%s', remark='%s' WHERE running_plan_num= %s"
                        data = (result[1], result[2].replace("'",'\"'), running_plan_no)
                        result = self.test_platform_db.execute_update(update_query, data)
                        if not result[0]:
                            msg = '更新数据库运行计划的运行状态失败：%s' % result[1]
                            logger.error(msg)
                            self.log_websocket_consumer.error(msg)
                            mark = mark + '&' + msg
                        return [run_result, mark]
                    else:
                        return [result[0], result[2]]
                else:
                    msg = '执行失败，运行计划已被禁用'
                    logger.warn(msg)
                    self.log_websocket_consumer.warn(msg)
                    return [False, msg]
            elif result[0] and not result[1]:
                msg = '未查询到运行计划相关的信息'
                logger.error(msg)
                self.log_websocket_consumer.error(msg)
                return [False, msg]
            else:
                msg = '查询运行计划相关信息失败：%s' % result[1]
                logger.error(msg)
                self.log_websocket_consumer.error(msg)
                return [False, msg]
        except Exception as e:
            msg = '%s' % e
            logger.error(msg)
            return [False, msg]
        finally:
            msg = '正在释放资源'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)

            msg = '正在关闭数据库连接'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            self.test_platform_db.close()

            msg = '正在清理与项目关联的全局变量'
            logger.info(msg)
            self.log_websocket_consumer.info(msg)
            global_variable_dic.clear()





