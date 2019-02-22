from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

import json
import re
import logging
from django.core.paginator import  Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Max
from django.db import transaction
from django.db.models import Q

from website.models import Page_tree
from website.models import Page_element
from website.models import Database_setting
from website.models import Function_setting
from website.models import Operation_for_object
from website.models import UI_test_case_step
from website.models import API_test_case_step
from website.models import Assertion_type_setting
from website.models import API_case_tree
from website.models import UI_case_tree
from website.models import API_project_setting
from website.models import UI_project_setting


logger = logging.getLogger('mylogger')


# 点击导航菜单【测试用例管理-UI测试用例管理】，请求页面
def ui_case_manager(request):
    template = loader.get_template('website/pages/UICaseManager.html')
    return HttpResponse(template.render({}, request))

# 点击导航菜单【测试用例管理-API测试用例管理】，请求页面
def api_case_manager(request):
    template = loader.get_template('website/pages/APICaseManager.html')
    return HttpResponse(template.render({}, request))

# 点击用例树节点，打开对应页面
def ui_case_tree_node_page(request):
    template = loader.get_template('website/pages/UICaseTreeNodePage.html')
    return HttpResponse(template.render({}, request))

def api_case_tree_node_page(request):
    template = loader.get_template('website/pages/APICaseTreeNodePage.html')
    return HttpResponse(template.render({}, request))

# # 点击用例树节点，打开对应页面的对应的列表数据
def get_ui_case_steps(request):
    grid_data = {"total": 0, "rows": []}
    rows = [] # 用于存储记录行

    params = request.GET
    tree_node_id = params['nodeID']
    # 获取总记录数
    ui_test_cases = UI_test_case_step.objects.filter(case_id=tree_node_id).order_by('-order').values()
    grid_data["total"] = len(ui_test_cases)

    page_num = request.GET.get('page') # 记录请求的是第几页数据
    rows_num = request.GET.get('rows') # 记录请求每页的记录数

    paginator = Paginator(ui_test_cases, rows_num) # 设置每页展示的数据

    try:
        page = paginator.page(page_num)
    except PageNotAnInteger as e: # 如果请求的页面编号不存在，返回第一页数据
        logger.warn('%s' % e)
        page = paginator.page(1)
    except EmptyPage as e: # 如果请求页面，超出页面范围，返回最后一页数据
        logger.warn('%s' % e)
        page = paginator.page(paginator.num_pages)

    ui_test_cases = page.object_list
    for ui_test_case in ui_test_cases:
        rows.append(ui_test_case)
    grid_data["rows"] =  rows
    grid_data = json.dumps(grid_data)
    return HttpResponse(grid_data)


# # 点击用例树节点，打开对应页面的对应的列表数据
def get_api_case_steps(request):
    grid_data = {"total": 0, "rows": []}
    rows = [] # 用于存储记录行

    params = request.GET
    tree_node_id = params['nodeID']
    # 获取总记录数
    test_cases = API_test_case_step.objects.filter(case_id=tree_node_id).order_by('-order').values()
    grid_data["total"] = len(test_cases)

    page_num = request.GET.get('page') # 记录请求的是第几页数据
    rows_num = request.GET.get('rows') # 记录请求每页的记录数

    paginator = Paginator(test_cases, rows_num) # 设置每页展示的数据

    try:
        page = paginator.page(page_num)
    except PageNotAnInteger as e: # 如果请求的页面编号不存在，返回第一页数据
        logger.warn('%s' % e)
        page = paginator.page(1)
    except EmptyPage as e: # 如果请求页面，超出页面范围，返回最后一页数据
        logger.warn('%s' % e)
        page = paginator.page(paginator.num_pages)

    test_cases = page.object_list
    for test_case in test_cases:
        test_case['input_params'] =  '<xmp>' + test_case['input_params'] + '</xmp>'
        test_case['check_pattern'] =  '<xmp>' + test_case['check_pattern'] + '</xmp>'
        rows.append(test_case)
    grid_data["rows"] =  rows
    grid_data = json.dumps(grid_data)
    return HttpResponse(grid_data)

