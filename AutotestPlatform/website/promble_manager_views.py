from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

import json
import logging
import datetime
from django.core.paginator import  Paginator, PageNotAnInteger, EmptyPage
from website.models import Promble_feedback
from django.db.models import Max

logger = logging.getLogger('mylogger')

# 测试管理-反馈问题管理
def promble_manager(request):
    template = loader.get_template('website/pages/prombleManager.html')
    return HttpResponse(template.render({}, request))

# # 对应的列表数据
def get_prombles(request):
    grid_data = {"total": 0, "rows": []}
    rows = [] # 用于存储记录行

    try:
        # 获取总记录数
        prombles = Promble_feedback.objects.order_by('-order').values()
        grid_data["total"] = len(prombles)

        page_num = request.GET.get('page') # 记录请求的是第几页数据
        rows_num = request.GET.get('rows') # 记录请求每页的记录数

        paginator = Paginator(prombles, rows_num) # 设置每页展示的数据

        try:
            page = paginator.page(page_num)
        except PageNotAnInteger as e: # 如果请求的页面编号不存在，返回第一页数据
            logger.warn('%s' % e)
            page = paginator.page(1)
        except EmptyPage as e: # 如果请求页面，超出页面范围，返回最后一页数据
            logger.warn('%s' % e)
            page = paginator.page(paginator.num_pages)

        prombles = page.object_list
        for promble in prombles:
            rows.append(promble)
        grid_data["rows"] =  rows
        grid_data = json.dumps(grid_data)
        return HttpResponse(grid_data)
    except Exception as e:
        return HttpResponse('%s' % e)

# 新增问题
def add_promble(request):
    try:
        params = request.POST

        desc = params['desc']
        issuer = params['issuer']
        tracer = params['tracer']
        handler = params['handler']
        mark = params['mark']

        record_time = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        status = '待跟进'

        if desc == '':
            # logger.error('保存失败，问题描述不能为空')
            return HttpResponse('保存失败，问题描述不能为空')

        all_objects = Promble_feedback.objects.all()
        if all_objects:
            max_order = all_objects.aggregate(Max('order'))['order__max']
            order = max_order + 1
        else:
            order = 1
        promble_obj = Promble_feedback(desc=desc, status=status, issuer=issuer, tracer=tracer, handler=handler,
                                  record_time=record_time,order=order, mark=mark)

        promble_obj.save()
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)


# 更新问题
def update_promble(request):
    try:
        params = request.POST
        id = params['id']
        desc = params['desc']
        issuer = params['issuer']
        tracer = params['tracer']
        handler = params['handler']
        mark = params['mark']

        if desc == '':
            # logger.error('保存失败，问题描述不能为空')
            return HttpResponse('保存失败，问题描述不能为空')

        promble_obj = Promble_feedback.objects.get(id=id)
        promble_obj.desc = desc
        promble_obj.issuer = issuer
        promble_obj.tracer = tracer
        promble_obj.handler = handler
        promble_obj.mark = mark

        promble_obj.save()
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)

# 处理问题
def handle_promble(request):
    try:
        params = request.POST
        id = params['rowID']
        op_type = params['opType']
        promble_obj = Promble_feedback.objects.get(id = id)
        if op_type == '跟进':
            promble_obj.status = '跟进中'
            promble_obj.start_trace_time = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
            # logger.info('设置顺序为正在跟进问题|已解决问题中最大顺序值+1')
            promble_objs = Promble_feedback.objects.filter(status='跟进中')
            if promble_objs:
                max_order =promble_objs.aggregate(Max('order'))['order__max']
            else:
                promble_objs = Promble_feedback.objects.filter(status='已解决')
                if promble_objs:
                    max_order = promble_objs.aggregate(Max('order'))['order__max']
                else:
                    max_order = 0

            # logger.info('更新顺序值在（找到的最大顺序值，正在操作记录的顺序值）区间的记录，顺序值+1')
            promble_objs = Promble_feedback.objects.filter(order__gt=max_order, order__lt=promble_obj.order)
            for promble in promble_objs:
                promble.order = promble.order + 1
                promble.save()

            promble_obj.order = max_order + 1
        elif op_type == '关闭':
            promble_obj.status = '已解决'
            promble_obj.solved_time = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')

            # logger.info('设置当前记录顺序为已解决问题中最大顺序值+1')
            promble_objs = Promble_feedback.objects.filter(status='已解决')
            if promble_objs:
                max_order =promble_objs.aggregate(Max('order'))['order__max']
            else:
                max_order = 0

            # logger.info('更新顺序值在（已解决问题最大顺序值，正在操作记录的顺序值）区间的记录，顺序值+1')
            promble_objs = Promble_feedback.objects.filter(order__gt=max_order, order__lt=promble_obj.order)
            for promble in promble_objs:
                promble.order = promble.order + 1
                promble.save()

            promble_obj.order = max_order + 1
        elif op_type == '激活':
            promble_obj.status = '跟进中'
            promble_obj.start_trace_time = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
            promble_obj.mark = promble_obj.mark + '--重新打开'
            # logger.info('设置顺序为正在跟进问题中|已解决问题中最大顺序值')
            promble_objs = Promble_feedback.objects.filter(status='跟进中')
            if promble_objs:
                max_order =promble_objs.aggregate(Max('order'))['order__max']
            else:
                promble_objs = Promble_feedback.objects.filter(status='已解决')
                if promble_objs:
                    max_order =  promble_objs.aggregate(Max('order'))['order__max']
                else:
                    max_order = 1

            # logger.info('更新顺序值在（正在操作记录的顺序值，找到的记录顺序最大值]区间的记录，顺序值+1')
            promble_objs = Promble_feedback.objects.filter(order__gt=promble_obj.order, order__lte=max_order)
            for promble in promble_objs:
                promble.order = promble.order - 1
                promble.save()

            promble_obj.order = max_order
            promble_obj.solved_time = ''
        promble_obj.save()
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return  HttpResponse('%s' % e)