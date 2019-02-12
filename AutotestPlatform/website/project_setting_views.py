from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

import json
import logging
from django.core.paginator import  Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Max
from django.db import transaction

from website.models import UI_project_setting
from website.models import API_project_setting
from website.models import Project_chosen
from website.models import Page_tree
from website.models import UI_case_tree
from website.models import API_case_tree
from website.models import Database_setting
from website.models import UI_test_plan
from website.models import API_test_plan
from website.models import Running_plan

logger = logging.getLogger('mylogger')

# 项目管理-UI项目配置
def ui_project_setting(request):
    template = loader.get_template('website/pages/UIProjectSetting.html')
    return HttpResponse(template.render({}, request))

# 项目管理-API项目配置
def api_project_setting(request):
    template = loader.get_template('website/pages/APIProjectSetting.html')
    return HttpResponse(template.render({}, request))

# 获取列表数据
def get_ui_project_settings(request):
    griddata = {"total": 0, "rows": []}
    rows = [] # 用于存储记录行

    try:
        # 获取总记录数
        records = UI_project_setting.objects.all().order_by('-order').values()
        griddata["total"] = len(records)

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

        objs = page.object_list
        for obj in objs:
            rows.append(obj)
        griddata["rows"] =  rows
        griddata = json.dumps(griddata)
        return HttpResponse(griddata)
    except Exception as e:
        logger.error('%s' % e)
        return  HttpResponse('%s' % e)


# 获取列表数据
def get_api_project_settings(request):
    griddata = {"total": 0, "rows": []}
    rows = [] # 用于存储记录行

    try:
        # 获取总记录数
        records = API_project_setting.objects.all().order_by('-order').values()
        griddata["total"] = len(records)

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

        objs = page.object_list
        for obj in objs:
            rows.append(obj)
        griddata["rows"] =  rows
        griddata = json.dumps(griddata)
        return HttpResponse(griddata)
    except Exception as e:
        logger.error('%s' % e)
        return  HttpResponse('%s' % e)

# 新增
def add_ui_project_setting(request):
    try:
        params = request.POST

        project_name = params['project_name']
        home_page = params['home_page']
        environment = params['environment']
        valid_flag = params['valid_flag']
        order = params['order']
        if not project_name:
            return HttpResponse('项目名称不能为空')
        elif UI_project_setting.objects.filter(project_name=project_name).exists():
            # logger.error('error, 项目名称(%s)已存在' % project_name)
            return HttpResponse('项目名称(%s)已存在' % project_name)
        if not home_page:
            return HttpResponse('项目主页不能为空')
        if not environment:
            return HttpResponse('所属环境不能为空')
        if not valid_flag:
            return HttpResponse('是否启用不能为空')

        if order == '': # 如果顺序为空，表明是新增
            all_objects = UI_project_setting.objects.all()
            if all_objects.exists():
                max_order = all_objects.aggregate(Max('order'))['order__max']
                order = max_order + 1
            else:
                order = 1
            obj = UI_project_setting(project_name=project_name, home_page=home_page,environment=environment, valid_flag=valid_flag, order=order)
            obj.save()
        else: #表明是插入
            # logger.info('即将插入新记录，正在调整记录的顺序') # 插入记录所在行上方的记录都+1
            try:
                with transaction.atomic():
                    all_objects = UI_project_setting.objects.filter(order__gte=order)
                    for item in all_objects:
                        item.order = item.order + 1
                        item.save()

                    obj = UI_project_setting(project_name=project_name, home_page=home_page,environment=environment, valid_flag=valid_flag, order=order)
                    obj.save()
            except Exception as e:
                logger.error('%s' % e)
                return  HttpResponse('%s' % e)

        project_id = UI_project_setting.objects.filter(project_name=project_name).values()[0]['id']

        # 往UI页面树数据表中写一条记录，即对应根目录
        obj = Page_tree(text=project_name, state='open', parent_id=0, iconCls='', attributes='', project_id=project_id, order=1)
        obj.save()

        # 往UI用例树数据表中写一条记录，即对应根目录
        obj = UI_case_tree(text=project_name, state='open', parent_id=0, iconCls='', attributes='', project_id=project_id, order=1)
        obj.save()

        # 页面树还没选择默认的项目，插入默认项目
        if not Project_chosen.objects.filter(tree_type='PageTree').exists():
            obj = Project_chosen(project_name=project_name, tree_type='PageTree', project_id=project_id)
            obj.save()

        # 用例树还没选择默认的项目，插入默认项目
        if not Project_chosen.objects.filter(tree_type='UICaseTree').exists():
            obj = Project_chosen(project_name=project_name, tree_type='UICaseTree', project_id=project_id)
            obj.save()

        # UI测试计划管理-用例树还没选择默认的项目，插入默认项目
        if not Project_chosen.objects.filter(tree_type='PlanUICaseTree').exists():
            obj = Project_chosen(project_name=project_name, tree_type='PlanUICaseTree', project_id=project_id)
            obj.save()
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return  HttpResponse('%s' % e)

