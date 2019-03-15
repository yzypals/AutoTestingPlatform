__author__ = 'laiyu'

import logging
import json
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Max
from django.db.models import Min
from django.db.models import F

from website.models import Sprint_tree
from website.models import Project_chosen
from website.models import Test_project_setting
from website.models import UI_project_setting
from website.models import API_project_setting
from website.models import Test_task_overview
from website.models import Test_task_detail
from website.models import Promble_feedback
from website.models import Browser_setting
from website.models import Database_setting
from website.models import Function_setting
from website.models import Operation_for_object
from website.models import Assertion_type_setting
from website.models import Global_variable_setting
from website.models import Page_tree
from website.models import UI_case_tree
from website.models import API_case_tree
from website.models import Page_element
from website.models import UI_test_case_step
from website.models import API_test_case_step
from website.models import UI_test_plan
from website.models import API_test_plan
from website.models import Running_plan
from website.models import UI_case_tree_test_plan
from website.models import API_case_tree_test_plan
from website.models import UI_test_report_for_summary
from website.models import API_test_report_for_summary
from website.models import UI_test_report_for_case
from website.models import API_test_report_for_case
from website.models import UI_test_report_for_case_step
from website.models import API_test_report_for_case_step


logger = logging.getLogger('mylogger')


# 获取上次选择的项目ID,用于展示树形结构，测试计划, 获取测试步骤页面元素所在页面等
def get_project_chosen(request):
    params = request.GET
    tree_type = params['treeType']
    if tree_type == 'SprintTree':
        db_class = Test_project_setting
    elif tree_type == 'PageTree' or tree_type == 'UICaseTree' or tree_type == 'PlanUICaseTree':
        db_class = UI_project_setting
    elif tree_type == 'APICaseTree' or tree_type == 'PlanAPICaseTree':
        db_class = API_project_setting
    try:
        record = Project_chosen.objects.filter(tree_type=tree_type).values()
        if record:
            response = {'result':'success', 'data':{"id":record[0]['project_id'], "projectName":record[0]['project_name']}}
        else: # 如果从没设置过，即没操作多下拉选择，切换项目，则从项目配置表取顺序最小的那个项目，作为默认项
            project = db_class.objects.all().order_by('order').values()
            if project:
                project = project[0]
                response = {'result':'success', 'data':{"id":project['id'], "projectName":project['project_name']}}
            else:
                response = {'result':'error', 'data':'请先新建测试项目'}
    except Exception as e:
        logger.error('%s' % e)
        response = {'result':'error', 'data':'%s' % e}
    finally:
        response = json.dumps(response)
        return HttpResponse(response)


# 存储上次选择的项目
def store_project_chosen(request):
    params = request.POST
    try:
        tree_type = params['treeType']
        project_id = params['projectID']
        project_name = params['projectName']
        record = Project_chosen.objects.filter(tree_type=tree_type)
        if record.exists(): #如果已经存在记录，则更新
            obj = record[0]
            obj.project_id = project_id
            obj.project_name = project_name
            obj.save()
        else: # 不存在，则新增
            obj = Project_chosen(project_id=project_id, project_name=project_name, tree_type=tree_type)
            obj.save()
        response = HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        response = HttpResponse('%s' % e)
    finally:
        return HttpResponse(response)

# 根据项目类型(测试项目|UI自动化项目|接口自动化项目)，获取对应的项目
def get_projects(request):
    project_list = []
    params = request.GET
    project_type = params['projectType']
    if project_type == 'TestProject':
        db_class = Test_project_setting
    elif project_type == 'UIProject':
        db_class = UI_project_setting
    elif project_type == 'APIProject':
        db_class = API_project_setting
    try:
        rows = db_class.objects.filter(valid_flag='启用').order_by('-order').values()
        for row in rows:
            temp_dic = {}
            temp_dic['id'] = str(row['id'])
            temp_dic['choice'] = row['project_name']
            project_list.append(temp_dic)
        response = {'result':'success', 'data':project_list}
    except Exception as e:
        logger.error('%s' % e)
        response = {'result':'error', 'data':'%s' % e}
    finally:
        response = json.dumps(response)
        return HttpResponse(response)

