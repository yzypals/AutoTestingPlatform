#!/usr/bin/env python
#-*-encoding:utf-8-*-

__author__ = 'shouke'

from common.log import logger
from common.globalvar import test_platform_db
from common.globalvar import db_related_to_project_dic
from common.globalvar import global_variable_dic
from common.mydb import MyDB
from test_project import TestProject

class RunningPlan:
    def __init__(self, running_plan_num, running_plan_name, project_id, project_name, plan_name, plan_id_list):
        self.running_plan_num = running_plan_num
        self.running_plan_name = running_plan_name
        self.project_id = project_id
        self.project_name = project_name
        self.plan_name = plan_name
        self.plan_id_list = plan_id_list

    def run(self, debug):
        try:
            logger.info('正在查询项目[ID：%s,名称：%s]相关信息' % (self.project_id, self.project_name))
            result = test_platform_db.select_one_record('SELECT home_page, environment_id, valid_flag '
                                                        'FROM `website_ui_project_setting` WHERE id = %s', (self.project_id,))

            if result[0] and result[1]:
                home_page, environment_id, valid_flag = result[1]
                if valid_flag  == '启用':
                    logger.info('正在查询与项目关联的数据库信息')
                    result = test_platform_db.select_many_record("SELECT db_type, db_alias, db_name, db_host, db_port, db_user, db_passwd "
                                                                 "FROM `website_database_setting` "
                                                                 "WHERE  locate('UI%s', project_id) != 0  AND environment_id= '%s'" % (self.project_id, environment_id))
                    if result[0] and result[1]:
                        for record in result[1]:
                            db_type, db_alias, db_name, db_host, db_port, db_user, db_passwd = record
                            if db_type == 'MySQL':
                                mydb = MyDB(db_name=db_name, db_host=db_host, port=db_port, user=db_user, password=db_passwd, charset='utf8')
                                db_related_to_project_dic[db_alias] = mydb
                    elif not result[0]:
                        logger.error('查询项目相关的数据库配置信息出错：%s' % result[1])
                        return [False, '运行失败', result[1]]

                    logger.info('正在查询与项目关联的全局变量')
                    result = test_platform_db.select_many_record("SELECT `name`, `value` "
                                                                 "FROM `website_global_variable_setting` "
                                                                 "WHERE  project_type='UI项目' AND locate('%s', project_id) != 0 AND locate('%s', env_id) != 0 ", (self.project_id, environment_id))
                    if result[0] and result[1]:
                        for record in result[1]:
                            name, value = record
                            name = name
                            global_variable_dic[name] = value
                    elif not result[0]:
                        logger.error('查询项目相关的全局变量配置信息出错：%s' % result[1])
                        return [False, '运行失败', result[1]]

                    try:
                        test_project = TestProject(self.project_id, self.project_name, home_page, self.plan_id_list)
                        logger.info('======================开始运行测试项目[名称：%s, ID：%s]======================' % (self.project_name, self.project_id))
                        result = test_project.run(debug)

                        if not result[0]:
                            result = [False, '运行失败', result[1]]
                        else:
                            result = [True, '运行成功', '']
                    except Exception as e:
                        logger.error('%s' % e)
                        result = [False, '运行失败', '%s' % e]
                else:
                    logger.warn('项目已被禁用，结束运行')
                    result = [False, '运行失败', '项目已被禁用，结束运行']
            elif result[0] and not result[1]:
                logger.error('未查询到项目相关的信息')
                result = [False, '运行失败', '未查询到项目相关的信息']
            else:
                logger.error('查询项目相关信息失败：%s' % result[1])
                result = [False, '运行失败', '查询项目相关信息失败：%s' % result[1]]
        except Exception as e:
            logger.error('%s' % e)
            result =  [False, '运行失败', '%s'% e]
        finally:
            logger.info('正在释放资源')
            logger.info('正在断开与项目关联的数据库连接')
            # 关闭数据库
            for key, db in db_related_to_project_dic.copy().items():
                db.close()
                del db_related_to_project_dic[key]

            logger.info('正在清理与项目关联的全局变量')
            global_variable_dic.clear()
            return result