# 用例步骤中选择“对象类型”为页面元素时，请求获取元素页面
def get_pages_for_page_elements(request):
    temp_var = ''
    try:
        params = request.GET
        project_id = params['projectID']

        def find_page_fullpath(page):
            nonlocal  temp_var
            if  page.parent_id !=0: # 存在上级页面
                father_page = Page_tree.objects.get(id = page.parent_id)
                temp_var = find_page_fullpath(father_page) + '->' + father_page.text
                return temp_var
            else:
                return temp_var

        page_list = []
        pages = Page_tree.objects.filter(project_id=project_id).all()
        for page in pages:
            temp_dic = {}
            temp_dic['id'] = str(page.id) # 改成字符串前端才可以正确展示
            temp_dic['choice'] = (find_page_fullpath(page) + '->' + page.text).lstrip('->')
            temp_var =  ''
            page_list.append(temp_dic)

        response = {'result':'success', 'choices':page_list}
        response = json.dumps(response)
        return HttpResponse(response)
    except Exception as e:
        logger.error('%s' % e)
        response = {'result':'error', 'choices':'%s' % e}
        response = json.dumps(response)
        return HttpResponse(response)


# 用例步骤中选择“对象类型”为用例时时，请求获取用例所在的页面
def get_pages_for_cases(request):
    temp_var = ''
    try:
        params = request.GET
        project_id = params['projectID']

        def find_page_fullpath(page):
            nonlocal  temp_var
            if  page.parent_id !=0: # 存在上级页面
                father_page = UI_case_tree.objects.get(id = page.parent_id)
                temp_var = find_page_fullpath(father_page) + '->' + father_page.text
                return temp_var
            else:
                return temp_var

        page_list = []
        pages = UI_case_tree.objects.filter(project_id=project_id).filter(id__in=UI_case_tree.objects.all().values_list('parent_id', flat=True))
        for page in pages:
            temp_dic = {}
            temp_dic['id'] = str(page.id) # 改成字符串前端才可以正确展示
            temp_dic['choice'] = (find_page_fullpath(page) + '->' + page.text).lstrip('->')
            temp_var =  ''
            page_list.append(temp_dic)

        response = {'result':'success', 'choices':page_list}
        response = json.dumps(response)
        return HttpResponse(response)
    except Exception as e:
        logger.error('%s' % e)
        response = {'result':'error', 'choices':'%s' % e}
        response = json.dumps(response)
        return HttpResponse(response)

# 用例步骤中选择“对象类型”为页面元素时，请求获取该页面拥有的页面元素名称
def get_elements_for_page_selected(request):
    params = request.GET
    page_id = params['pageID']

    element_list = []
    try:
        elements = Page_element.objects.filter(page_id=page_id).values()
        for element in elements:
            temp_dic = {}
            temp_dic['id'] = str(element['id'])
            temp_dic['choice'] = element['element_name']
            element_list.append(temp_dic)
        response = {'result':'success', 'choices':element_list}
        response = json.dumps(response)
        return HttpResponse(response)
    except Exception as e:
        logger.error('%s' % e)
        response = {'result':'error', 'choices':'%s' % e}
        response = json.dumps(response)
        return HttpResponse(response)


# 用例步骤中选择“对象类型”为用例时时，请求获取该页面所有的用例
def get_cases_for_page_selected(request):
    try:
        params = request.GET
        project_id = params['projectID']
        project_type = params['projectType']
        page_id = params['pageID']
        current_case_id = params['caseID'] # 正在编辑的步骤归属的用例ID
        if project_type == 'API':
            db_class = API_case_tree
        elif project_type == 'UI':
            db_class = UI_case_tree

        # temp_var = ''
        # def find_case_fullpath(case):
        #     nonlocal  temp_var
        #     if  case.parent_id !=0: # 存在上级页面
        #         father_node = db_class.objects.get(id = case.parent_id)
        #         temp_var = find_case_fullpath(father_node) + '->' + father_node.text
        #         return temp_var
        #     else:
        #         return temp_var


        case_list = []
        cases = db_class.objects.filter(project_id=project_id).filter(parent_id=page_id).exclude(id=current_case_id).all()

        for case in cases:
            case_id = case.id
            if db_class.objects.filter(parent_id=case_id).exists():# 非用例，为模块名称
                continue
            else:
                temp_dic = {}
                temp_dic['id'] = str(case_id)
                # temp_dic['choice'] = (find_case_fullpath(case) + '->' + case.text).lstrip('->')
                temp_dic['choice'] = case.text
                # temp_var = ''
                case_list.append(temp_dic)
        response = {'result':'success', 'choices':case_list}
        response = json.dumps(response)
        return HttpResponse(response)
    except Exception as e:
        logger.error('%s' % e)
        response = {'result':'error', 'choices':'%s' % e}
        response = json.dumps(response)
        return HttpResponse(response)