# 根据项目类型(测试项目|UI自动化项目|接口自动化项目)，项目ID，获取获取对应的测试计划
def get_plans(request):
    try:
        plan_list = []
        params = request.GET
        project_type = params['projectType']
        project_id = params['projectID']
        if project_type == 'UIProject':
            project_db_class = UI_project_setting
            plan_db_class = UI_test_plan
        elif project_type == 'APIProject':
            plan_db_class = API_test_plan
            project_db_class = API_project_setting

        if(project_db_class.objects.filter(valid_flag='启用').filter(id=project_id).exists()):
            rows = plan_db_class.objects.filter(project_id=project_id).filter(valid_flag='启用').order_by('-order').values()
            for row in rows:
                temp_dic = {}
                temp_dic['id'] = str(row['id'])
                temp_dic['choice'] = row['plan_name']
                plan_list.append(temp_dic)
            response = {'result':'success', 'data':plan_list}
        else:
            response = {'result':'error', 'data':'没有获取到同项目关联的计划'}
    except Exception as e:
        logger.error('%s' % e)
        response = {'result':'error', 'data':'%s' % e}
    finally:
        response = json.dumps(response)
        return HttpResponse(response)

# 获取节点树
def node_tree(request):
    node_list = [] # 用于存放所有节点
    params = request.GET
    tree_type = params['treeType']   # 获取树类型
    project_id = params['projectID'] # 获取项目ID

    if tree_type == 'SprintTree':
        db_class = Sprint_tree
    elif tree_type == 'PageTree':
        db_class = Page_tree
    elif tree_type == 'UICaseTree' or tree_type == 'PlanUICaseTree':
        db_class = UI_case_tree
    elif tree_type == 'APICaseTree' or tree_type == 'PlanAPICaseTree':
        db_class = API_case_tree

    #获取子节点
    def get_sub_node(node):
        node_id = node['id'] # 获取父节点的id
        node['children'] = [] # 用于存放子节点信息
        sub_nodes = db_class.objects.filter(parent_id=node_id).order_by('-order').values() # 获取父节点
        if sub_nodes: #如果存在子节点，遍历添加子节点
            for sub_node in sub_nodes:
                node['children'].append(sub_node)
                get_sub_node(sub_node)

    father_nodes = db_class.objects.filter(parent_id=0).filter(project_id=project_id).order_by('-order').values() # 获取所有一级节点
    for father_node in father_nodes:
        # logger.info(father_node)
        node_list.append(father_node)
        get_sub_node(father_node) # 获取子节点

    node_list = json.dumps(node_list)
    return HttpResponse(node_list, request)


#  修改节点名称
def update_tree_node_name(request):
    params = request.POST

    try:
        node_id = params['nodeID']
        node_name = params['nodeText']
        tree_type = params['treeType'] #获取树类型
        if tree_type == 'SprintTree':
            db_class = Sprint_tree
        elif tree_type == 'PageTree':
            db_class = Page_tree
        elif tree_type == 'UICaseTree':
            db_class = UI_case_tree
        elif tree_type == 'APICaseTree':
            db_class = API_case_tree

        node_obj = db_class.objects.get(id=node_id)
        node_obj.text = node_name
        node_obj.save()
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)


# 在节点树中增加节点
def append_tree_node(request):
    params = request.POST
    try:
        node_parent_id = params['nodeParentID']
        node_text = params['nodeText']
        state = params['state']
        iconcls = params['iconCls']
        attributes = params['attributes']
        tree_type = params['treeType'] # 获取树类型
        project_id = params['projectID']


        if tree_type == 'SprintTree':
            db_class = Sprint_tree
        elif tree_type == 'PageTree':
            db_class = Page_tree
        elif tree_type == 'UICaseTree':
            db_class = UI_case_tree
        elif tree_type == 'APICaseTree':
            db_class = API_case_tree

        sub_nodes = db_class.objects.filter(project_id=project_id).filter(parent_id=node_parent_id)
        if sub_nodes.exists():
            max_order = sub_nodes.aggregate(Max('order'))['order__max']
            order = max_order + 1
        else:
            order = 1

        node_obj = db_class(text=node_text, state=state, parent_id=node_parent_id, iconCls=iconcls, attributes=attributes, project_id=project_id, order=order)
        node_obj.save()
        # parent_node.save()
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)


