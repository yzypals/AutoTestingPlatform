from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

import json
import logging
import time
from datetime import datetime
import re
from django.core.paginator import  Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Max
from django.db import transaction

from website.models import Test_task_overview
from website.models import Test_task_detail

logger = logging.getLogger('mylogger')

# 测试管理-测试任务管理
def test_task_manager(request):
    template = loader.get_template('website/pages/testTaskManager.html')
    return HttpResponse(template.render({}, request))

# 任务概况
def test_task_overview(request):
    template = loader.get_template('website/pages/testTaskOverview.html')
    return HttpResponse(template.render({}, request))

# 任务明细
def test_task_detail(request):
    template = loader.get_template('website/pages/testTaskDetail.html')
    return HttpResponse(template.render({}, request))


# # 点击迭代树 任务概况 节点，打开对应页面的对应的列表数据
def load_test_tasks(request):
    grid_data = {"total": 0, "rows": []}
    rows = [] # 用于存储记录行

    try:
        params = request.GET
        tree_node_id = params['nodeID']
        task_type = params['taskType']
        if task_type == 'overview':
            db_class = Test_task_overview
        elif task_type == 'detail':
            db_class = Test_task_detail
        # 获取总记录数
        test_tasks = db_class.objects.filter(page_id=tree_node_id).order_by('-order').values()
        grid_data["total"] = len(test_tasks)

        page_num = request.GET.get('page') # 记录请求的是第几页数据
        rows_num = request.GET.get('rows') # 记录请求每页的记录数

        paginator = Paginator(test_tasks, rows_num) # 设置每页展示的数据
        try:
            page = paginator.page(page_num)
        except PageNotAnInteger as e: # 如果请求的页面编号不存在，返回第一页数据
            logger.warn('%s' % e)
            page = paginator.page(1)
        except EmptyPage as e: # 如果请求页面，超出页面范围，返回最后一页数据
            logger.warn('%s' % e)
            page = paginator.page(paginator.num_pages)

        test_tasks = page.object_list
        for test_task in test_tasks:
            rows.append(test_task)
        grid_data["rows"] =  rows
        grid_data = json.dumps(grid_data)
        return HttpResponse(grid_data)
    except Exception as e:
        return HttpResponse('%s' % e)


# # 增加任务明细
def add_test_detail_task(request):
    try:
        params = request.POST
        module = params['module']
        requirement = params['requirement']
        person_in_charge = params['person_in_charge']
        sub_task = params['sub_task']
        time_took = params['time_took']
        deadline = params['deadline']
        remark = params['remark']
        order =  params['order']
        page_id = params['node_id']

        progress = '0%'
        finish_time = ''  # 实际完成时间
        if_delay = ''    # 是否超时
        history_progress = '0%' #历史进度

        if requirement == '':
            return HttpResponse('保存失败，需求名称不能为空')
        if deadline == '':
            return HttpResponse('保存失败，预计截止时间不能为空')

        if order == '': # 如果无顺序，表明是新增
            all_objects = Test_task_detail.objects.filter(page_id=page_id)
            if all_objects.exists():
                max_order = all_objects.aggregate(Max('order'))['order__max']
                order = max_order + 1
            else:
                order = 1
            test_task_obj = Test_task_detail(module=module, requirement=requirement, person_in_charge=person_in_charge, sub_task=sub_task,
                                      progress=progress, time_took=time_took, deadline=deadline, finish_time=finish_time, remark=remark,
                                      if_delay=if_delay, history_progress=history_progress, order=order, page_id=page_id)
            test_task_obj.save()
        else: #表明是插入
            # logger.info('即将插入新记录，正在调整记录的顺序') # 插入记录所在行下方的记录都减去1
            try:
                with transaction.atomic():
                    all_objects = Test_task_detail.objects.filter(page_id=page_id).filter(order__gte=order)
                    for object in all_objects:
                        object.order = object.order + 1
                        object.save()

                    test_task_obj = Test_task_detail(module=module, requirement=requirement, person_in_charge=person_in_charge, sub_task=sub_task,
                                              progress=progress, time_took=time_took, deadline=deadline, finish_time=finish_time, remark=remark,
                                              if_delay=if_delay, history_progress=history_progress, order=order, page_id=page_id)
                    test_task_obj.save()
            except Exception as e:
                logger.error('%s' % e)
                return HttpResponse('%s' % e)
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)


