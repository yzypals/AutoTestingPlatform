#!/usr/bin/env python
#-*-encoding:utf-8-*-

__author__ = 'shouke'

import sys
import platform

from common.log import logger
from common.globalvar import test_platform_db
from running_plan import RunningPlan
from debug import Debug

if __name__ == '__main__':
    try:
        logger.info('执行当前脚本的Python版本：%s' % platform.python_version())

        run_mode = sys.argv[1]
        logger.info('当前运行模式为：%s' % run_mode)

        running_plan_num = sys.argv[2]
        logger.info('当前运行计划编号为：%s' % running_plan_num)

        temp_var = sys.argv[3:4]
        if temp_var:
            if temp_var[0].lower() == 'debug':
                is_debug = True
        else:
            is_debug = False

        if run_mode.lower() == 'rop':
            logger.info('运行单项目,待执行的运行计划编码：%s' % running_plan_num)
            logger.info('正在查询运行计划相关信息')
            try:
                result = test_platform_db.select_one_record('SELECT running_plan_name,project_id, project_name, plan_name, plan_id, valid_flag '
                                                        'FROM `website_running_plan` WHERE running_plan_num =%s', (running_plan_num,))
                if result[0] and result[1]:
                    running_plan_name, project_id, project_name, plan_name, plan_id_list, valid_flag = result[1]
                    plan_id_list = list(eval(plan_id_list + ','),) # 转字符串表示的list为列表
                    logger.info('待运行项目：名称：%s，ID：%s，关联的测试计划有：%s' % (project_name, project_id, plan_name))
                    if valid_flag == '启用':
                        running_plan = RunningPlan(running_plan_num, running_plan_name, project_id, project_name, plan_name, plan_id_list)
                        logger.info('======================开始执行运行计划[名称：%s]======================' % running_plan_name)
                        result = running_plan.run(is_debug)
                        if result[0]:
                            logger.info('执行成功，正在更新数据库运行计划的运行状态')
                        else:
                            logger.info('执行失败，正在更新数据库运行计划的运行状态')

                        if not is_debug:
                            update_query = "UPDATE `website_running_plan` SET running_status ='%s', remark='%s' WHERE running_plan_num= %s"
                            data = (result[1], result[2].replace("'",'\"'), running_plan_num)
                            result = test_platform_db.execute_update(update_query, data)
                            if not result[0]:
                                logger.error('更新数据库运行计划的运行状态失败：%s' % result[1])
                    else:
                        logger.warn('执行失败，运行计划已被禁用')
                elif result[0] and not result[1]:
                    logger.error('未查询到运行计划相关的信息')
                else:
                    logger.error('查询运行计划相关信息失败：%s' % result[1])
            except Exception as e:
                logger.error('%s' % e)
        elif run_mode.lower() == 'rap':
            logger.info('运行所有项目')
        elif run_mode.lower() == 'debug':
            logger.info('调试模式')
            try:
                input_id = ''
                while not input_id.isdigit():
                    input_id = input('请输入用例ID、套件ID：')
                    if not input_id.isdigit():
                        logger.warn('ID只能输为数字')
                    Debug().run(running_plan_num, input_id)
            except Exception as e:
                logger.error('%s' % e)

    except Exception as e:
        logger.error('运行出错：%s' % e)
    finally:
        test_platform_db.close()