# 移除节点树中的节点
def remove_tree_node(request):
    params = request.POST
    node_id = eval(params['nodeID'])
    parent_id = params['parentID']
    project_id = params['projectID']
    order = params['order']
    tree_type = params['treeType'] #获取树类型
    if tree_type == 'SprintTree':
        db_class = Sprint_tree
    elif tree_type == 'PageTree':
        db_class = Page_tree
    elif tree_type == 'UICaseTree':
        db_class = UI_case_tree
    elif tree_type == 'APICaseTree':
        db_class = API_case_tree

    def rm_node(node_id):
        try:
            with transaction.atomic():
                db_class.objects.filter(id=node_id).delete()
                nodes = db_class.objects.filter(parent_id=node_id)
                for node in nodes:
                    node_id = node.id
                    result = rm_node(node_id)
                    if not result[0]:
                        return [False,result[1]]
                return [True, '成功']
        except Exception as e:
            logger.error('delete node fail %s' % e)
            raise Exception('delete node fail %s' % e)

    try:
        with transaction.atomic():
            result = rm_node(node_id)
            # logger.debug(result)

            if result[0]:
                sibling_nodes = db_class.objects.filter(project_id=project_id).filter(parent_id=parent_id).filter(order__gt=order).order_by('order')
                if sibling_nodes.exists():
                    # logger.info('重新排序节点')
                    for node in sibling_nodes:
                        node.order = node.order - 1
                        node.save()
                return HttpResponse('success')
            else:
                return HttpResponse(result[1])
    except Exception as e:
        return HttpResponse('%s' % e)

# 拖动树节点
def drag_tree_node(request):
    try:
        parmas = request.POST
        parmas = eval(parmas['info'])

        target = parmas['target']
        source = parmas['source']
        operation = parmas['point']
        tree_type = parmas['treeType']

        if tree_type == 'SprintTree':
            db_class = Sprint_tree
        elif tree_type == 'PageTree':
            db_class = Page_tree
        elif tree_type == 'UICaseTree':
            db_class = UI_case_tree
        elif tree_type == 'APICaseTree':
            db_class = API_case_tree

        if operation == 'top' and target['parentID'] == 0:
            return HttpResponse('保存失败，只能有一个根节点节点')
        elif operation == 'top' and target['parentID'] != 0: # target节点之上
            # logger.info('正在重新排序节点')
            target_sibling_nodes = db_class.objects.filter(project_id=target['projectID']).filter(parent_id=target['parentID']).filter(order__gt=target['order']+1)
            for node in target_sibling_nodes:
                node.order = node.order + 1
                node.save()

            # logger.info('正在更新被拖拽节点的顺序')
            source_node = db_class.objects.filter(project_id=target['projectID']).get(id=source['id'])
            source_node.order = target['order'] + 1
            source_node.parent_id = target['parentID']
            source_node.save()
        elif operation == 'bottom' and target['parentID'] != 0: # target节点之下
            # logger.info('正在重新排序节点')
            target_sibling_nodes = db_class.objects.filter(project_id=target['projectID']).filter(parent_id=target['parentID']).filter(order__gte=target['order'])
            for node in target_sibling_nodes:
                node.order = node.order + 1
                node.save()

            # logger.info('正在更新被拖拽节点的顺序')
            source_node = db_class.objects.filter(project_id=target['projectID']).get(id=source['id'])
            source_node.order = target['order']
            source_node.parent_id = target['parentID']
            source_node.save()
        elif operation == 'append':
            target_sibling_nodes = db_class.objects.filter(project_id=target['projectID']).filter(parent_id=target['id'])
            if target_sibling_nodes.exists():
                max_order = target_sibling_nodes.aggregate(Max('order'))['order__max']
                order = max_order + 1
            else:
                order = 1
            source_node = db_class.objects.filter(project_id=target['projectID']).get(id=source['id'])
            source_node.order = order
            source_node.parent_id = target['id']
            source_node.save()
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)