# # 任务概要页面中增加任务概要
def add_test_overview_task(request):
    try:
        params = request.POST

        module = params['module']
        progress = params['progress']
        requirement = params['requirement']
        sub_task = params['sub_task']
        time_for_test = params['time_for_test']
        real_time_for_test = params['real_time_for_test']
        developer_in_charge = params['developer_in_charge']
        tester_in_charge = params['tester_in_charge']
        pm_in_charge = params['pm_in_charge']
        mark = params['mark']
        order =  params['order']
        page_id = params['node_id']


        if progress and progress.isdigit():
            progress = progress + '%'
        else:
            progress = '未完成'

        if time_for_test:
            time_for_test_bak = time_for_test.split(' ')[0]
            time_for_test_bak = time.mktime(datetime.strptime(time_for_test_bak, '%Y-%m-%d').timetuple())
        if real_time_for_test:
            real_time_for_test_bak = real_time_for_test.split(' ')[0]
            real_time_for_test_bak = time.mktime(datetime.strptime(real_time_for_test_bak, '%Y-%m-%d').timetuple())
        if time_for_test_bak < real_time_for_test_bak:
            if_delay  = '是'
        else:
            if_delay = '否'

        if requirement == '':
            # logger.error('保存失败，需求名称不能为空')
            return HttpResponse('保存失败，需求名称不能为空')

        if order == '': # 如果无顺序，表明是新增
            all_objects = Test_task_overview.objects.filter(page_id=page_id)
            if all_objects.exists():
                max_order = all_objects.aggregate(Max('order'))['order__max']
                order = max_order + 1
            else:
                order = 1
        else: #表明是插入
            # logger.info('即将插入新记录，正在调整记录的顺序')
            all_objects = Test_task_overview.objects.filter(page_id=page_id).filter(order__gte=order)
            for object in all_objects:
                object.order = object.order + 1
                object.save()

        test_task_obj = Test_task_overview(module=module, progress=progress, requirement=requirement, sub_task=sub_task, time_for_test=time_for_test,
                                  real_time_for_test=real_time_for_test, developer_in_charge=developer_in_charge,tester_in_charge=tester_in_charge,
                                  pm_in_charge=pm_in_charge, mark=mark, order=order, page_id=page_id,if_delay=if_delay)

        # logger.info('同步更新有相同需求任务行的模块名称，进度')
        all_objects = Test_task_overview.objects.filter(page_id=page_id).filter(requirement=requirement)
        for item in all_objects:
            item.progress = progress
            item.module = module
            item.save()
        test_task_obj.save()

        all_objects = Test_task_detail.objects.filter(page_id=page_id)
        if not all_objects.filter(requirement=requirement).exists() : # 如果明细任务中没该需求任务，则插入
            if all_objects.exists():
                max_order = all_objects.aggregate(Max('order'))['order__max']
                order = max_order + 1
            else:
                order = 1

            test_task_obj = Test_task_detail(module=module, requirement=requirement, person_in_charge=tester_in_charge, sub_task='功能测试',
                                  progress='0%', time_took='', deadline='', finish_time='', remark='',
                                  if_delay='', history_progress='0%', order=order, page_id=page_id)

            test_task_obj.save()
        return  HttpResponse('success')
    except Exception as e:
        transaction.rollback()
        logger.error('%s' % e)
        return HttpResponse('%s' % e)