# 用例步骤中选择“对象类型”为数据库时、“步骤类型”选择 执行数据库，请求获取数据库名称
def get_dbs_for_db_obj_type(request):
    db_list = []
    try:
        params = request.GET
        project_id = params['projectID']
        project_type = params['projectType']
        if project_type == 'APIProject':
            project_info = API_project_setting.objects.filter(id=project_id).values()
            project_type = 'API项目'
        elif project_type == 'UIProject':
            project_info = UI_project_setting.objects.filter(id=project_id).values()
            project_type = 'UI项目'
        project_env = project_info[0]['environment']
        dbs = Database_setting.objects.filter(project_type=project_type).filter(project_id=project_id).filter(environment=project_env).values()
        for db in dbs:
            temp_dic = {}
            temp_dic['id'] = str(db['id'])
            temp_dic['choice'] = db['db_alias']
            db_list.append(temp_dic)
        response = {'result':'success', 'choices':db_list}
        response = json.dumps(response)
        return HttpResponse(response)
    except Exception as e:
        logger.error('%s' % e)
        response = {'result':'error', 'choices':'%s' % e}
        response = json.dumps(response)
        return HttpResponse(response)

# 用例步骤中选择“对象类型”为系统函数时，请求获取可执行函数
def get_funtions_for_func_type(request):
    function_list = []
    try:
        project_type = request.GET.get('projectType') # 页面操作|接口请求操作|数据库操作|系统函数调用
        project_type = project_type.split('|')

        if len(project_type) > 1:
            project_type1,project_type2 = project_type
            functions = Function_setting.objects.filter(Q(project_type=project_type1) | Q(project_type=project_type2)).values()
        else:
            project_type1 = project_type[0]
            functions = Function_setting.objects.filter(project_type=project_type1).values()
        # functions = Function_setting.objects.all().values()
        for function in functions:
            temp_dic = {}
            temp_dic['id'] = str(function['id'])
            temp_dic['choice'] = function['function_name']
            temp_dic['param_style'] = function['param_style']
            function_list.append(temp_dic)
        response = {'result':'success', 'choices':function_list}
        response = json.dumps(response)
        return HttpResponse(response)
    except Exception as e:
        logger.error('%s' % e)
        response = {'result':'error', 'choices':'%s' % e}
        response = json.dumps(response)
        return HttpResponse(response)

# 用例步骤中选择不同的“对象类型”时，请求对象可被执行的操作
def get_operations_for_object_type(request):
    object_type = request.GET.get('objectType') # 获取对象类型 页面元素 | 数据库 | 系统函数
    opertion_list = []
    try:
        operations = Operation_for_object.objects.filter(object_type=object_type).values()
        for operation in operations:
            temp_dic = {}
            temp_dic['id'] = str(operation['id'])
            temp_dic['choice'] = operation['operation']
            opertion_list.append(temp_dic)
        response = {'result':'success', 'choices':opertion_list}
        response = json.dumps(response)
        return HttpResponse(response)
    except Exception as e:
        logger.error('%s' % e)
        response = {'result':'error', 'choices':'%s' % e}
        response = json.dumps(response)
        return HttpResponse(response)

# 用例步骤，步骤类型选择 执行用例 时，请求对应项目的测试用例
def get_cases_for_project(request):
    try:
        params = request.GET
        project_id = params['projectID']
        case_id = params['caseID']
        project_type = params['projectType']
        if project_type == 'API':
            db_class = API_case_tree
        elif project_type == 'UI':
            db_class = UI_case_tree

        temp_var = ''
        def find_case_fullpath(case):
            nonlocal  temp_var
            if  case.parent_id !=0: # 存在上级页面
                father_node = db_class.objects.get(id = case.parent_id)
                temp_var = find_case_fullpath(father_node) + '->' + father_node.text
                return temp_var
            else:
                return temp_var


        case_list = []
        cases = db_class.objects.filter(project_id=project_id).exclude(parent_id=0).exclude(id=case_id).all()

        for case in cases:
            case_id = case.id
            if db_class.objects.filter(parent_id=case_id).exists():# 非用例，为模块名称
                continue
            else:
                temp_dic = {}
                temp_dic['id'] = str(case_id)
                temp_dic['choice'] = (find_case_fullpath(case) + '->' + case.text).lstrip('->')
                temp_var = ''
                case_list.append(temp_dic)
        response = {'result':'success', 'choices':case_list}
        response = json.dumps(response)
        return HttpResponse(response)
    except Exception as e:
        logger.error('%s' % e)
        response = {'result':'error', 'choices':'%s' % e}
        response = json.dumps(response)
        return HttpResponse(response)