# 复制节点树中叶子节点
def copy_tree_leaf_node(request):
    params = request.POST
    try:
        node_parent_id = params['nodeParentID']
        source_node_ID = params['sourceNodeID']
        node_text = params['nodeText']
        state = params['state']
        iconcls = params['iconCls']
        attributes = params['attributes']
        tree_type = params['treeType'] # 获取树类型
        project_id = params['projectID']


        if tree_type == 'UICaseTree':
            sub_nodes = UI_case_tree.objects.filter(project_id=project_id).filter(parent_id=node_parent_id)
            if sub_nodes.exists():
                max_order = sub_nodes.aggregate(Max('order'))['order__max']
                order = max_order + 1
            else:
                order = 1
            with transaction.atomic():
                # logger.info('正在复制基础用例信息')
                node_obj = UI_case_tree(text=node_text, state=state, parent_id=node_parent_id, iconCls=iconcls, attributes=attributes, project_id=project_id, order=order)
                node_obj.save()
                node_obje_id = node_obj.id

                # logger.info('正在复制用例步骤')
                sub_nodes = UI_test_case_step.objects.filter(case_id=source_node_ID).order_by('order')
                for sub_node in sub_nodes:
                    step_order = sub_node.order
                    status = sub_node.status
                    object_type = sub_node.object_type
                    page_name = sub_node.page_name
                    object = sub_node.object
                    exec_operation =  sub_node.exec_operation
                    input_params = sub_node.input_params
                    output_params = sub_node.output_params
                    assert_type = sub_node.assert_type
                    assert_pattern = sub_node.assert_pattern
                    run_times = sub_node.run_times
                    try_for_failure = sub_node.try_for_failure
                    object_id =  sub_node.object_id
                    case_id = node_obje_id

                    ui_case_step_obj = UI_test_case_step(order=step_order, status=status, object_type= object_type,object=object, exec_operation=exec_operation,
                                            input_params=input_params, output_params=output_params, assert_type=assert_type, assert_pattern=assert_pattern,
                                            run_times=run_times,try_for_failure=try_for_failure,page_name=page_name,case_id=case_id, object_id=object_id)
                    ui_case_step_obj.save()
        elif tree_type == 'APICaseTree':
            sub_nodes = API_case_tree.objects.filter(project_id=project_id).filter(parent_id=node_parent_id)
            if sub_nodes.exists():
                max_order = sub_nodes.aggregate(Max('order'))['order__max']
                order = max_order + 1
            else:
                order = 1

            with transaction.atomic():
                # logger.info('正在复制基础用例信息')
                node_obj = API_case_tree(text=node_text, state=state, parent_id=node_parent_id, iconCls=iconcls, attributes=attributes, project_id=project_id, order=order)
                node_obj.save()
                node_obje_id = node_obj.id

                # logger.info('正在复制用例步骤')
                sub_nodes = API_test_case_step.objects.filter(case_id=source_node_ID).order_by('order')
                for sub_node in sub_nodes:
                    step_order = sub_node.order
                    status = sub_node.status
                    step_type = sub_node.step_type
                    op_object = sub_node.op_object
                    object_id =  sub_node.object_id
                    exec_operation = sub_node.exec_operation
                    request_header = sub_node.request_header
                    request_method = sub_node.request_method
                    url_or_sql = sub_node.url_or_sql
                    input_params = sub_node.input_params
                    response_to_check = sub_node.response_to_check
                    check_rule = sub_node.check_rule
                    check_pattern = sub_node.check_pattern
                    output_params = sub_node.output_params
                    protocol = sub_node.protocol
                    host = sub_node.host
                    port = sub_node.port
                    run_times = sub_node.run_times
                    try_for_failure = sub_node.try_for_failure
                    case_id = node_obje_id

                    case_step_obj = API_test_case_step(order=step_order, status=status, step_type=step_type,op_object=op_object, object_id=object_id,exec_operation=exec_operation,
                                        request_header=request_header, request_method=request_method, url_or_sql=url_or_sql, input_params=input_params,
                                        response_to_check=response_to_check,check_rule=check_rule,check_pattern=check_pattern, output_params=output_params,
                                        protocol=protocol, host=host, port=port, run_times=run_times, try_for_failure=try_for_failure, case_id=case_id)
                    case_step_obj.save()
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)

