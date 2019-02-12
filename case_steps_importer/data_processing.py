#!/usr/bin/env python
#-*- coding:utf-8 -*-

__author__ = 'laifuyu'

import xlrd
import xlwt
import os
import json
import time

class DataProcessing:
    def __init__(self):

        pass

    # 数据填写规则校验(校验用例步骤填写是否符合规则）
    def varify_data(self, file_name, op_opject_list, case_id_list, file_handler):
        # 打开excel
        excel = xlrd.open_workbook(file_name)

        # 新建excel,存放解析结果
        work_book = xlwt.Workbook()

        # 查看文件中包含的sheet名称
        sheet_names = excel.sheet_names()

        exists_error = False # 用于标记步骤填写值是否存在错误
        # 循环遍历每个sheet表
        for sheet_name in sheet_names:
            print('校验sheet名称：%s' % sheet_name)
            file_handler.write('校验sheet名称：%s' % sheet_name)
            sheet_dest = work_book.add_sheet(sheet_name, cell_overwrite_ok=True)# 添加表单，允许覆盖单元格
            # 通过名称，获取指定sheet表
            sheet_src = excel.sheet_by_name(sheet_name)

            # 获取源sheet行数
            row_cnt = sheet_src.nrows

            # 往结果表插入表头
            if row_cnt > 0:
                row_values = sheet_src.row_values(0)
                del row_values[18:] # 防止用户多输入一列
                col_index = 0
                for value in row_values:
                    sheet_dest.write(0, col_index, value)
                    col_index = col_index + 1
                sheet_dest.write(0, col_index, '备注')


            # 针对每一行记录进行校验(第一行除外)
            for row_index in range(1, row_cnt):
                row_values = sheet_src.row_values(row_index)
                del row_values[18:] # 防止用户多输入一列
                col_index = 0
                remark = ''
                for value in row_values:
                    sheet_dest.write(row_index, col_index, value)
                    col_index = col_index + 1

                step_type = row_values[1]

                if step_type.strip() == '':
                    continue

                # 校验对象ID是否填写正确
                temp_object_id = row_values[3]
                if type(temp_object_id) == type(0.1):
                    object_id = str(int(temp_object_id))
                else:
                    object_id = str(temp_object_id)

                if step_type == '执行用例':
                    if not object_id.strip().isdigit():
                        remark = remark + '&对象ID不为数字'
                    elif object_id.strip().isdigit():
                        if int(object_id) not in case_id_list:
                            remark = remark + '&对象ID不存在'

                exec_opration  = row_values[4]
                check_rule = row_values[10]
                op_object = row_values[2]
                response_to_check = row_values[9]
                if step_type == '请求接口':
                    # 校验操作对象是否填写正确
                    step_type = row_values[1]
                    if op_object != 'APIUnittestTestCase':
                        remark = remark + '&操作对象必须为APIUnittestTestCase'

                    # 校验执行操作是否填写正确
                    if exec_opration not in ['test_api_for_json','test_api_for_urlencode','test_api_for_xml']:
                        remark = remark + '&不支持的执行操作'

                    # 校验请求头是否填写正确
                    request_header = row_values[5]
                    if request_header.strip() != '':
                        try:
                            json.loads(request_header.strip())
                        except Exception as e:
                            remark = remark + '&请求头填写错误,必须为json格式'

                    request_method = row_values[6]
                    if request_method not in ['POST', 'GET']:
                        remark = remark + '&请求方法为POST,GET'


                    # 校验输入参数是否填写正确
                    input_params = row_values[8]
                    if exec_opration != 'test_api_for_xml' and input_params != '':
                        try:
                            json.loads(input_params.strip())
                        except Exception as e:
                            remark = remark + '&输入参数写错误,必须为json格式'


                    if response_to_check not in ['body', 'header', 'code']:
                        remark = remark + '&检查响应必须为body, header, code'

                    # 校验校验规则是否填写正确
                    if check_rule  in ['db列值相等','db列值不相等']:
                        remark = remark + '&不支持的校验规则'

                elif step_type == '操作数据库':
                    if op_object not in op_opject_list[:]:
                        remark = remark + '&不支持的操作对象'
                    elif op_object == 'APIUnittestTestCase':
                        remark = remark +  '&不支持的操作对象'

                    if exec_opration in ['test_api_for_json','test_api_for_urlencode','test_api_for_xml']:
                        remark = remark +  '&不支持的执行操作'

                    if check_rule.strip() !=  '' and check_rule.strip() not in ['db列值相等','db列值不相等']:
                        remark = remark +  '&不支持的校验规则'

                    if response_to_check != 'body':
                        remark = remark + '&检查响应必须为body'

                if step_type != '执行用例':
                    url_or_sql = row_values[7]
                    if url_or_sql.strip() == '':
                        remark = remark + '&url/sql不能为空'

                    check_pattern = row_values[11]
                    if check_pattern.strip() != '':
                        try:
                            json.loads(check_pattern.strip())
                        except Exception as e:
                            remark = remark + '&校验模式填写错误，必须为json格式'

                    output_params = row_values[12]
                    if output_params.strip() != '':
                        try:
                            json.loads(output_params.strip())
                        except Exception as e:
                            remark = remark + '&输出参数填写错误，必须为json格式'

                # 校验用例ID是否填写正确
                temp_case_id = row_values[16]
                if type(temp_case_id) == type(0.1):
                    case_id = str(int(temp_case_id))
                else:
                    case_id = str(temp_case_id)

                if not case_id.isdigit():
                    remark = remark + '&用例ID %s不为数字' % case_id
                elif int(case_id) not in case_id_list:
                    remark = remark + '&用例ID %s不存在' % case_id

                remark = remark.lstrip('&')
                if remark:
                    exists_error = True
                    print('填写出错：%s' % remark)
                    print('错误所在行：第 %s 行\n' % (row_index + 1))
                    file_handler.write('校验失败：%s\n' % remark)
                    file_handler.write('错误所在行：第 %s 行\n' % (row_index + 1))
                    file_handler.flush()
                    sheet_dest.write(row_index, col_index, remark)
            file_handler.write('\n\n')
            print()

        work_book.save('./resultfile/数据校验-' + os.path.split(file_name)[1])
        return exists_error


    def import_data(self, file_name, db):
        temp_var = ''
        def find_case_fullpath(node_id):
            nonlocal  temp_var
            query = "SELECT parent_id, text FROM `website_api_case_tree` WHERE id = %s"
            data = (node_id, )
            result = db.select_one_record(query, data)

            if result[0] and result[1]:
                parent_id, text = result[1]
                temp_var = find_case_fullpath(parent_id) + '->' + text
                return temp_var
            elif result[0] and not result[1]:
                return temp_var
            else:
                print('查询出错，退出程序')
                exit()

        # 打开excel
        excel = xlrd.open_workbook(file_name)

        # 新建excel,存放解析结果
        work_book = xlwt.Workbook()

        # 查看文件中包含的sheet名称
        sheet_names = excel.sheet_names()

        file_handler = open('./resultfile/import_error_record.txt', 'w', encoding='utf-8')
        exists_error = False # 用于标记步骤填写值是否存在错误


        file_handler.write('导入文件： %s\n' %  file_name)

        # 循环遍历每个sheet表
        for sheet_name in sheet_names:
            run_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 记录执行时间
            file_handler.write('导入时间：%s\n' % run_time)
            file_handler.write('导入sheet： %s' % sheet_name)

            sheet_dest = work_book.add_sheet(sheet_name, cell_overwrite_ok=True)# 添加表单，允许覆盖单元格
            # 通过名称，获取指定sheet表
            sheet_src = excel.sheet_by_name(sheet_name)

            # 获取源sheet行数
            row_cnt = sheet_src.nrows

            # 往结果表插入表头
            if row_cnt > 0:
                row_values = sheet_src.row_values(0)
                col_index = 0
                for value in row_values:
                    sheet_dest.write(0, col_index, value)
                    col_index = col_index + 1
                sheet_dest.write(0, col_index, '备注')

            # 针对每一行记录进行导入
            temp_case_id = 0
            step_order = 0
            for row_index in range(1, row_cnt):
                row_values = sheet_src.row_values(row_index)
                del row_values[18:] # 防止用户多输入一列
                col_index = 0

                for value in row_values:
                    sheet_dest.write(row_index, col_index, value)
                    col_index = col_index + 1

                if row_values[17:18][0] == '是': # 已经导入过了
                    sheet_dest.write(row_index, col_index - 1, '否')
                    sheet_dest.write(row_index, col_index, '已经导入过')
                    continue
                elif row_values[1].strip() == '':
                    continue
                else:#未导入
                    if row_values[1] == '执行用例':
                        print('正在查找操作对象(用例路径)')
                        query = "SELECT parent_id, text FROM `website_api_case_tree` WHERE id = %s"
                        case_id = int(row_values[3])
                        data = (case_id,)
                        result = db.select_one_record(query, data)

                        if result[0] and result[1]:
                            parent_id, text = result[1]
                            row_values[2] = (find_case_fullpath(parent_id) + '->' + text).lstrip('->')
                        elif result[0] and not result[1]:
                            print('用例ID %s 不存在' % case_id)
                            sheet_dest.write(row_index, col_index - 1, '否')
                            sheet_dest.write(row_index, col_index, '用例ID: %s 不存在' % case_id)

                            file_handler.write('导入结果：第%s行 导入失败\n' % (row_index + 1))
                            file_handler.write('失败原因：用例ID: %s 不存在' % case_id)
                            file_handler.write('\n\n')
                            continue
                        else:
                            print('查询用例[ID:%s]信息出错，退出程序' % case_id)
                            sheet_dest.write(row_index, col_index - 1, '否')
                            sheet_dest.write(row_index, col_index, '查询用例[ID:%s]信息出错，退出程序' % case_id)

                            file_handler.write('导入结果：第%s行 导入失败\n' % row_index + 1)
                            file_handler.write('失败原因：查询用例[ID:%s]信息出错，退出程序' % case_id)
                            work_book.save('./resultfile/数据导入-' + os.path.split(file_name)[1])
                            exit()
                    temp_var = ''

                case_id = int(row_values[16])

                #获取最大顺序
                print('正在获取用例步骤最大顺序值')
                if temp_case_id != case_id:
                    query = "SELECT MAX(`order`) FROM `website_api_test_case_step` WHERE case_id = %s"
                    data = (case_id,)
                    result = db.select_one_record(query, data)
                    if result[0] and result[1][0]:
                        step_order = result[1][0] + 1
                    elif result[0] and not result[1][0]:
                        step_order = 1
                    else:
                        print('查询用例[ID:%s]步骤顺序信息出错，退出程序' % case_id)
                        sheet_dest.write(row_index, col_index - 1, '否')
                        sheet_dest.write(row_index, col_index, '查询用例[ID:%s]步骤顺序信息出错，退出程序' % case_id)

                        file_handler.write('导入结果：第%s行 导入失败\n' % row_index + 1)
                        file_handler.write('失败原因：查询用例[ID:%s]步骤顺序信息出错，退出程序\n\n' % case_id)
                        work_book.save('./resultfile/数据导入-' + os.path.split(file_name)[1])
                        exit()

                    temp_case_id = case_id

                del row_values[0] # 删除第一列 用例名称
                row_values.insert(0, step_order)
                step_type = row_values[1]
                if step_type == '执行用例':
                    row_values[4:16] = ['', '', '', '', '', '', '', '', '', '', '', '']
                elif step_type == '操作数据库':
                    row_values[3]='0' #object_id
                    row_values[5:7] = ['', ''] #request_header  request_method
                    row_values[9] = 'body' # response_to_check
                    row_values[13: 16] = ['', '', ''] #protocol	host	port
                elif step_type == '请求接口':
                    row_values[3] = '0'
                row_values[16] = int(row_values[16])

                del row_values[17:]
                row_values.append('启用')

                query = "INSERT INTO `website_api_test_case_step`(`order`, step_type, op_object, object_id, exec_operation, request_header, request_method, url_or_sql, " \
                        "input_params, response_to_check, check_rule, check_pattern, output_params, protocol, `host`, `port`, case_id, status) " \
                        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                result = db.execute_insert(query, row_values)
                if not result[0]:
                    sheet_dest.write(row_index, col_index - 1 , '否')
                    sheet_dest.write(row_index, col_index, '%s' % result[1])

                    file_handler.write('导入结果：第%s行 导入失败\n' % (row_index + 1))
                    file_handler.write('失败原因：%s' % result[1])
                else:
                    sheet_dest.write(row_index, col_index - 1, '是')

                step_order = step_order + 1

                file_handler.write('\n\n')

        work_book.save('./resultfile/数据导入-' + os.path.split(file_name)[1])
        return exists_error