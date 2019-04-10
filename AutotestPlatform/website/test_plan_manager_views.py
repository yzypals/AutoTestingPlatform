from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

import json
import logging
from django.core.paginator import  Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Max
from django.db import transaction

from website.models import UI_test_plan
from website.models import API_test_plan
from website.models import Project_chosen
from website.models import Browser_setting
from website.models import UI_case_tree
from website.models import API_case_tree
from website.models import UI_case_tree_test_plan
from website.models import API_case_tree_test_plan


logger = logging.getLogger('mylogger')


# 测试计划管理-UI测试计划
def ui_test_plan_manager(request):
    template = loader.get_template('website/pages/UITestPlanManager.html')
    return HttpResponse(template.render({}, request))

# 测试计划管理-API测试计划
def api_test_plan_manager(request):
    template = loader.get_template('website/pages/APITestPlanManager.html')
    return HttpResponse(template.render({}, request))

# # UI测试计划列表数据
def get_ui_test_plans(request):
    grid_data = {"total": 0, "rows": []}
    rows = [] # 用于存储记录行

    try:
        # 获取当前项目ID
        project_id = request.GET['projectID']
        if project_id == 'undefined':
            record = Project_chosen.objects.filter(tree_type='PlanUICaseTree').values()
            if record:
                project_id = record[0]['project_id']
            else:
                response = {'result':'error', 'data':'请先选项项目'}
                response = json.dumps(response)
                return HttpResponse(response)

        # 获取总记录数
        records = UI_test_plan.objects.filter(project_id=project_id).order_by('-order').values()
        grid_data["total"] = len(records)

        page_num = request.GET.get('page') # 记录请求的是第几页数据
        rows_num = request.GET.get('rows') # 记录请求每页的记录数

        paginator = Paginator(records, rows_num) # 设置每页展示的数据

        try:
            page = paginator.page(page_num)
        except PageNotAnInteger as e: # 如果请求的页面编号不存在，返回第一页数据
            logger.warn('%s' % e)
            page = paginator.page(1)
        except EmptyPage as e: # 如果请求页面，超出页面范围，返回最后一页数据
            logger.warn('%s' % e)
            page = paginator.page(paginator.num_pages)

        records = page.object_list
        for record in records:
            rows.append(record)
        grid_data["rows"] =  rows
        grid_data = json.dumps(grid_data)
        return HttpResponse(grid_data)
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)


# # API测试计划列表数据
def get_api_test_plans(request):
    grid_data = {"total": 0, "rows": []}
    rows = [] # 用于存储记录行

    try:
        # 获取当前项目ID
        project_id = request.GET['projectID']
        if project_id == 'undefined':
            record = Project_chosen.objects.filter(tree_type='PlanAPICaseTree').values()
            if record:
                project_id = record[0]['project_id']
            else:
                response = {'result':'error', 'data':'请先选项项目'}
                response = json.dumps(response)
                return HttpResponse(response)

        # 获取总记录数
        records = API_test_plan.objects.filter(project_id=project_id).order_by('-order').values()
        grid_data["total"] = len(records)

        page_num = request.GET.get('page') # 记录请求的是第几页数据
        rows_num = request.GET.get('rows') # 记录请求每页的记录数

        paginator = Paginator(records, rows_num) # 设置每页展示的数据

        try:
            page = paginator.page(page_num)
        except PageNotAnInteger as e: # 如果请求的页面编号不存在，返回第一页数据
            logger.warn('%s' % e)
            page = paginator.page(1)
        except EmptyPage as e: # 如果请求页面，超出页面范围，返回最后一页数据
            logger.warn('%s' % e)
            page = paginator.page(paginator.num_pages)

        records = page.object_list
        for record in records:
            rows.append(record)
        grid_data["rows"] =  rows
        grid_data = json.dumps(grid_data)
        return HttpResponse(grid_data)
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)

# 点击 在线调试 打开页面
def debug_api_test_plan(request):
    template = loader.get_template('website/pages/debugAPITestPlanView.html')
    return HttpResponse(template.render({}, request))

# 新增|编辑ui测试计划，请求运行环境（浏览器）
def get_browsers_for_ui_test_plan(request):
    choice_list = []
    try:
        browsers = Browser_setting.objects.all().values()
        for browser in browsers:
            temp_dic = {}
            temp_dic['id'] = str(browser['id'])
            temp_dic['choice'] = browser['browser']
            choice_list.append(temp_dic)
        response = {'result':'success', 'choices':choice_list}
        response = json.dumps(response)
        return HttpResponse(response)
    except Exception as e:
        logger.error('%s' % e)
        response = {'result':'error', 'choices':'%s' % e}
        response = json.dumps(response)
        return HttpResponse(response)