# 删除datagrid中所选记录
def remove_row(request):
    try:
        params = request.POST

        row_ids = eval(params['rowIDs'])
        class_name = params['datagridID']
        order_list = []  # 存放被删除记录的顺序
        db_class = globals()[class_name]

        db_class_list  = ['UI_test_report_for_summary', 'UI_test_report_for_case', 'UI_test_report_for_case_step',
                              'API_test_report_for_summary', 'API_test_report_for_case', 'API_test_report_for_case_step',
                          'API_case_tree_test_plan', 'UI_case_tree_test_plan']

        if class_name not in db_class_list:
            try:
                with transaction.atomic():
                    for row_id in row_ids:
                        row_id = int(row_id)
                        record = db_class.objects.filter(id=row_id)
                        if not record.exists():
                            # logger.error('error, ID(%s)不存在' % row_id)
                            continue
                        else:
                            order_list.append(record.values()[0]['order'])
                            record.delete()

                    # logger.info('删除操作完成，正在重新调整顺序')
                    order_list.sort()
                    if order_list:
                        min_order_for_deleted = order_list[0]
                        all_objects = db_class.objects.filter(order__gt=min_order_for_deleted).order_by('order')

                        for object in all_objects:
                            object.order = min_order_for_deleted
                            object.save()
                            min_order_for_deleted = min_order_for_deleted + 1

                return HttpResponse('success')
            except Exception as e:
                    logger.error('%s' % e)
                    return HttpResponse('%s' % e)
        else:
            try:
                for row_id in row_ids:
                    row_id = int(row_id)
                    record = db_class.objects.filter(id=row_id)
                    if not record.exists():
                        # logger.error('error, ID(%s)不存在' % row_id)
                        continue
                    else:
                        record.delete()
                return HttpResponse('success')
            except Exception as e:
                logger.error('%s' % e)
                return HttpResponse('%s' % e)
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)


# 上移|下移datagrid中的行记录
def move_row(request):
    params = request.POST

    order_dic = json.loads(params['orderDic'])
    class_name = params['datagridID']
    db_class = globals()[class_name]
    try:
        with transaction.atomic():
            for id, order in order_dic.items():
                obj = db_class.objects.get(id=id)
                obj.order = order
                obj.save()
        return  HttpResponse('success')
    except Exception as e:
        reason = '%s' % e
        return HttpResponse(reason)

#
# # 置顶、置底datagrid中的行记录
# def put_row_top_or_bottom(request):
#     params = request.POST
#     class_name = params['datagridID']
#     db_class = globals()[class_name]
#     plan_id = params['planID']
#     row_id = params['rowID']
#     direction = params['direction']
#
#     try:
#         case = db_class.objects.get(id=row_id)
#         if direction == 'top':
#             min_order = db_class.objects.filter(plan_id = plan_id).filter(sub_node_num=0).aggregate(Min('order'))['order__min']
#             if case.order == min_order:
#                 return HttpResponse('AlreadyTop')
#             else:
#                 case.order = min_order - 1
#                 case.save()
#         elif direction == 'bottom':
#             max_order = db_class.objects.filter(plan_id = plan_id).filter(sub_node_num=0).aggregate(Max('order'))['order__max']
#             if max_order ==  case.order:
#                 return HttpResponse('AlreadyBottom')
#             else:
#                 case.order = max_order + 1
#                 case.save()
#         else:
#             return HttpResponse('参数错误')
#
#         return HttpResponse('success')
#     except Exception as e:
#         return HttpResponse('%s' % e)

#
# # 重新调整datagrid中的记录的顺序值
# def reorder_rows(request):
#     params = request.POST
#     class_name = params['datagridID']
#     db_class = globals()[class_name]
#     plan_id = params['planID']
#     logger.info(plan_id)
#     logger.info(db_class)
#     try:
#         with transaction.atomic():
#             min_order = 1
#             all_objects = db_class.objects.filter(plan_id=plan_id).filter(sub_node_num=0).order_by('order')
#             for object in all_objects:
#                 object.order = min_order
#                 object.save()
#                 min_order = min_order + 1
#         return HttpResponse('success')
#     except Exception as e:
#         return HttpResponse('%s' % e)