# 在 任务明细 管理页面中修改任务明细
def update_test_detail_task(request):
    try:
        params = request.POST

        id = params['id']
        module = params['module']
        requirement = params['requirement']
        person_in_charge = params['person_in_charge']
        sub_task = params['sub_task']
        progress = params['progress']
        time_took = params['time_took']
        deadline = params['deadline']
        remark = params['remark']
        page_id = params['node_id']
        if requirement == '':
            return HttpResponse('保存失败，需求名称不能为空')
        if deadline == '':
            return HttpResponse('保存失败，预计截止时间不能为空')
        if progress == '':
            return HttpResponse('保存失败，进度不能为空')
        elif progress[len(progress)-1] == '%':
            if  not progress[0:len(progress)-1].isdigit():
                return HttpResponse('保存失败，进度只能为数字')
        elif not progress.isdigit():
            return HttpResponse('保存失败，进度只能为数字')
        else:
            progress = progress + '%'

        if progress == '100%':
            finish_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            milliseconds_for_deadline = time.mktime(datetime.strptime(deadline.split(' ')[0], '%Y-%m-%d').timetuple())
            milliseconds_for_finish_time = time.mktime(datetime.strptime(finish_time.split(' ')[0], '%Y-%m-%d').timetuple())
            if milliseconds_for_finish_time <= milliseconds_for_deadline:
                if_delay = '否'
            else:
                if_delay = '是'
        else:
            finish_time = ''
            if_delay = ''

        test_task_obj = Test_task_detail.objects.get(id=id)
        requirement_old = test_task_obj.requirement
        test_task_obj.module = module
        test_task_obj.requirement = requirement
        test_task_obj.person_in_charge = person_in_charge
        test_task_obj.progress = progress
        test_task_obj.sub_task = sub_task
        test_task_obj.time_took = time_took
        test_task_obj.deadline = deadline
        test_task_obj.finish_time = finish_time
        test_task_obj.if_delay = if_delay
        test_task_obj.remark = remark

        today = time.strftime('%m.%d.%Y',time.localtime(time.time()))
        date = datetime.strptime(today, '%m.%d.%Y')
        weekday = str(date.weekday())
        weekday_dic = {"0": "周一", "1":"周二", "2":"周三", "3":"周四", "4":"周五", "5":"周六"}
        history_progress = weekday_dic[weekday] + '(' + today[0:len(today)-5] + ')' + ':' + progress
        pattern = weekday_dic[weekday] + '\(' + today[0:len(today)-5] + '\)' + ':[\d]+%$'

        result = re.findall(pattern, test_task_obj.history_progress) # 如果同一天多次更新进度，则覆盖之前的进度
        if result:
            test_task_obj.history_progress = test_task_obj.history_progress.replace(result[0], history_progress)
        else:
            if progress != '0%':
                test_task_obj.history_progress = (test_task_obj.history_progress + '>' + history_progress).lstrip('>')

        test_task_obj.save()

        # logger.info('同步相同需求任务的需求任务名，测试负责人')
        all_objects = Test_task_detail.objects.filter(page_id=page_id).filter(requirement=requirement_old)
        for item in all_objects:
            item.requirement = requirement
            item.person_in_charge = person_in_charge
            item.save()

        tasks_progress = '100%'
        all_objects = Test_task_detail.objects.filter(page_id=page_id).filter(requirement=requirement)
        for item in all_objects:
            if item.progress != '100%':
                tasks_progress = '未完成'
                break

        # logger.info('修改任务明细，同步更新任务概要表的需求任务名，是否完成')
        requirements =  Test_task_overview.objects.filter(page_id=page_id).filter(requirement = requirement_old)
        for item in requirements:
            item.requirement = requirement
            item.progress = tasks_progress
            item.save()
        return  HttpResponse('success')
    except Exception as e:
        transaction.rollback()
        logger.error('%s' % e)
        return HttpResponse('%s' % e)


# 在 任务概要 管理页面中修改任务概要
def update_test_overview_task(request):
    try:
        params = request.POST

        id = params['id']
        page_id = params['node_id']
        module = params['module']
        progress = params['progress']
        if progress == '':
            progress = '未完成'
        elif progress and progress.isdigit():
            progress = progress + '%'
        requirement = params['requirement']
        sub_task = params['sub_task']
        time_for_test = params['time_for_test']
        real_time_for_test = params['real_time_for_test']
        developer_in_charge = params['developer_in_charge']
        tester_in_charge = params['tester_in_charge']
        pm_in_charge = params['pm_in_charge']
        mark = params['mark']
        if requirement == '':
            # logger.error('保存失败，需求名称不能为空')
            return HttpResponse('保存失败，需求名称不能为空')

        test_task_obj = Test_task_overview.objects.get(id=id)
        requirement_old = test_task_obj.requirement
        test_task_obj.module = module
        test_task_obj.progress = progress
        test_task_obj.requirement = requirement
        test_task_obj.sub_task = sub_task
        test_task_obj.time_for_test = time_for_test
        test_task_obj.real_time_for_test = real_time_for_test
        test_task_obj.developer_in_charge = developer_in_charge
        test_task_obj.tester_in_charge = tester_in_charge
        test_task_obj.pm_in_charge = pm_in_charge
        test_task_obj.mark = mark

        if time_for_test and real_time_for_test:
            time_for_test = time_for_test.split(' ')[0]
            time_for_test = time.mktime(datetime.strptime(time_for_test, '%Y-%m-%d').timetuple())
            real_time_for_test = real_time_for_test.split(' ')[0]
            real_time_for_test = time.mktime(datetime.strptime(real_time_for_test, '%Y-%m-%d').timetuple())
            if time_for_test < real_time_for_test:
                test_task_obj.if_delay  = '是'
            else:
                test_task_obj.if_delay = '否'

        # logger.info('同步相同需求任务的模块名称，进度，需求任务名称')
        all_objects = Test_task_overview.objects.filter(page_id=page_id).filter(requirement=requirement_old)
        for item in all_objects:
            item.requirement = requirement
            item.progress = progress
            item.module = module
            item.save()

        test_task_obj.save()

        # logger.info('更新任务概要，同步更新任务明细表的需求任务名,模块名称')
        requirements =  Test_task_detail.objects.filter(page_id=page_id).filter(requirement = requirement_old)
        for i in requirements:
            i.requirement = requirement
            i.module = module
            i.save()
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)


# 删除用例步骤
def remove_task(request):
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