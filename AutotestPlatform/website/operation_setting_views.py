from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

import json
import logging
from django.core.paginator import  Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Max
from django.db import transaction

from website.models import Operation_for_object

logger = logging.getLogger('mylogger')

# 系统配置-项目配置
def operation_setting(request):
    template = loader.get_template('website/pages/operationSetting.html')
    return HttpResponse(template.render({}, request))

# 获取列表数据
def get_operation_settings(request):
    griddata = {"total": 0, "rows": []}
    rows = [] # 用于存储记录行

    try:
        # 获取总记录数
        records = Operation_for_object.objects.all().order_by('-order').values()
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
def add_operation_setting(request):
    try:
        params = request.POST

        object_type = params['object_type']
        operation = params['operation'].strip().lower()
        order = params['order']
        if not object_type:
            return HttpResponse('对象类型不能为空')
        if not operation:
            return HttpResponse('对象操作不能为空')

        if_name_exists = Operation_for_object.objects.filter(operation=operation).exists()
        if if_name_exists:
            # logger.error('error, 可执行操作(%s)已存在' % operation)
            return HttpResponse('可执行操作(%s)已存在' % operation)

        if order == '': # 如果顺序为空，表明是新增
            all_objects = Operation_for_object.objects.all()
            if all_objects.exists():
                max_order = all_objects.aggregate(Max('order'))['order__max']
                order = max_order + 1
            else:
                order = 1
            obj = Operation_for_object(object_type=object_type, operation=operation,order=order)
            obj.save()
        else: #表明是插入
            # logger.info('即将新记录，正在调整记录的顺序') # 插入记录所在行上方的记录都+1
            try:
                with transaction.atomic():
                    all_objects = Operation_for_object.objects.filter(order__gte=order)
                    for item in all_objects:
                        item.order = item.order + 1
                        item.save()

                    obj = Operation_for_object(object_type=object_type, operation=operation,order=order)
                    obj.save()
            except Exception as e:
                logger.error('%s' % e)
                return  HttpResponse('%s' % e)
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return  HttpResponse('%s' % e)

# 修改
def edit_operation_setting(request):
    try:
        params = request.POST

        id = params['id']
        object_type = params['object_type']
        operation = params['operation'].strip().lower()
        if not object_type:
            return HttpResponse('对象类型不能为空')
        if not operation:
            return HttpResponse('可执行操作')
        elif Operation_for_object.objects.filter(operation=operation).exclude(id=id).exists():
            # logger.error('error, 可执行操作(%s)已存在' % operation)
            return HttpResponse('可执行操作(%s)已存在' % operation)

        obj = Operation_for_object.objects.get(id=id)
        obj.object_type = object_type
        obj.operation = operation
        obj.save()
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return  HttpResponse('%s' % e)