# 拖拽表格中的记录行（针对测试计划用例视图表）
def drag_row_of_testplan_case_view(request):
    try:
        params = request.POST
        class_name = params['datagridID']
        db_class = globals()[class_name]
        plan_id = params['planID']

        # target_row_id = params['targetRowID']
        target_row_order = params['targetRowOrder']

        source_row_id = params['sourceRowID']
        source_row_order = params['sourceRowOrder']

        direction = params['direction']


        with transaction.atomic():

            if direction == 'top':
                if source_row_order > target_row_order:  # 从下往上拖动，拖动至目标行记录上方     # target_row_order <= order < source_row_order 的记录，order + 1
                    db_class.objects.filter(plan_id=plan_id, sub_node_num=0).filter(order__gte=target_row_order).filter(order__lt=source_row_order).update(order=F('order') + 1)

                    source_row = db_class.objects.get(id=source_row_id)
                    source_row.order = target_row_order
                    source_row.save()
                else:   # 从上往下拖动，拖动至目标行记录上方    # source_row_order < order < target_row_order 的记录，order - 1
                    db_class.objects.filter(plan_id=plan_id, sub_node_num=0).filter(order__gt=source_row_order).filter(order__lt=target_row_order).update(order=F('order') - 1)

                    source_row = db_class.objects.get(id=source_row_id)
                    source_row.order = int(target_row_order) - 1
                    source_row.save()
            elif direction == 'bottom':
                if source_row_order > target_row_order: # 从下往上拖动，拖动至目标行记录下方    # target_row_order < order < source_row_order 的记录，order + 1
                    db_class.objects.filter(plan_id=plan_id, sub_node_num=0).filter(order__gt=target_row_order).filter(order__lt=source_row_order).update(order=F('order') + 1)

                    source_row = db_class.objects.get(id=source_row_id)
                    source_row.order = int(target_row_order) + 1
                    source_row.save()
                else:  # 从上往下拖动，拖动至目标行记录下方     # source_row_order < order <= target_row_order 的记录，order - 1
                    db_class.objects.filter(plan_id=plan_id, sub_node_num=0).filter(order__gt=source_row_order).filter(order__lte=target_row_order).update(order=F('order') - 1)

                    source_row = db_class.objects.get(id=source_row_id)
                    source_row.order = target_row_order
                    source_row.save()

        return HttpResponse('success')
    except Exception as e:
        return HttpResponse('%s' % e)


# 拖拽表格中的记录行（针对测试用例步骤表）
def drag_row_of_testcase_step(request):
    try:
        params = request.POST
        class_name = params['datagridID']
        db_class = globals()[class_name]
        case_id = params['caseID']

        # target_row_id = params['targetRowID']
        target_row_order = params['targetRowOrder']

        source_row_id = params['sourceRowID']
        source_row_order = params['sourceRowOrder']

        direction = params['direction']


        with transaction.atomic():
            if direction == 'top':
                if source_row_order < target_row_order:  # 从下往上拖动，拖动至目标行记录上方     # source_row_order < order <= target_row_order 的记录，order - 1
                    db_class.objects.filter(case_id=case_id).filter(order__lte=target_row_order).filter(order__gt=source_row_order).update(order=F('order') - 1)

                    source_row = db_class.objects.get(id=source_row_id)
                    source_row.order = target_row_order
                    source_row.save()
                else:   # 从上往下拖动，拖动至目标行记录上方    # target_row_order < order < source_row_order 的记录，order + 1
                    db_class.objects.filter(case_id=case_id).filter(order__gt=target_row_order).filter(order__lt=source_row_order).update(order=F('order') + 1)

                    source_row = db_class.objects.get(id=source_row_id)
                    source_row.order = int(target_row_order) + 1
                    source_row.save()
            elif direction == 'bottom':
                if source_row_order < target_row_order: # 从下往上拖动，拖动至目标行记录下方    # source_row_order < order < target_row_order 的记录，order - 1
                    db_class.objects.filter(case_id=case_id).filter(order__gt=source_row_order).filter(order__lt=target_row_order).update(order=F('order') - 1)

                    source_row = db_class.objects.get(id=source_row_id)
                    source_row.order = int(target_row_order) - 1
                    source_row.save()
                else:  # 从上往下拖动，拖动至目标行记录下方     # target_row_order =< order <= source_row_order 的记录，order + 1
                    db_class.objects.filter(case_id=case_id).filter(order__lt=source_row_order).filter(order__gte=target_row_order).update(order=F('order') + 1)
                    source_row = db_class.objects.get(id=source_row_id)
                    source_row.order = target_row_order
                    source_row.save()

        return HttpResponse('success')
    except Exception as e:
        return HttpResponse('%s' % e)