# 新增
def add_api_project_setting(request):
    try:
        params = request.POST

        project_name = params['project_name']
        protocol = params['protocol'].strip().lower()
        host = params['host'].strip()
        port = params['port'].strip()
        environment = params['environment']
        valid_flag = params['valid_flag']
        order = params['order']
        if not project_name:
            return HttpResponse('项目名称不能为空')
        elif API_project_setting.objects.filter(project_name=project_name).exists():
            return HttpResponse('项目名称(%s)已存在' % project_name)
        if protocol == '':
            return HttpResponse('接口请求协议不能为空')
        elif protocol !='' and protocol not in ('https', 'http'):
            return HttpResponse('协议只能是http、https')
        if not host:
            return HttpResponse('主机地址不能为空')
        if not environment:
            return HttpResponse('所属环境不能为空')
        if not valid_flag:
            return HttpResponse('是否启用不能为空')

        if protocol == 'http' and port == '':
            port = 80 # http请求，默认为80
        elif protocol != 'http' and port == '':
            return HttpResponse('非http协议，端口不能为空')
        elif not port.isdigit():
            return HttpResponse('端口只能为数字')

        if order == '': # 如果顺序为空，表明是新增
            all_objects = API_project_setting.objects.all()
            if all_objects.exists():
                max_order = all_objects.aggregate(Max('order'))['order__max']
                order = max_order + 1
            else:
                order = 1
            obj = API_project_setting(project_name=project_name, protocol=protocol, host=host, port=port, environment=environment, valid_flag=valid_flag, order=order)
            obj.save()
        else: #表明是插入
            # logger.info('即将插入新记录，正在调整记录的顺序') # 插入记录所在行上方的记录都+1
            try:
                with transaction.atomic():
                    all_objects = API_project_setting.objects.filter(order__gte=order)
                    for item in all_objects:
                        item.order = item.order + 1
                        item.save()

                    obj = API_project_setting(project_name=project_name, protocol=protocol, host=host, port=port, environment=environment, valid_flag=valid_flag, order=order)
                    obj.save()
            except Exception as  e:
                logger.error('%s' % e)
                return  HttpResponse('%s' % e)

        project_id = API_project_setting.objects.filter(project_name=project_name).values()[0]['id']

        # 往API用例树数据表中写一条记录，即对应根目录
        obj = API_case_tree(text=project_name, state='open', parent_id=0, iconCls='', attributes='', project_id=project_id, order=1)
        obj.save()

        # 用例树还没选择默认的项目，插入默认项目
        if not Project_chosen.objects.filter(tree_type='APICaseTree').exists():
            obj = Project_chosen(project_name=project_name, tree_type='APICaseTree', project_id=project_id)
            obj.save()

        # API测试计划管理-用例树还没选择默认的项目，插入默认项目
        if not Project_chosen.objects.filter(tree_type='PlanAPICaseTree').exists():
            obj = Project_chosen(project_name=project_name, tree_type='PlanAPICaseTree', project_id=project_id)
            obj.save()

        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return  HttpResponse('%s' % e)