# 增加UI测试计划
def add_ui_test_plan(request):
    try:
        params = request.POST
        # logger.info('新增UI测试计划，请求参数为：%s' % params)
        project_id =  params['project_id']
        project_name = params['project_name']
        plan_name = params['plan_name']
        plan_desc = params['plan_desc']
        browsers = params['browsers']
        browser_id = params['browser_id']
        valid_flag = params['valid_flag']
        order = params['order']

        if project_name == '':
            return  HttpResponse('保存失败，当前所选项目为空')
        if plan_name == '':
            return  HttpResponse('保存失败，计划名称不能为空')
        elif UI_test_plan.objects.filter(project_id=project_id).filter(plan_name=plan_name).exists():
            return  HttpResponse('保存失败，计划名称重复')
        if browsers == '':
            return  HttpResponse('保存失败，运行环境不能为空')
        if valid_flag == '':
            return  HttpResponse('保存失败，是否启用不能为空')

        if order == '': # 如果顺序为空，表明是新增
            all_objects = UI_test_plan.objects.all()
            if all_objects.exists():
                max_order = all_objects.aggregate(Max('order'))['order__max']
                order = max_order + 1
            else:
                order = 1
            obj = UI_test_plan(project_id=project_id, project_name=project_name, plan_name=plan_name, plan_desc=plan_desc,
                                    browsers=browsers, valid_flag=valid_flag, order=order)
            obj.save()
        else: #表明是插入
            # logger.info('插入了新记录，正在调整记录的顺序') # 插入记录所在行上方的记录都+1
            try:
                with transaction.atomic():
                    all_objects = UI_test_plan.objects.filter(order__gte=order)
                    for item in all_objects:
                        item.order = item.order + 1
                        item.save()

                    obj = UI_test_plan(project_id=project_id, project_name=project_name, plan_name=plan_name, plan_desc=plan_desc,
                                            browsers=browsers, browser_id=browser_id, valid_flag=valid_flag, order=order)
                    obj.save()
            except Exception as e:
                logger.error('%s' % e)
                return HttpResponse('%s' % e)
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)


# 增加API测试计划
def add_api_test_plan(request):
    try:
        params = request.POST

        project_id =  params['project_id']
        project_name = params['project_name']
        plan_name = params['plan_name']
        plan_desc = params['plan_desc']
        valid_flag = params['valid_flag']
        order = params['order']

        if project_name == '':
            return  HttpResponse('保存失败，当前所选项目为空')
        if plan_name == '':
            return  HttpResponse('保存失败，计划名称不能为空')
        elif API_test_plan.objects.filter(project_id=project_id).filter(plan_name=plan_name).exists():
            return  HttpResponse('保存失败，计划名称重复')
        if valid_flag == '':
            return  HttpResponse('保存失败，是否启用不能为空')

        if order == '': # 如果顺序为空，表明是新增
            all_objects = API_test_plan.objects.all()
            if all_objects.exists():
                max_order = all_objects.aggregate(Max('order'))['order__max']
                order = max_order + 1
            else:
                order = 1
            obj = API_test_plan(project_id=project_id, project_name=project_name, plan_name=plan_name, plan_desc=plan_desc, valid_flag=valid_flag, order=order)
            obj.save()
        else: #表明是插入
            # logger.info('插入了新记录，正在调整记录的顺序') # 插入记录所在行上方的记录都+1
            try:
                with transaction.atomic():
                    all_objects = API_test_plan.objects.filter(order__gte=order)
                    for item in all_objects:
                        item.order = item.order + 1
                        item.save()

                    obj = API_test_plan(project_id=project_id, project_name=project_name, plan_name=plan_name, plan_desc=plan_desc, valid_flag=valid_flag, order=order)
                    obj.save()
            except Exception as e:
                logger.error('%s' % e)
                return HttpResponse('%s' % e)
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)

# 修改UI测试计划
def update_ui_test_plan(request):
    try:
        params = request.POST

        id = params['id']
        project_id = params['project_id']
        plan_name = params['plan_name']
        plan_desc = params['plan_desc']
        browsers = params['browsers']
        browser_id = params['browser_id']
        valid_flag = params['valid_flag']

        if plan_name == '':
            return  HttpResponse('保存失败，计划名称不能为空')
        elif UI_test_plan.objects.filter(project_id=project_id).filter(plan_name=plan_name).exclude(id=id).exists():
            return  HttpResponse('保存失败，计划名称重复')
        if browsers == '':
            return  HttpResponse('保存失败，运行环境不能为空')
        if valid_flag == '':
            return  HttpResponse('保存失败，是否启用不能为空')

        obj = UI_test_plan.objects.get(id=id)
        obj.plan_name = plan_name
        obj.plan_desc = plan_desc
        obj.browsers = browsers
        obj.browser_id = browser_id
        obj.valid_flag = valid_flag
        obj.save()
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)

# 修改UI测试计划
def update_api_test_plan(request):
    try:
        params = request.POST

        id = params['id']
        project_id = params['project_id']
        plan_name = params['plan_name']
        plan_desc = params['plan_desc']
        valid_flag = params['valid_flag']

        if plan_name == '':
            return  HttpResponse('保存失败，计划名称不能为空')
        elif API_test_plan.objects.filter(project_id=project_id).filter(plan_name=plan_name).exclude(id=id).exists():
            return  HttpResponse('保存失败，计划名称重复')
        if valid_flag == '':
            return  HttpResponse('保存失败，是否启用不能为空')

        obj = API_test_plan.objects.get(id=id)
        obj.plan_name = plan_name
        obj.plan_desc = plan_desc
        obj.valid_flag = valid_flag
        obj.save()
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)

