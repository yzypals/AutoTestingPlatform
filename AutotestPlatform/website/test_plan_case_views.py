from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.db.models import Max
from django.db.models import Min
from django.db import  transaction
from django.core.paginator import  Paginator, PageNotAnInteger, EmptyPage

import json
import logging

from website.models import UI_case_tree_test_plan
from website.models import API_case_tree_test_plan

logger = logging.getLogger('mylogger')

# 测试计划-操作|查看用例
def ui_test_plan_case_view(request):
    template = loader.get_template('website/pages/UITestPlanCaseView.html')
    return HttpResponse(template.render({}, request))


def api_test_plan_case_view(request):
    template = loader.get_template('website/pages/APITestPlanCaseView.html')
    return HttpResponse(template.render({}, request))

# 查看用例-列表数据
def load_test_plan_cases(request):
    griddata = {"total": 0, "rows": []}
    rows = [] # 用于存储记录行

    plan_id = request.GET['planID']
    plan_type = request.GET['planType']
    if plan_type == 'UITestPlan':
        db_class = UI_case_tree_test_plan
    elif plan_type == 'APITestPlan':
        db_class = API_case_tree_test_plan

    # 获取总记录数
    records = db_class.objects.filter(plan_id=plan_id).filter(sub_node_num=0).order_by('order').values()
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

# 重新调整datagrid中的记录的顺序值
def reorder_rows(request):
    params = request.POST
    class_name = params['datagridID']
    db_class = globals()[class_name]
    plan_id = params['planID']
    logger.info(plan_id)
    logger.info(db_class)
    try:
        with transaction.atomic():
            min_order = 1
            all_objects = db_class.objects.filter(plan_id=plan_id).filter(sub_node_num=0).order_by('order')
            for object in all_objects:
                object.order = min_order
                object.save()
                min_order = min_order + 1
        return HttpResponse('success')
    except Exception as e:
        return HttpResponse('%s' % e)


# 置顶、置底datagrid中的行记录
def put_row_top_or_bottom(request):
    params = request.POST
    class_name = params['datagridID']
    db_class = globals()[class_name]
    plan_id = params['planID']
    row_id = params['rowID']
    direction = params['direction']

    try:
        case = db_class.objects.get(id=row_id)
        if direction == 'top':
            min_order = db_class.objects.filter(plan_id = plan_id).filter(sub_node_num=0).aggregate(Min('order'))['order__min']
            if case.order == min_order:
                return HttpResponse('AlreadyTop')
            else:
                case.order = min_order - 1
                case.save()
        elif direction == 'bottom':
            max_order = db_class.objects.filter(plan_id = plan_id).filter(sub_node_num=0).aggregate(Max('order'))['order__max']
            if max_order ==  case.order:
                return HttpResponse('AlreadyBottom')
            else:
                case.order = max_order + 1
                case.save()
        else:
            return HttpResponse('参数错误')

        return HttpResponse('success')
    except Exception as e:
        return HttpResponse('%s' % e)


# # 置顶、置底操作
# def put_row_top_or_bottom(request):
#     params = request.POST
#     datagrid = params['datagridID']
#     if datagrid == 'UI_case_tree_test_plan':
#         db_class = UI_case_tree_test_plan
#     elif datagrid == 'API_case_tree_test_plan':
#         db_class = API_case_tree_test_plan
#     plan_id = params['planID']
#     row_id = params['rowID']
#     row_order = params['rowOrder']
#     direction = params['direction']
#
#     try:
#         case = db_class.objects.get(id=row_id)
#         if direction == 'top':
#             case.order = 1
#             case.save()
#
#             logger.info('正在调整其它用例的顺序')
#             cases = db_class.objects.filter(plan_id=plan_id).filter(sub_node_num=0).filter(order__lt = row_order).exclude(id=row_id)
#             for case in cases:
#                 case.order = case.order + 1
#                 case.save()
#         elif direction == 'bottom':
#             max_order = db_class.objects.filter(plan_id = plan_id).filter(sub_node_num=0).aggregate(Max('order'))['order__max']
#             case.order = max_order
#             case.save()
#
#             logger.info('正在调整其它用例的顺序')
#             cases = db_class.objects.filter(plan_id=plan_id).filter(sub_node_num=0).filter(order__gt = row_order).exclude(id=row_id)
#             for case in cases:
#                 case.order = case.order - 1
#                 case.save()
#         else:
#             return HttpResponse('参数错误')
#
#         return HttpResponse('success')
#     except Exception as e:
#         return HttpResponse('%s' % e)


# # 删除用例
# def remove_testplan_case(request):
#     try:
#         params = request.POST
#         logger.info('待删除的记录ID列表有：%s' % params)
#
#         row_ids = eval(params['rowIDs'])
#         class_name = params['datagridID']
#
#         order_list = []  # 存放被删除记录的顺序
#         db_class = globals()[class_name]
#
#         try:
#             with transaction.atomic():
#                 for row_id in row_ids:
#                     row_id = int(row_id)
#                     record = db_class.objects.filter(id=row_id)
#                     if not record.exists():
#                         logger.error('error, ID(%s)不存在' % row_id)
#                         continue
#                     else:
#                         temp_record = record.values()[0]
#                         logger.info(temp_record)
#                         plan_id = temp_record['plan_id']
#                         order_list.append(temp_record['order'])
#                         record.delete()
#
#                 logger.info('删除操作完成，正在重新调整顺序')
#                 order_list.sort()
#                 if order_list:
#                     min_order_for_deleted = order_list[0]
#                     all_objects = db_class.objects.filter(plan_id=plan_id).filter(sub_node_num=0).filter(order__gt=min_order_for_deleted).order_by('order')
#                     for object in all_objects:
#                         object.order = min_order_for_deleted
#                         object.save()
#                         min_order_for_deleted = min_order_for_deleted + 1
#             return HttpResponse('success')
#         except Exception as e:
#             logger.error('%s' % e)
#             return HttpResponse('%s' % e)
#     except Exception as e:
#         logger.error('%s' % e)
#         return HttpResponse('%s' % e)