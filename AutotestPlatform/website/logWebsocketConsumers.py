#!/usr/bin/env python

#-*-encoding:utf-8-*-

__author__ = 'shouke'

from django.conf import settings
from channels.generic.websocket import WebsocketConsumer
import json
import sys
import os
import time
import platform
import threading
import traceback

from website.apiRunner.common.log import logger
from website.apiRunner.APIRunner import APIRunner


web_debug_log_level = settings.WEB_DEBUG_LOG_LEVEL.lower().strip()


class LogWebsocketConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thread = None

    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass



    def receive(self, text_data):
        try:
            mark = False
            text_data_json = json.loads(text_data)
            task_type = text_data_json['task_type']
            message = text_data_json['message']
            node_id = text_data_json['node_id']
            project_id = text_data_json['project_id']
            plan_id = text_data_json['plan_id']
            running_plan_no = text_data_json['running_plan_no']

            mark =  True # 标记程序是否执行到这里,如果没走到这里，则需要给web页面发送taskEnd
            if message == 'taskBegin' and not self.thread:
                message = 'clearLog'
                self.send(text_data=json.dumps({'message':message}))
                if task_type == 'debugAPICaseOrSuit':
                    self.thread = threading.Thread(target=self.debug_api_case_or_suite,
                                                   name="debug_api_case_or_suite",
                                                   args=(project_id, node_id))
                elif task_type == 'debugAPITestPlan':
                    self.thread = threading.Thread(target=self.debug_api_test_plan,
                                                   name="debug_api_test_plan",
                                                   args=(plan_id,))
                elif task_type == 'debugAPIRunningPlan':
                     self.thread = threading.Thread(target=self.run_api_running_plan,
                                                   name="run_api_case_or_suite",
                                                   args=(running_plan_no, True))
                elif task_type == 'runAPIRunningPlan':
                     self.thread = threading.Thread(target=self.run_api_running_plan,
                                                   name="run_api_case_or_suite",
                                                   args=(running_plan_no, False))
                self.thread.start()
                self.send(text_data=json.dumps({'message':'taskBegin'}))
                self.info('开始调试运行')
            elif message == 'taskBegin' and self.thread :
                message = '执行失败，已有调试任务在运行'
                logger.error('执行失败，已有调试任务在运行')
                self.error(message)
        except Exception as e:
            msg = '运行出错：%s' % e
            logger.error(msg)
            self.error(msg)
            if not mark:
                self.send(text_data=json.dumps({'message':'taskEnd'}))


    def debug(self, msg):
        try:
            if web_debug_log_level in ['info', 'warn', 'error', 'critical']:
                return;

            timetuple = time.localtime() # 记录采样时间
            time_when_called = time.strftime('%Y-%m-%d %H:%M:%S', timetuple)
            code_line_when_called = sys._getframe().f_back.f_lineno # 获取被调用函数在被调用时所处代码行数
            result = traceback.extract_stack()
            caller = result[len(result)-2]
            file_path_when_called = str(caller).split(',')[0].lstrip('<FrameSummary file ') # 获取被调用函数所在模块文件路径
            file_name_when_called = os.path.basename(file_path_when_called)  # 获取被调用函数所在模块文件名称

            message = '<p style="color:#228B22">%s %s %s %s %s</p>' % (time_when_called, file_name_when_called, code_line_when_called, 'DEBUG', msg)
            self.send(text_data=json.dumps({'message': message}))
        except Exception as e:
            logger.error('发送debug日志失败:\n日志内容：%s\n 发送失败原因：%s' % (msg,e))

    def info(self, msg):
        try:
            if web_debug_log_level in ['warn', 'error', 'critical']:
                return;
            timetuple = time.localtime() # 记录采样时间
            time_when_called = time.strftime('%Y-%m-%d %H:%M:%S', timetuple)
            code_line_when_called = sys._getframe().f_back.f_lineno # 获取被调用函数在被调用时所处代码行数
            result = traceback.extract_stack()
            caller = result[len(result)-2]
            file_path_when_called = str(caller).split(',')[0].lstrip('<FrameSummary file ')
            file_name_when_called = os.path.basename(file_path_when_called)

            message = '<p style="color:#000000">%s %s %s %s %s</p>' % (time_when_called, file_name_when_called, code_line_when_called, 'INFO', msg)
            self.send(text_data=json.dumps({'message': message}))
        except Exception as e:
            logger.error('发送info日志失败:\n日志内容：%s\n 发送失败原因：%s' % (msg,e))

    def warn(self, msg):
        try:
            if web_debug_log_level in ['error', 'critical']:
                return;
            timetuple = time.localtime() # 记录采样时间
            time_when_called = time.strftime('%Y-%m-%d %H:%M:%S', timetuple)
            code_line_when_called = sys._getframe().f_back.f_lineno # 获取被调用函数在被调用时所处代码行数
            result = traceback.extract_stack()
            caller = result[len(result)-2]
            file_path_when_called = str(caller).split(',')[0].lstrip('<FrameSummary file ')
            file_name_when_called = os.path.basename(file_path_when_called) # 获取被调用函数所在模块文件名称

            message = '<p style="color:#FFD700">%s %s %s %s %s</p>' % (time_when_called, file_name_when_called, code_line_when_called, 'WARN', msg)
            self.send(text_data=json.dumps({'message': message}))
        except Exception as e:
            logger.error('发送warn日志失败:\n日志内容：%s\n 发送失败原因：%s' % (msg,e))

    def error(self, msg):
        try:
            if web_debug_log_level in ['critical']:
                return;
            timetuple = time.localtime() # 记录采样时间
            time_when_called = time.strftime('%Y-%m-%d %H:%M:%S', timetuple)
            code_line_when_called = sys._getframe().f_back.f_lineno # 获取被调用函数在被调用时所处代码行数
            result = traceback.extract_stack()
            caller = result[len(result)-2]
            file_path_when_called = str(caller).split(',')[0].lstrip('<FrameSummary file ')
            file_name_when_called = os.path.basename(file_path_when_called) # 获取被调用函数所在模块文件名称

            message = '<p style="color:#FF0000">%s %s %s %s %s</p>' % (time_when_called, file_name_when_called, code_line_when_called, 'ERROR', msg)
            self.send(text_data=json.dumps({'message': message}))
        except Exception as e:
            logger.error('发送error日志失败:\n日志内容：%s\n 发送失败原因：%s' % (msg,e))

    def critical(self, msg):
        try:
            timetuple = time.localtime() # 记录采样时间
            time_when_called = time.strftime('%Y-%m-%d %H:%M:%S', timetuple)
            code_line_when_called = sys._getframe().f_back.f_lineno # 获取被调用函数在被调用时所处代码行数
            result = traceback.extract_stack()
            caller = result[len(result)-2]
            file_path_when_called = str(caller).split(',')[0].lstrip('<FrameSummary file ')
            file_name_when_called = os.path.basename(file_path_when_called) # 获取被调用函数所在模块文件名称

            message = '<p style="color:#FF0000" >%s %s %s %s %s</p>' % (time_when_called, file_name_when_called, code_line_when_called, 'CRITICAL', msg)
            self.send(text_data=json.dumps({'message': message}))
        except Exception as e:
            logger.error('发送critical日志失败:\n日志内容：%s\n 发送失败原因：%s' % (msg,e))


    def debug_api_case_or_suite(self, project_id, case_or_suit_id):
        '''调试测试用例或者测试套件'''
        try:
            msg = '运行当前程序的Python版本：%s' % platform.python_version()
            logger.info(msg)
            self.info(msg)

            msg = '当前用例关联的项目ID为：%s' % project_id
            logger.info(msg)
            self.info(msg)

            result = APIRunner(self).debug_case_or_suit(project_id, case_or_suit_id)
            if result[0]:
                msg  = '调试运行成功'
                logger.info(msg)
                self.info(msg)
            else:
                msg = '调试运行失败：%s' % result[1]
                logger.error(msg)
                self.error(msg)
        except Exception as e:
            logger.error('调试运行失败：%s' % e)
            self.error('调试运行失败：%s' % e)
        finally:
            self.thread = None
            self.send(text_data=json.dumps({'message': 'taskEnd'}))

    def debug_api_test_plan(self, plan_id):
        '''调试测试计划'''
        try:
            msg = '运行当前程序的Python版本：%s' % platform.python_version()
            logger.info(msg)
            self.info(msg)

            msg = '当前测试计划id为：%s' % plan_id
            logger.info(msg)
            self.info(msg)

            result = APIRunner(self).debug_test_plan(plan_id)
            if result[0]:
                msg  = '调试运行成功'
                logger.info(msg)
                self.info(msg)
            else:
                msg = '调试运行失败：%s' % result[1]
                logger.error(msg)
                self.error(msg)
        except Exception as e:
            logger.error('调试运行失败：%s' % e)
            self.error('调试运行失败：%s' % e)
        finally:
            self.thread = None
            self.send(text_data=json.dumps({'message': 'taskEnd'}))

    def run_api_running_plan(self, runing_plan_no, debug=False):
        '''调试运行计划'''
        '''调试测试计划'''
        try:
            msg = '运行当前程序的Python版本：%s' % platform.python_version()
            logger.info(msg)
            self.info(msg)

            msg = '当前运行计划编码为：%s' % runing_plan_no
            logger.info(msg)
            self.info(msg)

            result = APIRunner(self).run_running_plan(runing_plan_no, debug)
            if result[0]:
                msg  = '在线运行成功'
                logger.info(msg)
                self.info(msg)
            else:
                msg = '在线运行失败：%s' % result[1]
                logger.error(msg)
                self.error(msg)
        except Exception as e:
            logger.error('在线运行失败：%s' % e)
            self.error('在线运行失败：%s' % e)
        finally:
            self.thread = None
            self.send(text_data=json.dumps({'message': 'taskEnd'}))