# 关联用例树节点和测试计划
def correlate_testplan_and_testcase(request):
    def find_node_father_path(parent_node_id):
        nonlocal  temp_var
        if  parent_node_id !=0: # 存在上级节点
            father_node = case_tree_db_class.objects.get(id = parent_node_id)
            temp_var = find_node_father_path(father_node.parent_id) + '->' + father_node.text
            return temp_var
        else:
            return temp_var
    try:
        temp_var = ''
        params = request.POST

        plan_id = params['planID']
        plan_type = params['planType']
        if plan_type == 'UITestPlan':
            case_tree_db_class = UI_case_tree
            case_tree_test_plan_db_class = UI_case_tree_test_plan
        elif plan_type == 'APITestPlan':
            case_tree_db_class = API_case_tree
            case_tree_test_plan_db_class = API_case_tree_test_plan

        if params['nodeList']:
            node_list = eval(params['nodeList']) # 转字符串为数组
        else:
            node_list = []

        if params['nodeIDList']:
            node_id_list = eval(params['nodeIDList'])
        else:
            node_id_list = []

        node_id_list_for_old = []
        nodes_for_old = case_tree_test_plan_db_class.objects.filter(plan_id=plan_id)
        for node in nodes_for_old:
            node_id_list_for_old.append(node.node_id)
    except Exception as e:
        return HttpResponse('获取旧关联记录失败：%s' % e)

    # 获取新增关联的用例树节点
    node_id_list_to_add = set(node_id_list) - set(node_id_list_for_old)

    # 获取已关联，且不需要取消关联的用例树节点
    case_id_list_to_update = set(node_id_list) & set(node_id_list_for_old)

    # 获取需要取消关联的用例树节点，即要删除的记录
    case_id_list_to_delete = set(node_id_list_for_old) - set(case_id_list_to_update)

    # 删除要取消关联的用例树节点
    node_order_list_for_deleted = []
    try:
        with transaction.atomic():
            for node_id in case_id_list_to_delete:
                node = case_tree_test_plan_db_class.objects.filter(plan_id=plan_id).filter(node_id=node_id)
                if node.exists():
                    if node.values()[0]['sub_node_num'] == 0:
                        node_order_list_for_deleted.append(node.values()[0]['order'])
                    node.delete()
                else:
                    continue

            # logger.info('删除操作完成，正在重新调整顺序')
            # node_order_list_for_deleted.sort()
            # if node_order_list_for_deleted:
            #     min_order_for_deleted = node_order_list_for_deleted[0]
            #     all_objects = case_tree_test_plan_db_class.objects.filter(plan_id=plan_id).filter(sub_node_num=0).filter(order__gt=min_order_for_deleted).order_by('order')
            #
            #     for object in all_objects:
            #         object.order = min_order_for_deleted
            #         object.save()
            #         min_order_for_deleted = min_order_for_deleted + 1
    except Exception as e:
        logger.error('关联用例树节点到测试计划失败：%s' % e)
        return HttpResponse('删除要取消关联的用例树节点：%s' % e)

    if node_list:
        try:
            node_list = node_list[0]
            order = case_tree_test_plan_db_class.objects.filter(plan_id=plan_id).filter(sub_node_num=0).aggregate(Max('order'))['order__max']
            if not order:
                order = 1
            else:
                order = order + 1
            for node_id in node_id_list_to_add:
                node_id = str(node_id)
                node_name = node_list[node_id]['nodeName']
                sub_node_num = node_list[node_id]['subNodeNum']
                parent_id =  node_list[node_id]['parentID']
                node_path = find_node_father_path(parent_id).lstrip('->')
                temp_var = ''
                node = case_tree_test_plan_db_class(plan_id=plan_id,node_id=node_id,
                                                    node_name=node_name, node_path=node_path, sub_node_num=sub_node_num, order=order)
                node.save()
                if sub_node_num == 0:
                    order = order + 1
            return HttpResponse('success')
        except Exception as e:
            # logger.error('关联用例树节点到测试计划失败：%s' % e)
            return HttpResponse('关联用例树节点到测试计划失败：%s' % e)
    else:
        logger.warn('未获取到需要关联的用例树节点')
        return HttpResponse('success')


# 获取测试计划关联的用例树节点
def get_test_plan_case_tree_nodes(request):
    node_id_list_for_check = []
    try:
        params = request.GET
        plan_id = params['planID']
        plan_type = params['planType']
        if plan_type == 'UITestPlan':
            db_class = UI_case_tree_test_plan
        elif plan_type == 'APITestPlan':
            db_class = API_case_tree_test_plan

        nodes = db_class.objects.filter(plan_id=plan_id).filter(sub_node_num=0).values()
        for node in nodes:
            node_id_list_for_check.append(node['node_id'])
        response = {'result':'success', 'data':node_id_list_for_check}
        response = json.dumps(response)
        return HttpResponse(response)
    except Exception as e:
        response = {'result':'error', 'data':'%s' % e}
        response = json.dumps(response)
        return HttpResponse(response)

