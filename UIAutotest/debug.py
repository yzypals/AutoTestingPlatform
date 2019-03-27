#!/usr/bin/env python
#-*-encoding:utf-8-*-

__author__ = 'shouke'

import time
import re

from common.log import logger
from common.globalvar import test_platform_db
from test_case import TestCase
from common.mydb import MyDB
from common.globalvar import db_related_to_project_dic
from common.globalvar import global_variable_dic
from common.seleniumutil import selenium_util


class Debug:
    def __init__(self):
       pass

    def run(self, project_id, id, browser):
        try:
            logger.info('正在查询项目[ID：%s]相关信息' % project_id)
            result = test_platform_db.select_one_record('SELECT home_page, environment_id, valid_flag '
                                                        'FROM `website_ui_project_setting` WHERE id = %s', (project_id,))
            if result[0] and result[1]:
                home_page, environment_id, valid_flag = result[1]

                logger.info('正在查询与项目关联的数据库信息')
                result = test_platform_db.select_many_record("SELECT db_type, db_alias, db_name, db_host, db_port, db_user, db_passwd "
                                                             "FROM `website_database_setting` "
                                                             "WHERE  locate('UI%s', project_id) != 0  AND environment_id= '%s'" % (project_id, environment_id))

                if result[0] and result[1]:
                    for record in result[1]:
                        db_type, db_alias, db_name, db_host, db_port, db_user, db_passwd = record
                        if db_type == 'MySQL':
                            mydb = MyDB(db_name=db_name, db_host=db_host, port=db_port, user=db_user, password=db_passwd, charset='utf8')
                            db_related_to_project_dic[db_alias] = mydb
                elif not result[0]:
                    logger.error('查询项目相关的数据库配置信息出错：%s' % result[1])
                    return [False, result[1]]

                logger.info('正在查询与项目关联的全局变量')
                result = test_platform_db.select_many_record("SELECT `name`, `value` "
                                                             "FROM `website_global_variable_setting` "
                                                             "WHERE  project_type='UI项目' AND locate('%s', project_id) != 0 AND locate('%s', env_id) != 0 " % (self.project_id, environment_id))

                if result[0] and result[1]:
                    for record in result[1]:
                        name, value = record
                        name = name
                        global_variable_dic[name] = value
                elif not result[0]:
                    logger.error('查询项目相关的全局变量配置信息出错：%s' % result[1])
                    return [False, result[1]]

                host_port = re.findall('[https|http]+://[^/]+', home_page) # 获取http地址 形如 http://www.baidu.com, http://www.baidu.com:8080
                if host_port:
                    host_port = host_port[0]
                else:
                    return [False, '项目主页填写错误']

                logger.info('正在查询输入ID标识的用例(套件)相关信息')
                query = 'SELECT id, text FROM `website_ui_case_tree` WHERE project_id = %s AND id = %s' % (project_id, id)
                result = test_platform_db.select_one_record(query)

                logger.info('正在获取浏览器驱动')
                result_get = selenium_util.set_driver(browser)
                if not result_get[0]:
                    logger.error('获取浏览器驱动出错，退出')
                    exit()
                browser_driver = selenium_util.get_driver()

                logger.info('正在打开项目主页：%s' % home_page)
                selenium_util.maximize_window()
                selenium_util.get(home_page)
                selenium_util.implicitly_wait(20)
                try:
                    if result[0] and result[1]:
                        record = result[1]
                        case_id, case_name = record
                        execution_num = str(int(time.time())) # 执行编号

                        query = 'SELECT id, text FROM `website_ui_case_tree` WHERE project_id = %s AND parent_id = %s  ' \
                                'AND id NOT IN (SELECT parent_id FROM `website_ui_case_tree` WHERE project_id=%s)' \
                                'ORDER BY `order` ASC' % (project_id, id, project_id)
                        result = test_platform_db.select_many_record(query)

                        if result[0] and result[1]:
                            logger.info('输入ID标识的是测试套件')
                            records = result[1]

                            for record in records:
                                case_id, case_name = record
                                test_case = TestCase(execution_num, 0, case_id, '--', case_name, host_port)
                                logger.info('======================开始运行测试用例[名称：%s, ID:%s]======================' % (case_name, case_id))
                                result = test_case.run(True)
                                if not result[0]:
                                    return [False, '用例（ID:%s 名称：%s）运行出错：%s' % (case_id, case_name, result[2])]
                        elif result[0] and not result[1]:
                            logger.info('输入ID标识的是测试用例，开始执行用例')
                            test_case = TestCase(execution_num, 0, case_id, '--', case_name, host_port)
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
                except Exception as e:
                    logger.error('运行出错：%s' % e)
                finally:
                     browser_driver.quit()
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
