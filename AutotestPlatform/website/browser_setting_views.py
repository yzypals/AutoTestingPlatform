from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

import json
import logging
from django.core.paginator import  Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Max
from django.db import transaction

from website.models import Browser_setting

logger = logging.getLogger('mylogger')

# 系统配置-浏览器设置
def browser_setting(request):
    template = loader.get_template('website/pages/browserSetting.html')
    return HttpResponse(template.render({}, request))

# 获取系统配置-浏览器配置表，列表数据
def get_browser_settings(request):
    griddata = {"total": 0, "rows": []}
    rows = [] # 用于存储记录行

    # 获取总记录数
    envs = Browser_setting.objects.all().order_by('-order').values()
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

# 新增浏览器配置
def add_browser_setting(request):
    try:
        params = request.POST

        browser_name = params['browser']
        order = params['order']
        if not browser_name:
            return HttpResponse('浏览器名称不能为空')

        if_name_exists = Browser_setting.objects.filter(browser=browser_name).exists()
        if if_name_exists:
            # logger.error('error, 环境名称(%s)已存在' % browser_name)
            return HttpResponse('环境名称(%s)已存在' % browser_name)

        if order == '': # 如果顺序为空，表明是新增
            all_objects = Browser_setting.objects.all()
            if all_objects.exists():
                max_order = all_objects.aggregate(Max('order'))['order__max']
                order = max_order + 1
            else:
                order = 1
            obj = Browser_setting(browser = browser_name, order=order)
            obj.save()
        else: #表明是插入
            logger.info('即将插入新记录，正在调整记录的顺序') # 插入记录所在行上方的记录都+1
            all_objects = Browser_setting.objects.filter(order__gte=order)
            try:
                with transaction.atomic():
                    for item in all_objects:
                        item.order = item.order + 1
                        item.save()
                    obj = Browser_setting(browser = browser_name, order=order)
                    obj.save()
            except Exception as e:
                logger.error('%s' % e)
                return HttpResponse('%s' % e)
        return  HttpResponse('success')
    except Exception as e:
        return HttpResponse('%s' % e)


# 系统设置-浏览器配置，修改浏览器名称
def edit_browser_setting(request):
    try:
        params = request.POST

        id = params['id']
        name = params['browser']
        if not name:
            return HttpResponse('浏览器名称不能为空')

        if_name_exists = Browser_setting.objects.filter(browser=name).exclude(id=id).exists()
        if if_name_exists:
            # logger.error('error, 浏览器名称(%s)已存在' % name)
            return HttpResponse('浏览器名称(%s)已存在' % name)

        obj = Browser_setting.objects.get(id=id)
        obj.browser = name
        obj.save()
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)
