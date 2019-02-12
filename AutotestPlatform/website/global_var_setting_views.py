from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

import json
import logging
from django.core.paginator import  Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Max
from django.db import transaction

from website.models import Global_variable_setting

logger = logging.getLogger('mylogger')

# 系统配置-数据库配置
def global_var_setting(request):
    template = loader.get_template('website/pages/globalVarSetting.html')
    return HttpResponse(template.render({}, request))

# 获取系统配置-数据库配置，列表数据
def get_global_var_settings(request):
    griddata = {"total": 0, "rows": []}
    rows = [] # 用于存储记录行

    # 获取总记录数
    records = Global_variable_setting.objects.all().order_by('-order').values()
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

# 新增
def add_global_var_setting(request):
    try:
        params = request.POST

        name = params['name'].replace(' ', '').replace('\t', '').replace('-', '').lower()
        value = params['value']
        project_type = params['project_type']
        project_name = params['project_name']
        project_id = params['project_id']
        environment = params['environment']
        order = params['order']

        if name == '':
            return HttpResponse('变量名不能为空')
        elif Global_variable_setting.objects.filter(project_id=project_id).filter(name=name).exists():
            return HttpResponse('变量名已存在')
        if value == '':
            return HttpResponse('变量值不能为空')
        if not project_type:
            return HttpResponse('项目类型不能为空')
        if not project_name:
            return HttpResponse('所属项目不能为空')
        if not environment:
            return HttpResponse('所属环境不能为空')

        if order == '': # 如果顺序为空，表明是新增
            all_objects = Global_variable_setting.objects.all()
            if all_objects.exists():
                max_order = all_objects.aggregate(Max('order'))['order__max']
                order = max_order + 1
            else:
                order = 1
            obj = Global_variable_setting(name=name, value=value, project_type=project_type, project_name=project_name, environment=environment, order=order, project_id=project_id)
            obj.save()
        else: #表明是插入
            # logger.info('即将插入新记录，正在调整记录的顺序') # 插入记录所在行上方的记录都+1
            try:
                with transaction.atomic():
                    all_objects = Global_variable_setting.objects.filter(order__gte=order)
                    for item in all_objects:
                        item.order = item.order + 1
                        item.save()

                    obj = Global_variable_setting(name=name, value=value, project_type=project_type, project_name=project_name, environment=environment, order=order, project_id=project_id)
                    obj.save()
            except Exception as e:
                reason = '%s' % e
                logger.error(reason)
                return HttpResponse(reason)
        return  HttpResponse('success')
    except Exception as e:
        reason = '%s' % e
        logger.error(reason)
        return HttpResponse(reason)

# 编辑
def edit_global_var_setting(request):
    try:
        params = request.POST

        id = params['id']
        name = params['name'].replace(' ', '').replace('\t', '').replace('-', '').lower()
        value = params['value']
        project_type = params['project_type']
        project_name = params['project_name']
        project_id = params['project_id']
        environment = params['environment']

        if name == '':
            return HttpResponse('变量名不能为空')
        elif Global_variable_setting.objects.filter(project_id=project_id).filter(name=name).exists():
            return HttpResponse('变量名已存在')
        if value == '':
            return HttpResponse('变量值不能为空')
        if not project_type:
            return HttpResponse('项目类型不能为空')
        if not project_name:
            return HttpResponse('所属项目不能为空')
        if not environment:
            return HttpResponse('所属环境不能为空')

        obj = Global_variable_setting.objects.get(id=id)
        obj.name = name
        obj.value = value
        obj.project_type = project_type
        obj.project_name = project_name
        obj.environment = environment
        if project_id != '-1':
            obj.project_id = project_id
        obj.save()
        return  HttpResponse('success')
    except Exception as e:
        return HttpResponse('%s' % e)