# 用例步骤中选择不同的“对象类型”、“步骤类型”时，请求可用断言类型
def get_assertions_for_op_type(request):
    try:
        op_type = request.GET.get('opType') # 页面操作|接口请求操作|数据库操作|系统函数调用
        op_type = op_type.split('|')
        if len(op_type) > 1:
            op_type1,op_type2 = op_type
            assertions = Assertion_type_setting.objects.filter(Q(op_type=op_type1) | Q(op_type=op_type2)).values()
        else:
            op_type = op_type[0]
            assertions = Assertion_type_setting.objects.filter(op_type=op_type).values()
        opertion_list = []

        for assertion in assertions:
            temp_dic = {}
            temp_dic['id'] = str(assertion['id'])
            temp_dic['choice'] = assertion['assertion_type']
            temp_dic['assert_pattern'] = assertion['assertion_pattern']
            opertion_list.append(temp_dic)
        response = {'result':'success', 'choices':opertion_list}
        response = json.dumps(response)
        return HttpResponse(response)
    except Exception as e:
        logger.error('%s' % e)
        response = {'result':'error', 'choices':'%s' % e}
        response = json.dumps(response)
        return HttpResponse(response)

# 增加用例步骤
def add_ui_case_step(request):
    try:
        params = request.POST

        step_order = params['order']
        status = params['status']
        object_type = params['object_type']
        object = params['object']
        exec_operation = params['exec_operation']
        input_params = params['input_params']
        output_params = params['output_params']
        assert_type = params['assert_type']
        assert_pattern = params['assert_pattern']
        run_times = params['run_times'].strip()
        try_for_failure = params['try_for_failure'].strip()
        page_name = params['page_name']
        case_id = params['node_id']
        object_id =  params['object_id']

        if object_type == '':
            return  HttpResponse('保存失败，对象类型不能为空')
        elif object_type == '数据库操作' and input_params == '':
            return  HttpResponse('保存失败，输入参数不能为空')
        if object == '':
            return  HttpResponse('保存失败，操作对象不能为空')
        if exec_operation == '' and object_type == '页面元素':
            return  HttpResponse('保存失败，执行操作不能为空')
        if not run_times.isdigit() and run_times !=  '':
            return HttpResponse('保存失败，重复执行次数只能为数字')
        if not try_for_failure.isdigit() and try_for_failure !=  '':
            return HttpResponse('保存失败，失败重试次数只能为数字')

        if page_name == '':
            page_name = '--'
        if run_times == '':
            run_times = 0
        if try_for_failure == '':
            try_for_failure = 0

        if step_order == '': # 如果无顺序，表明是新增
            all_objects = UI_test_case_step.objects.filter(case_id=case_id)
            if all_objects.exists():
                max_order = all_objects.aggregate(Max('order'))['order__max']
                step_order = max_order + 1
            else:
                step_order = 1
            ui_case_step_obj = UI_test_case_step(order=step_order,status=status, object_type= object_type,object=object, exec_operation=exec_operation,
                                            input_params=input_params, output_params=output_params, assert_type=assert_type, assert_pattern=assert_pattern,
                                            run_times=run_times,try_for_failure=try_for_failure,page_name=page_name,case_id=case_id, object_id=object_id)

            ui_case_step_obj.save()
        else: #表明是插入
            # logger.info('即将插入新记录，正在调整记录的顺序') # 插入记录所在行下方的记录都减去1
            try:
                with transaction.atomic():
                    all_objects = UI_test_case_step.objects.filter(case_id=case_id).filter(order__gte=step_order)
                    for item in all_objects:
                        item.order = item.order + 1
                        item.save()

                    ui_case_step_obj = UI_test_case_step(order=step_order, status=status,object_type= object_type,object=object, exec_operation=exec_operation,
                                            input_params=input_params, output_params=output_params, assert_type=assert_type, assert_pattern=assert_pattern,
                                            run_times=run_times,try_for_failure=try_for_failure,page_name=page_name,case_id=case_id, object_id=object_id)

                    ui_case_step_obj.save()
            except Exception as e:
                logger.error('%s' % e)
                return  HttpResponse('%s' % e)
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)


