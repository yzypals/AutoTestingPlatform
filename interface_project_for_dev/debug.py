#!/usr/bin/env python
#-*-encoding:utf-8-*-

__author__ = 'shouke'

import time
import json

from common.log import logger
from common.globalvar import test_platform_db
from test_case import TestCase
from common.mydb import MyDB
from common.redis_client import RedisClient
from common.globalvar import db_related_to_project_dic
from common.globalvar import redis_related_to_project_dic

from common.globalvar import global_variable_dic

from collections import OrderedDict

class Debug:
    def __init__(self):
       pass

    def run(self, project_id, id):
        try:
            logger.info('正在查询项目[ID：%s]相关信息' % project_id)
            result = test_platform_db.select_one_record('SELECT protocol, host, port, environment, valid_flag '
                                                        'FROM `website_api_project_setting` WHERE id = %s', (project_id,))
            if result[0] and result[1]:
                protocol, host, port, environment, valid_flag = result[1]

                logger.info('正在查询与项目关联的数据库信息')
                result = test_platform_db.select_many_record("SELECT db_type, db_alias, db_name, db_host, db_port, db_user, db_passwd "
                                                             "FROM `website_database_setting` "
                                                             "WHERE  locate('API%s', project_id) != 0 AND environment= '%s'" %  (project_id, environment))
                if result[0] and result[1]:
                    for record in result[1]:
                        db_type, db_alias, db_name, db_host, db_port, db_user, db_passwd = record
                        if db_type == 'MySQL':
                            mydb = MyDB(db_name=db_name, db_host=db_host, port=db_port, user=db_user, password=db_passwd, charset='utf8')
                            db_related_to_project_dic[db_alias] = mydb
                        elif db_type == 'Redis':
                            if not db_passwd.strip():
                                db_passwd = None
                            if db_name.strip() == '':
                                db_name = '0'
                            myredis = RedisClient(host=db_host, port=db_port, password=db_passwd, db=db_name, charset='utf-8')
                            redis_related_to_project_dic[db_alias] = myredis

                elif not result[0]:
                    logger.error('查询项目相关的数据库配置信息出错：%s' % result[1])
                    return [False, result[1]]

                logger.info('正在查询与项目关联的全局变量')
                result = test_platform_db.select_many_record("SELECT `name`, `value` "
                                                             "FROM `website_global_variable_setting` "
                                                             "WHERE project_id = %s AND environment= %s", (project_id, environment))
                if result[0] and result[1]:
                    for record in result[1]:
                        name, value = record
                        name = name
                        global_variable_dic[name] = value
                elif not result[0]:
                    logger.error('查询项目相关的全局变量配置信息出错：%s' % result[1])
                    return [False, result[1]]

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
                    logger.error('%s' % e)
                    return [False, '%s' % e]

                logger.info('正在查询输入ID标识的用例(套件)相关信息')
                query = 'SELECT id, text FROM `website_api_case_tree` WHERE project_id = %s AND id = %s' % (project_id, id)
                result = test_platform_db.select_one_record(query)

                if result[0] and result[1]:
                    record = result[1]
                    case_id, case_name = record
                    execution_num = str(int(time.time())) # 执行编号

                    query = 'SELECT id, text FROM `website_api_case_tree` WHERE project_id = %s AND parent_id = %s  ' \
                            'AND id NOT IN (SELECT parent_id FROM `website_api_case_tree` WHERE project_id=%s)' \
                            'ORDER BY `order` ASC' % (project_id, id, project_id)
                    result = test_platform_db.select_many_record(query)
                    if result[0] and result[1]:
                        logger.info('输入ID标识的是测试套件')
                        records = result[1]
                        for record in records:
                            case_id, case_name = record
                            test_case = TestCase(execution_num, 0, case_id, '--', case_name, protocol, host, port, global_headers)
                            logger.info('======================开始运行测试用例[名称：%s, ID:%s]======================' % (case_name, case_id))
                            result = test_case.run(True)
                            if not result[0]:
                                return [False, '用例（ID:%s 名称：%s）运行出错：%s' % (case_id, case_name, result[2])]

                    elif result[0] and not result[1]:
                        logger.info('输入ID标识的是测试用例，开始执行用例')
                        test_case = TestCase(execution_num, 0, case_id, '--', case_name, protocol, host, port, global_headers)
                        logger.info('======================开始运行测试用例[名称：%s, ID:%s]======================' % (case_name, case_id))
                        result = test_case.run(True)
                        if not result[0]:
                            return [False, '用例（ID:%s 名称：%s）运行出错：%s' % (case_id, case_name, result[2])]
                    else:
                        logger.error('查询出错:%s' % result[1])
                        return [False, result[1]]
                elif result[0] and not result[1]:
                    reason = '未查找到相关信息，请检查配置的项目ID(%s)，用例(套件)标识ID(%s)是否正确'
                    logger.warn(reason)
                    return [False, reason]
                else:
                    logger.error('查找相关信息失败：%s' % result[1])
                    return [False, '查找相关信息失败：%s' % result[1]]

            elif result[0] and not result[1]:
                logger.error('未查询到项目相关的信息')
                return [False, '未查询到项目相关的信息']
            else:
                logger.error('查询项目相关信息失败：%s' % result[1])
                return [False, '查询项目相关信息失败：%s' % result[1]]
        except Exception as e:
            logger.error('%s' % e)
            return [False,  '%s'% e]
        finally:
            logger.info('正在释放资源')
            logger.info('正在断开与项目关联的数据库连接')
            # 关闭数据库
            for key, db in db_related_to_project_dic.copy().items():
                db.close()
                del db_related_to_project_dic[key]

            logger.info('正在清理与项目关联的全局变量')
            global_variable_dic.clear()
