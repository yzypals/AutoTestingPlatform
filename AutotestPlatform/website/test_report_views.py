from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

import json
import logging
from django.core.paginator import  Paginator, PageNotAnInteger, EmptyPage
from website.models import UI_test_report_for_summary
from website.models import API_test_report_for_summary

logger = logging.getLogger('mylogger')


# 测试报告-UI测试报告
def ui_test_report(request):
    template = loader.get_template('website/pages/UITestReport.html')
    return HttpResponse(template.render({}, request))

def api_test_report(request):
    template = loader.get_template('website/pages/APITestReport.html')
    return HttpResponse(template.render({}, request))

# # 列表数据
def get_test_report_for_summary(request):
    grid_data = {"total": 0, "rows": []}
    rows = [] # 用于存储记录行

    report_type = request.GET.get('reportType')
    if report_type == 'APITestReport':
        db_class = API_test_report_for_summary
    elif report_type == 'UITestReport':
        db_class = UI_test_report_for_summary

    # 获取总记录数
    records = db_class.objects.order_by('-id').values()
    grid_data["total"] = len(records)

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

    records = page.object_list
    for record in records:
        rows.append(record)
    grid_data["rows"] =  rows
    grid_data = json.dumps(grid_data)
    return HttpResponse(grid_data)