# 增加用例步骤
def add_api_case_step(request):
    try:
        params = request.POST
        step_order = params['order']
        status = params['status']
        step_type = params['step_type']
        op_object = params['op_object']
        object_id =  params['object_id']
        exec_operation = params['exec_operation']
        request_header = params['request_header'].strip()
        request_method = params['request_method']
        url_or_sql = params['url_or_sql'].strip()
        if not url_or_sql.startswith('/') and step_type not in ('操作数据库', '执行用例',  '执行函数'):
            url_or_sql = '/' + url_or_sql
        input_params = params['input_params'].strip().replace('\'', '\"')
        if input_params.startswith('<xmp>'):
            input_params = input_params[5:]
            logger.info(input_params)
        if input_params.endswith('</xmp>'):
            input_params = input_params[:-6]

        if step_type == '操作数据库':
            input_params = input_params.replace('\'', '\"')

        response_to_check = params['response_to_check']
        check_rule = params['check_rule']
        check_pattern = params['check_pattern'].strip()

        if check_pattern.startswith('<xmp>'):
            check_pattern = check_pattern[5:]
            logger.info(input_params)
        if check_pattern.endswith('</xmp>'):
            check_pattern = check_pattern[:-6]
        output_params = params['output_params'].strip()
        protocol = params['protocol'].strip().lower()
        if protocol != '' and protocol not in ('https', 'http'):
            return HttpResponse('协议只能为http、https')

        host = params['host'].strip()
        port = params['port'].strip()
        run_times = params['run_times'].strip()
        try_for_failure = params['try_for_failure'].strip()
        case_id = params['case_id']

        if step_type == '':
            return  HttpResponse('保存失败，对象类型不能为空')
        if op_object == '':
            return HttpResponse('保存失败，操作对象不能为空')
        elif step_type in('请求接口', '操作数据库操作') and url_or_sql == '':
            return  HttpResponse('保存失败，URL/SQL不能为空')
        if exec_operation == '':
            return  HttpResponse('保存失败，执行操作不能为空')
        if port !=  '' and not port.isdigit():
            return HttpResponse('保存失败，端口号只能为数字')
        if not run_times.isdigit() and run_times !=  '':
            return HttpResponse('保存失败，运行次数只能为数字')
        if not try_for_failure.isdigit() and try_for_failure !=  '':
            return HttpResponse('保存失败，失败重试次数只能为数字')


        if run_times == '':
            run_times = '1'

        if try_for_failure == '':
            try_for_failure = '1'


        # 检查输出中的定义变了变量命名是否合法
        variable_list = re.findall('\$(.+?)\$', output_params)
        for variable in variable_list:
            variable = variable.strip().lower()
            if re.findall('[\s|-]', variable):
                return HttpResponse('变量名不能包含字符"tab、空格、- 等字符')
            if  re.findall('^global_', variable.lower()) or re.findall('global', variable.lower()):
                return HttpResponse('变量名不能以global_、global开头')

        if step_order == '': # 如果无顺序，表明是新增
            all_objects = API_test_case_step.objects.filter(case_id=case_id)
            if all_objects.exists():
                max_order = all_objects.aggregate(Max('order'))['order__max']
                step_order = max_order + 1
            else:
                step_order = 1
            case_step_obj = API_test_case_step(order=step_order, status=status,step_type=step_type,op_object=op_object, object_id=object_id,exec_operation=exec_operation,
                                    request_header=request_header, request_method=request_method, url_or_sql=url_or_sql, input_params=input_params,
                                    response_to_check=response_to_check,check_rule=check_rule,check_pattern=check_pattern, output_params=output_params,
                                    protocol=protocol, host=host, port=port, run_times=run_times, try_for_failure=try_for_failure, case_id=case_id)

            case_step_obj.save()
        else: #表明是插入
            # logger.info('即将插入新记录，正在调整记录的顺序') # 插入记录所在行下方的记录都减去1
            try:
                with transaction.atomic():
                    all_objects = API_test_case_step.objects.filter(case_id=case_id).filter(order__gte=step_order)
                    for item in all_objects:
                        item.order = item.order + 1
                        item.save()

                    case_step_obj = API_test_case_step(order=step_order, status=status,step_type=step_type,op_object=op_object, object_id=object_id,exec_operation=exec_operation,
                                            request_header=request_header, request_method=request_method, url_or_sql=url_or_sql, input_params=input_params,
                                            response_to_check=response_to_check,check_rule=check_rule,check_pattern=check_pattern, output_params=output_params,
                                            protocol=protocol, host=host, port=port, run_times=run_times, try_for_failure=try_for_failure, case_id=case_id)

                    case_step_obj.save()
            except Exception as e:
                logger.error('%s' % e)
                return HttpResponse('%s' % e)
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)

