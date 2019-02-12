from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

import json
import logging
from django.core.paginator import  Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Max
from django.db import transaction

from website.models import Page_element
from website.models import UI_test_case_step
from website.models import Page_tree

logger = logging.getLogger('mylogger')

# 页面管理-页面元素管理
def page_element_manager(request):
    template = loader.get_template('website/pages/pageElementManager.html')
    return HttpResponse(template.render({}, request))

# 点击页面树节点，打开对应页面
def page_tree_node_page(request):
    template = loader.get_template('website/pages/pageTreeNodePage.html')
    return HttpResponse(template.render({}, request))

# # 点击页面树节点，打开对应页面，对应的列表数据
def get_page_elements(request):
    griddata = {"total": 0, "rows": []}
    rows = [] # 用于存储记录行

    page_id = request.GET['nodeID']

    try:
        # 获取总记录数
        elements = Page_element.objects.filter(page_id=page_id).order_by('-order').values()
        griddata["total"] = len(elements)

        page_num = request.GET.get('page') # 记录请求的是第几页数据
        rows_num = request.GET.get('rows') # 记录请求每页的记录数

        paginator = Paginator(elements, rows_num) # 设置每页展示的数据

        try:
            page = paginator.page(page_num)
        except PageNotAnInteger as e: # 如果请求的页面编号不存在，返回第一页数据
            logger.warn('%s' % e)
            page = paginator.page(1)
        except EmptyPage as e: # 如果请求页面，超出页面范围，返回最后一页数据
            logger.warn('%s' % e)
            page = paginator.page(paginator.num_pages)

        elements = page.object_list
        for element in elements:
            del element['page_id']
            rows.append(element)
        griddata["rows"] =  rows
        griddata = json.dumps(griddata)
        return HttpResponse(griddata)
    except Exception as e:
        logger.error('%s' % e)
        return  HttpResponse('%s' % e)

# 在页面元素管理页面中增加页面元素
def add_page_element(request):
    try:
        params = request.POST
        element_name = params['elementName']
        selector1 = params['selector1']
        selector2 = params['selector2']
        order = params['order']
        page_id = params['node_id']

        if element_name == '':
            logger.error('保存元素失败，元素名称不能为空')
            return HttpResponse('error')
        elif selector1 == '':
            logger.error('保存元素失败，选择器1不能为空')
            return HttpResponse('error')

        if order == '': # 如果无顺序，表明是新增
            all_objects = Page_element.objects.filter(page_id=page_id)
            if all_objects.exists():
                max_order = all_objects.aggregate(Max('order'))['order__max']
                order = max_order + 1
            else:
                order = 1
            element_obj = Page_element(element_name=element_name, selector1=selector1, selector2=selector2, order=order, page_id=page_id)
            element_obj.save()
        else: #表明是插入
            # logger.info('即将插入新记录，正在调整记录的顺序') # 插入记录所在行下方的记录都减去1
            try:
                with transaction.atomic():
                    all_objects = Page_element.objects.filter(page_id=page_id).filter(order__gte=order)
                    for object in all_objects:
                        object.order = object.order + 1
                        object.save()
                    element_obj = Page_element(element_name=element_name, selector1=selector1, selector2=selector2, order=order, page_id=page_id)
                    element_obj.save()
            except Exception as e:
                logger.error('%s' % e)
                return  HttpResponse('%s' % e)
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return  HttpResponse('%s' % e)


#
# # 用例步骤中选择“对象类型”为用例时时，请求获取该页面所有的用例
# def get_cases_for_page_selected(request):
#     try:
#         params = request.GET
#         project_id = params['projectID']
#         project_type = params['projectType']
#         page_id = params['pageID']
#         current_case_id = params['caseID'] # 正在编辑的步骤归属的用例ID
#         if project_type == 'API':
#             db_class = API_case_tree
#         elif project_type == 'UI':
#             db_class = UI_case_tree
#
#         temp_var = ''
#         def find_case_fullpath(case):
#             nonlocal  temp_var
#             if  case.parent_id !=0: # 存在上级页面
#                 father_node = db_class.objects.get(id = case.parent_id)
#                 temp_var = find_case_fullpath(father_node) + '->' + father_node.text
#                 return temp_var
#             else:
#                 return temp_var
#
#
#         case_list = []
#         cases = db_class.objects.filter(project_id=project_id).filter(parent_id=page_id).exclude(id=current_case_id).all()
#
#         for case in cases:
#             case_id = case.id
#             if db_class.objects.filter(parent_id=case_id).exists():# 非用例，为模块名称
#                 continue
#             else:
#                 temp_dic = {}
#                 temp_dic['id'] = str(case_id)
#                 # temp_dic['choice'] = (find_case_fullpath(case) + '->' + case.text).lstrip('->')
#                 temp_dic['choice'] = case.text
#                 # temp_var = ''
#                 case_list.append(temp_dic)
#         response = {'result':'success', 'choices':case_list}
#         response = json.dumps(response)
#         return HttpResponse(response)
#     except Exception as e:
#         logger.error('%s' % e)
#         response = {'result':'error', 'choices':'%s' % e}
#         response = json.dumps(response)
#         return HttpResponse(response)

# 在页面元素管理页面中修改页面元素
def update_page_element(request):
    try:
        params = request.POST
        id = params['id']
        element_name = params['elementName']
        selector1 = params['selector1']
        selector2 = params['selector2']

        if element_name == '':
            # logger.error('保存元素失败，元素名称不能为空')
            return HttpResponse('error')
        elif selector1 == '':
            # logger.error('保存元素失败，选择器1不能为空')
            return HttpResponse('error')

        element_obj = Page_element.objects.get(id=id)
        element_obj.element_name = element_name
        element_obj.selector1 = selector1
        element_obj.selector2 = selector2
        element_obj.save()

        # logger.info('同步更新UI测试用例详情表')
        obj_list = UI_test_case_step.objects.filter(object_id=id).filter(object_type='页面元素')
        for obj in obj_list:
            obj.object = element_name
            obj.save()
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return  HttpResponse('%s' % e)


# 删除用例步骤
def remove_page_element(request):
    try:
        params = request.POST
        row_ids = eval(params['rowIDs'])
        class_name = params['datagridID']

        order_list = []  # 存放被删除记录的顺序
        db_class = globals()[class_name]

        try:
            with transaction.atomic():
                for row_id in row_ids:
                    row_id = int(row_id)
                    record = db_class.objects.filter(id=row_id)
                    if not record.exists():
                        # logger.error('error, ID(%s)不存在' % row_id)
                        continue
                    else:
                        temp_record = record.values()[0]
                        page_id = temp_record['page_id']
                        order_list.append(temp_record['order'])
                        record.delete()

                # logger.info('删除操作完成，正在重新调整顺序')
                order_list.sort()
                if order_list:
                    min_order_for_deleted = order_list[0]
                    all_objects = db_class.objects.filter(page_id=page_id).filter(order__gt=min_order_for_deleted).order_by('order')

                    for object in all_objects:
                        object.order = min_order_for_deleted
                        object.save()
                        min_order_for_deleted = min_order_for_deleted + 1
            return HttpResponse('success')
        except Exception as e:
            logger.error('%s' % e)
            return HttpResponse('%s' % e)
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)