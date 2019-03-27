from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

import json
import logging
from django.core.paginator import  Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Max,F
from django.db import transaction

from website.models import Env_setting
from website.models import UI_project_setting
from website.models import API_project_setting
from website.models import Database_setting
from website.models import Global_variable_setting

logger = logging.getLogger('mylogger')

# 系统配置-环境设置
def env_setting(request):
    template = loader.get_template('website/pages/envSetting.html')
    return HttpResponse(template.render({}, request))

# 获取系统配置-环境配置表，列表数据
def get_env_settings(request):
    griddata = {"total": 0, "rows": []}
    rows = [] # 用于存储记录行

    # 获取总记录数
    envs = Env_setting.objects.all().order_by('-order').values()
    griddata["total"] = len(envs)

    page_num = request.GET.get('page') # 记录请求的是第几页数据
    rows_num = request.GET.get('rows') # 记录请求每页的记录数

    paginator = Paginator(envs, rows_num) # 设置每页展示的数据

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

# 新增环境配置
def add_env_setting(request):
    try:
        params = request.POST

        env_name = params['env']
        order = params['order']
        if not env_name:
            return HttpResponse('环境名称不能为空')

        if_name_exists = Env_setting.objects.filter(env=env_name).exists()
        if if_name_exists:
            return HttpResponse('环境名称(%s)已存在' % env_name)

        if order == '': # 如果顺序为空，表明是新增
            all_objects = Env_setting.objects.all()
            if all_objects.exists():
                max_order = all_objects.aggregate(Max('order'))['order__max']
                order = max_order + 1
            else:
                order = 1
            obj = Env_setting(env = env_name, order=order)
            obj.save()
        else: #表明是插入
            logger.info('即将插入新记录，正在调整记录的顺序') # 插入记录所在行上方的记录都+1
            all_objects = Env_setting.objects.filter(order__gte=order)
            try:
                with transaction.atomic():
                    for item in all_objects:
                        item.order = item.order + 1
                        item.save()
                    obj = Env_setting(env = env_name, order=order)
                    obj.save()
            except Exception as e:
                logger.error('%s' % e)
                return HttpResponse('%s' % e)
        return  HttpResponse('success')
    except Exception as e:
        return HttpResponse('%s' % e)


# 系统设置-环境配置，修改环境称
def edit_env_setting(request):
    try:
        params = request.POST

        id = params['id']
        env = params['env']
        if not env:
            return HttpResponse('环境名称不能为空')

        if_name_exists = Env_setting.objects.filter(env=env).exclude(id=id).exists()
        if if_name_exists:
            return HttpResponse('环境名称(%s)已存在' % env)

        obj = Env_setting.objects.get(id=id)
        try:
            with transaction.atomic():
                # 更改UI、API项目配置、数据库配置表引用的环境名称
                UI_project_setting.objects.filter(environment_id=id).update(environment=env)
                API_project_setting.objects.filter(environment_id=id).update(environment=env)
                Database_setting.objects.filter(environment=obj.env).update(environment=env) # 数据库配置environment_id可能存放多个env对应的id，需要使用模糊查询，所以采用按名称查询

                global_vars = Global_variable_setting.objects.filter(environment__contains=obj.env)
                for global_var in global_vars:
                    if obj.env in global_var.environment:
                        global_var.environment = global_var.environment.replace(obj.env, env)
                        global_var.save()
                obj.env = env
                obj.save()
            return HttpResponse('success')
        except Exception as e:
            logger.error('%s' % e)
            return HttpResponse('%s' % e)
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)
