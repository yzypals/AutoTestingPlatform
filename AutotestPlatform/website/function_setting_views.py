from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

import json
import logging
from django.core.paginator import  Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Max
from django.db import transaction

from website.models import Function_setting
from website.models import UI_test_case_step


logger = logging.getLogger('mylogger')

# 系统配置-函数配置
def function_setting(request):
    template = loader.get_template('website/pages/functionSetting.html')
    return HttpResponse(template.render({}, request))

# 获取列表数据
def get_function_settings(request):
    griddata = {"total": 0, "rows": []}
    rows = [] # 用于存储记录行

    try:
        # 获取总记录数
        records = Function_setting.objects.all().order_by('-order').values()
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
        return HttpResponse('%s' % e)

# 新增
def add_function_setting(request):
    try:
        params = request.POST

        function_name = params['function_name']
        param_style = params['param_style']
        order = params['order']

        if not function_name:
            return HttpResponse('函数名称不能为空')
        elif Function_setting.objects.filter(function_name=function_name).exists():
            logger.error('error, 函数名称(%s)已存在' % function_name)
            return HttpResponse('函数名称(%s)已存在' % function_name)
        # if not param_style:
        #     return HttpResponse('参数样例不能为空')

        if order == '': # 如果顺序为空，表明是新增
            all_objects = Function_setting.objects.all()
            if all_objects.exists():
                max_order = all_objects.aggregate(Max('order'))['order__max']
                order = max_order + 1
            else:
                order = 1
            obj = Function_setting(function_name=function_name, param_style=param_style, order=order)
            obj.save()
        else: #表明是插入
            # logger.info('即将插入新记录，正在调整记录的顺序') # 插入记录所在行上方的记录都+1
            try:
                with transaction.atomic():
                    all_objects = Function_setting.objects.filter(order__gte=order)
                    for item in all_objects:
                        item.order = item.order + 1
                        item.save()
                    obj = Function_setting(function_name=function_name, param_style=param_style, order=order)
                    obj.save()
            except Exception as e:
                logger.error('%s' % e)
                return HttpResponse('%s' % e)
        return  HttpResponse('success')
    except Exception as e:
        return HttpResponse('%s' % e)

# 编辑
def edit_function_setting(request):
    try:
        params = request.POST
        id = params['id']
        function_name = params['function_name']
        param_style = params['param_style']
        param_style = param_style.strip()

        if not function_name:
            return HttpResponse('函数名称不能为空')
        elif Function_setting.objects.filter(function_name=function_name).exclude(id=id).exists():
            return HttpResponse('函数名称(%s)已存在' % function_name)

        obj = Function_setting.objects.get(id=id)
        obj.function_name = function_name
        obj.param_style = param_style
        obj.save()

        # logger.info('同步更新UI测试用例详情表')
        ui_case_step_obj_list = UI_test_case_step.objects.filter(object_id=id)
        for ui_case_step_obj in ui_case_step_obj_list:
            ui_case_step_obj.object = function_name
            ui_case_step_obj.save()
        return  HttpResponse('success')
    except Exception as e:
        return HttpResponse('%s' % e)