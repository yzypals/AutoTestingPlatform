from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import  Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from website.models import UI_test_report_for_case
from website.models import API_test_report_for_case

import json
import logging
from itertools import chain


logger = logging.getLogger('mylogger')

# 测试报告-测试概况-操作|查看详情
def test_report_cases_view(request):
    if request.GET['reportType'] == 'UITestReport':
        template = loader.get_template('website/pages/UITestReportCasesView.html')
    elif request.GET['reportType'] == 'APITestReport':
        template = loader.get_template('website/pages/APITestReportCasesView.html')
    return HttpResponse(template.render({}, request))


# 查看用例-列表数据
def get_test_report_cases(request):
    griddata = {"total": 0, "rows": []}
    rows = [] # 用于存储记录行

    report_type = request.GET.get('reportType')
    if report_type == 'APITestReport':
        db_class = API_test_report_for_case
    elif report_type == 'UITestReport':
        db_class = UI_test_report_for_case

    execution_num = request.GET['executionNum']
    plan_id = request.GET['planID']
    # 获取总记录数
    records = []
    records_fail = db_class.objects.filter(execution_num=execution_num).filter(plan_id=plan_id).filter(Q(run_result='失败')|Q(run_result='阻塞')).order_by('id').values()
    records_success = db_class.objects.filter(execution_num=execution_num).filter(plan_id=plan_id).filter(run_result='成功').order_by('id').values()

    records.extend(records_fail)
    records.extend(records_success)

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