# 编辑
def edit_ui_project_setting(request):
    try:
        params = request.POST

        id = params['id']
        project_name = params['project_name']
        home_page = params['home_page']
        environment = params['environment']
        valid_flag = params['valid_flag']
        if not project_name:
            return HttpResponse('项目名称不能为空')
        elif UI_project_setting.objects.filter(project_name=project_name).exclude(id=id).exists():
            # logger.error('error, 项目名称(%s)已存在' % project_name)
            return HttpResponse('项目名称(%s)已存在' % project_name)
        if not home_page:
            return HttpResponse('项目主页不能为空')
        if not environment:
            return HttpResponse('所属环境不能为空')
        if not valid_flag:
            return HttpResponse('是否启用不能为空')

        obj = UI_project_setting.objects.get(id=id)
        obj.project_name = project_name
        obj.home_page = home_page
        obj.environment = environment
        obj.valid_flag = valid_flag
        obj.save()

        # logger.info('同步更新数据库配置表')
        obj_list = Database_setting.objects.filter(project_type='UI项目').filter(project_id=id)
        for obj in obj_list:
            obj.project_name = project_name
            obj.save()

        # logger.info('同步更新UI测试计划表')
        obj_list = UI_test_plan.objects.filter(project_id=id)
        for obj in obj_list:
            obj.project_name = project_name
            obj.save()

        # logger.info('同步更新运行计划表')
        obj_list = Running_plan.objects.filter(project_id=id)
        for obj in obj_list:
            obj.project_name = project_name
            obj.save()

        # logger.info('同步更新当前所选项目表')
        obj_list = Project_chosen.objects.filter(project_id=id).exclude(tree_type='SprintTree').exclude(tree_type='APICaseTree').exclude(tree_type='PlanAPICaseTree')
        for obj in obj_list:
            obj.project_name = project_name
            obj.save()
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return  HttpResponse('%s' % e)


# 编辑
def edit_api_project_setting(request):
    try:
        params = request.POST

        id = params['id']
        project_name = params['project_name']
        protocol = params['protocol'].strip().lower()
        host = params['host'].strip()
        port = params['port'].strip()
        environment = params['environment']
        valid_flag = params['valid_flag']
        if not project_name:
            return HttpResponse('项目名称不能为空')
        elif API_project_setting.objects.filter(project_name=project_name).exclude(id=id).exists():
            return HttpResponse('项目名称(%s)已存在' % project_name)
        if not protocol:
            return HttpResponse('接口请求协议不能为空')
        elif protocol not in ('https', 'http'):
            return HttpResponse('协议只能是http、https')
        if not host:
            return HttpResponse('主机地址不能为空')
        if not environment:
            return HttpResponse('所属环境不能为空')
        if not valid_flag:
            return HttpResponse('是否启用不能为空')

        if protocol == 'http' and port == '':
            port = 80 # http请求，默认为80
        elif protocol != 'http' and port == '':
            return HttpResponse('非http协议，端口不能为空')
        elif not port.isdigit():
            return HttpResponse('端口只能为数字')


        obj = API_project_setting.objects.get(id=id)
        obj.project_name = project_name
        obj.protocol = protocol
        obj.host = host
        obj.port = port
        obj.environment = environment
        obj.valid_flag = valid_flag
        obj.save()

        # logger.info('同步更新数据库配置表')
        obj_list = Database_setting.objects.filter(project_type='API项目').filter(project_id=id)
        for obj in obj_list:
            obj.project_name = project_name
            obj.save()

        # logger.info('同步更新API测试计划表')
        obj_list = API_test_plan.objects.filter(project_id=id)
        for obj in obj_list:
            obj.project_name = project_name
            obj.save()

        # logger.info('同步更新当前所选项目表')
        obj_list = Running_plan.objects.filter(project_id=id)
        for obj in obj_list:
            obj.project_name = project_name
            obj.save()

        # logger.info('同步更新运行计划表')
        obj_list = Project_chosen.objects.filter(project_id=id).exclude(tree_type='SprintTree').exclude(tree_type='UICaseTree').exclude(tree_type='PlanUICaseTree').exclude(tree_type='PageTree')
        for obj in obj_list:
            obj.project_name = project_name
            obj.save()
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return  HttpResponse('%s' % e)