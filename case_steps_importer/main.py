#!/usr/bin/env python
#-*- coding:utf-8 -*-

__author__ = 'laifuyu'

import time

from configparser import ConfigParser

from mydb import MyDB
from data_processing import DataProcessing
from tools import Tools



if __name__ == '__main__':
    test_platform_db = MyDB('TESTPLATFORM')
    tools = Tools()
    try:
        print('--------------正在读取project.conf配置-------------\n')
        config = ConfigParser()
        config.read('./conf/project.conf', encoding='utf-8-sig' )
        project_id = config['PROJECTINFO']['project_id'].strip()
        environment = config['PROJECTINFO']['environment'].strip()
        if project_id == '':
            print('项目ID不能为空')
            exit()
        if environment == '':
            print('项目环境不能为空')
            exit()
        elif environment not in ['测试环境', '预发布环境', '生产环境']:
            print('“项目环境”填写值非法，可选值：测试环境、 预发布环境、 生产环境')
            exit()

        print('\n--------------正在检测项目ID是否存在--------------')
        query = "SELECT * FROM `website_api_project_setting` WHERE id = %s AND environment=%s"
        data = (project_id, environment)
        result = test_platform_db.select_many_record(query, data)
        if result[0] and result[1]:
            pass
        elif result[0] and not result[1]:
            print('告警：项目ID不存在,提前退出程序')
            exit()
        else:
            print('查询出错，退出程序')
            exit()

        op_opject_list = ['APIUnittestTestCase']
        print('\n--------------正在读项目关联的取数据库别名--------------')
        query = "SELECT db_alias FROM `website_database_setting`WHERE project_id = %s AND project_type='API项目' AND environment=%s"
        data = (project_id, environment)
        result = test_platform_db.select_many_record(query, data)
        if result[0] and result[1]:
            for record  in result[1]:
                op_opject_list.append(record[0])
        elif result[0] and not result[1]:
            print('告警：未配置数据库')
        else:
            print('查询出错，退出程序')
            exit()

        print('获取的操作对象(数据库别名及类名)：%s\n' % op_opject_list)

        print('\n--------------正在读取项目关联的用例ID--------------')
        query = "SELECT t1.id FROM `website_api_case_tree` AS t1 WHERE t1.project_id = %s AND t1.parent_id != 0 AND t1.id NOT IN (SELECT t2.parent_id FROM website_api_case_tree AS t2)"
        data = (project_id, )
        result = test_platform_db.select_many_record(query, data)
        case_id_list = []
        if result[0] and result[1]:
            for record  in result[1]:
                case_id_list.append(record[0])
        elif result[0] and not result[1]:
            print('告警：没有查询到用例')
        else:
            print('查询出错，退出程序')
            exit()

        print('获取的用例ID有：%s\n' % case_id_list)

        print('\n--------------正在获取用例步骤excel文件--------------')
        data_file_list = tools.get_files_in_dirpath('./datafile')
        print('获取的文件列表有：', data_file_list)

        print('\n正在校验数据文件是否符合填写规范')
        data_processor = DataProcessing()

        data_file_with_error_list = [] # 存放数据填写不符规范，存在错误的文件
        file_handler = open('./resultfile/data-file-with-error.txt', 'w', encoding='utf-8')
        for data_file in data_file_list[:]:
            run_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            print('正在校验文件：%s' % data_file)
            file_handler.write('校验时间：%s\n' % run_time)
            file_handler.write("校验文件：%s\n" % data_file)
            result = data_processor.varify_data(data_file, op_opject_list, case_id_list, file_handler)
            if result:
                data_file_list.remove(data_file)
                data_file_with_error_list.append(data_file)

            file_handler.write('\n\n')
            print('\n\n')

        file_handler.close()

        print('校验不通过的文件有：%s' % data_file_with_error_list)
        print('校验通过的文件有：%s' % data_file_list)

        for data_file in data_file_list:
            print('正在导入测试用例步骤文件：%s' % data_file)
            result = data_processor.import_data(data_file, test_platform_db)

    except Exception as e:
        print('%s' % e)
    finally:
        test_platform_db.close()