# 修改任务步骤
def update_ui_case_step(request):
    try:
        params = request.POST

        id = params['id']
        object_type = params['object_type']
        object = params['object']
        exec_operation = params['exec_operation']
        input_params = params['input_params']
        output_params = params['output_params']
        assert_type = params['assert_type']
        assert_pattern = params['assert_pattern']
        run_times = params['run_times'].strip()
        try_for_failure = params['try_for_failure'].strip()
        page_name = params['page_name']
        object_id = params['object_id']

        if object_type == '':
            return  HttpResponse('保存失败，对象类型不能为空')
        elif object_type == '数据库' and input_params == '':
            return  HttpResponse('保存失败，输入参数不能为空')
        if object == '':
            return  HttpResponse('保存失败，操作对象不能为空')
        if exec_operation == '' and object_type == '页面元素':
            return  HttpResponse('保存失败，执行操作不能为空')
        if not run_times.isdigit() and run_times !=  '':
            return HttpResponse('保存失败，运行次数只能为数字')
        if not try_for_failure.isdigit() and try_for_failure !=  '':
            return HttpResponse('保存失败，失败重试次数只能为数字')

        if run_times == '':
            run_times = '1'

        if try_for_failure == '':
            try_for_failure = '0'

        ui_case_step_obj = UI_test_case_step.objects.get(id=id)
        ui_case_step_obj.object_type = object_type
        ui_case_step_obj.object = object
        ui_case_step_obj.exec_operation = exec_operation
        ui_case_step_obj.input_params = input_params
        ui_case_step_obj.output_params = output_params
        ui_case_step_obj.assert_type = assert_type
        ui_case_step_obj.assert_pattern = assert_pattern
        ui_case_step_obj.run_times = run_times
        ui_case_step_obj.try_for_failure = try_for_failure
        ui_case_step_obj.page_name = page_name

        if object_id != '-1':
            ui_case_step_obj.object_id = object_id
        ui_case_step_obj.save()
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)


