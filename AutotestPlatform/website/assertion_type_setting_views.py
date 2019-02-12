from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

import json
import logging
from django.core.paginator import  Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Max
from django.db import transaction
from website.models import Assertion_type_setting


logger = logging.getLogger('mylogger')

# 系统配置-断言配置
def assertion_type_setting(request):
    template = loader.get_template('website/pages/assertionTypeSetting.html')
    return HttpResponse(template.render({}, request))

# 获取列表数据
def get_assertion_type_settings(request):
    griddata = {"total": 0, "rows": []}
    rows = [] # 用于存储记录行

    try:
        # 获取总记录数
        records = Assertion_type_setting.objects.all().order_by('-order').values()
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
def add_assertion_type_setting(request):
    try:
        params = request.POST
        op_type = params['op_type']
        assertion_type = params['assertion_type'].strip().replace(' ', '').lower()
        assertion_pattern = params['assertion_pattern'].strip()
        order = params['order']

        if not op_type:
            return HttpResponse('适用类型不能为空')
        if not assertion_type:
            return HttpResponse('断言类型不能为空')
        elif Assertion_type_setting.objects.filter(assertion_type=assertion_type).exists():
            # logger.error('error, 断言类型(%s)已存在' % assertion_type)
            return HttpResponse('断言类型(%s)已存在' % assertion_type)
        if not assertion_pattern:
            return HttpResponse('断言模式不能为空')

        if order == '': # 如果顺序为空，表明是新增
            all_objects = Assertion_type_setting.objects.all()
            if all_objects.exists():
                max_order = all_objects.aggregate(Max('order'))['order__max']
                order = max_order + 1
            else:
                order = 1
            obj = Assertion_type_setting(op_type=op_type, assertion_type=assertion_type, assertion_pattern=assertion_pattern, order=order)
            obj.save()
        else: #表明是插入
            try:
                # logger.info('即将插入新记录，正在调整记录的顺序') # 插入记录所在行上方的记录都+1
                with transaction.atomic():
                    all_objects = Assertion_type_setting.objects.filter(order__gte=order)
                    for item in all_objects:
                        item.order = item.order + 1
                        item.save()

                    obj = Assertion_type_setting(op_type=op_type, assertion_type=assertion_type, assertion_pattern=assertion_pattern, order=order)
                    obj.save()
            except Exception as e:
                logger.error('%s' % e)
                return HttpResponse('%s' % e)
        return  HttpResponse('success')
    except Exception as e:
        return HttpResponse('%s' % e)

# 编辑
def edit_assertion_type_setting(request):
    try:
        params = request.POST
        id = params['id']
        op_type = params['op_type']
        assertion_type = params['assertion_type'].strip().replace(' ', '').lower()
        assertion_pattern = params['assertion_pattern'].strip()

        if not op_type:
            return HttpResponse('适用类型不能为空')
        if not assertion_type:
            return HttpResponse('断言类型不能为空')
        elif Assertion_type_setting.objects.filter(assertion_type=assertion_type).exclude(id=id).exists():
            # logger.error('error, 断言类型(%s)已存在' % assertion_type)
            return HttpResponse('断言类型(%s)已存在' % assertion_type)
        if not assertion_pattern:
            return HttpResponse('断言模式不能为空')
        obj = Assertion_type_setting.objects.get(id=id)
        obj.op_type = op_type
        obj.assertion_type = assertion_type
        obj.assertion_pattern = assertion_pattern

        obj.save()
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)