# 修改任务步骤
def update_api_case_step(request):
    try:
        params = request.POST

        id = params['id']
        step_type = params['step_type']
        op_object = params['op_object']
        object_id =  params['object_id']
        exec_operation = params['exec_operation']
        request_header = params['request_header'].strip()
        request_method = params['request_method']
        url_or_sql = params['url_or_sql'].strip().replace('\'', '\"')
        if not url_or_sql.startswith('/') and step_type not in ('操作数据库', '执行用例', '执行函数'):
            url_or_sql = '/' + url_or_sql
        input_params = params['input_params'].strip().replace('\'', '\"')
        if input_params.startswith('<xmp>'):
            input_params = input_params[5:]
            logger.info(input_params)
        if input_params.endswith('</xmp>'):
            input_params = input_params[:-6]
        response_to_check = params['response_to_check']
        check_rule = params['check_rule']
        check_pattern = params['check_pattern'].strip()

        if check_pattern.startswith('<xmp>'):
            check_pattern = check_pattern[5:]
            logger.info(input_params)
        if check_pattern.endswith('</xmp>'):
            check_pattern = check_pattern[:-6]

        if step_type == '操作数据库':
            input_params = input_params.replace('\'', '\"')

        output_params = params['output_params'].strip()
        protocol = params['protocol'].strip().lower()
        if protocol != '' and protocol not in ('https', 'http'):
            return HttpResponse('协议只能为http、https')
        host = params['host'].strip()
        port = params['port'].strip()
        run_times = params['run_times'].strip()
        try_for_failure = params['try_for_failure'].strip()

        if step_type == '':
            return  HttpResponse('保存失败，对象类型不能为空')
        if op_object == '':
            return HttpResponse('保存失败，操作对象不能为空')
        elif step_type in('请求接口', '操作数据库操作') and url_or_sql == '':
            return  HttpResponse('保存失败，URL/SQL不能为空')
        if exec_operation == '':
            return  HttpResponse('保存失败，执行操作不能为空')
        if port !=  '' and not port.isdigit():
            return HttpResponse('保存失败，端口号只能为数字')
        if not run_times.isdigit() and run_times !=  '':
            return HttpResponse('保存失败，运行次数只能为数字')
        if not try_for_failure.isdigit() and try_for_failure !=  '':
            return HttpResponse('保存失败，失败重试次数只能为数字')

        if run_times == '':
            run_times = '1'

        if try_for_failure == '':
            try_for_failure = '0'

        # 检查输出中的定义变了变量命名是否合法
        variable_list = re.findall('\$(.+?)\$', output_params)
        for variable in variable_list:
            variable = variable.strip().lower()
            if re.findall('[\s|-]', variable):
                return HttpResponse('变量名不能包含字符"tab、空格、- 等字符')
            if  re.findall('^global_', variable.lower()) or re.findall('global', variable.lower()):
                return HttpResponse('变量名不能以global_、global开头')

        case_step_obj = API_test_case_step.objects.get(id=id)
        case_step_obj.step_type = step_type
        case_step_obj.op_object = op_object
        case_step_obj.exec_operation = exec_operation
        case_step_obj.request_header = request_header
        case_step_obj.request_method = request_method
        case_step_obj.url_or_sql = url_or_sql
        case_step_obj.input_params = input_params
        case_step_obj.response_to_check = response_to_check
        case_step_obj.check_rule = check_rule
        case_step_obj.check_pattern = check_pattern
        case_step_obj.output_params = output_params
        case_step_obj.protocol = protocol
        case_step_obj.host = host
        case_step_obj.port = port
        case_step_obj.run_times = run_times
        case_step_obj.try_for_failure = try_for_failure

        if object_id != '-1':
            case_step_obj.object_id = object_id
        case_step_obj.save()
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)


# 删除用例步骤
def remove_case_step(request):
    try:
        params = request.POST

        row_ids = eval(params['rowIDs'])
        class_name = params['datagridID']

        order_list = []  # 存放被删除记录的顺序
        db_class = globals()[class_name]

        try:
            with transaction.atomic():
                for row_id in row_ids:
                    row_id = int(row_id)
                    record = db_class.objects.filter(id=row_id)
                    if not record.exists():
                        logger.error('error, ID(%s)不存在' % row_id)
                        continue
                    else:
                        temp_record = record.values()[0]
                        # logger.info(temp_record)
                        case_id = temp_record['case_id']
                        order_list.append(temp_record['order'])
                        record.delete()

                # logger.info('删除操作完成，正在重新调整顺序')
                order_list.sort()
                if order_list:
                    min_order_for_deleted = order_list[0]
                    all_objects = db_class.objects.filter(case_id=case_id).filter(order__gt=min_order_for_deleted).order_by('order')
                    for object in all_objects:
                        object.order = min_order_for_deleted
                        object.save()
                        min_order_for_deleted = min_order_for_deleted + 1
            return HttpResponse('success')
        except Exception as e:
            logger.error('%s' % e)
            return HttpResponse('%s' % e)
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)

# 启用、禁用测试用例步骤
def enable_or_disable_case_tep(request):
    try:
        params = request.POST

        row_ids = eval(params['rowIDs'])
        class_name = params['datagridID']
        op_type = params['opType']

        db_class = globals()[class_name]

        try:
            with transaction.atomic():
                if op_type == '禁用':
                    for row_id in row_ids:
                        row_id = int(row_id)
                        record = db_class.objects.get(id=row_id)
                        record.status = '禁用'
                        record.save()
                elif op_type == '启用':
                    for row_id in row_ids:
                        row_id = int(row_id)
                        record = db_class.objects.get(id=row_id)
                        record.status = '启用'
                        record.save()
            return HttpResponse('success')
        except Exception as e:
            logger.error('%s' % e)
            return HttpResponse('%s' % e)
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)