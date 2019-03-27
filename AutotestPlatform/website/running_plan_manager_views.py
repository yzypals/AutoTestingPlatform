from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import  Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Max
from django.db import transaction

import json
import logging
import os
import time
import threading

from website.models import Running_plan

logger = logging.getLogger('mylogger')


# 运行计划管理
def running_plan_manager(request):
    template = loader.get_template('website/pages/runningPlanManager.html')
    return HttpResponse(template.render({}, request))

# # 运行计划列表数据
def get_running_plans(request):
    grid_data = {"total": 0, "rows": []}
    rows = [] # 用于存储记录行

    try:
        # 获取总记录数
        records = Running_plan.objects.all().order_by('-order').values()
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
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)


# 增加运行计划
def add_running_plan(request):
    try:
        params = request.POST

        running_plan_num = int(time.time())
        running_plan_name = params['running_plan_name']
        project_type = params['project_type']
        project_id =  params['project_id']
        project_name = params['project_name']
        # for item in plan_id[:]:
        #     if type(item) == type('') and not item.isdigit():
        #         plan_id.remove(item)
        plan_id = params['plan_id']
        plan_name = params['plan_name']
        script_dirpath = params['script_dirpath'].strip()
        python_path = params['python_path'].strip()
        running_status = '未执行'
        valid_flag = params['valid_flag']
        order = params['order']

        if running_plan_name == '':
            return  HttpResponse('保存失败，运行计划名称不能为空')
        if project_type == '':
            return  HttpResponse('保存失败，项目类型不能为空')
        if project_id == '':
            return  HttpResponse('保存失败，项目ID不能为空')
        if project_name == '':
            return  HttpResponse('保存失败，项目名称不能为空')
        if not plan_id:
            return  HttpResponse('保存失败，计划id不能为空')
        if plan_name == '':
            return  HttpResponse('保存失败，计划名称不能为空')
        if script_dirpath == '':
            return  HttpResponse('保存失败，运行脚本所在父级目录绝对路径不能为空')
        # elif not os.path.exists(script_dirpath):
        #     logger.info(script_dirpath)
        #     return  HttpResponse('保存失败，运行脚本所在父级路径不存在')
        # elif not os.path.isdir(script_dirpath):
        #     return  HttpResponse('保存失败，自动化脚本所在父级路径不为目录')
        # else:
        #     # logger.info('正在规范化路径')
        #     script_dirpath = os.path.normpath(script_dirpath)
        # if not os.path.exists(python_path):
        #     return  HttpResponse('保存失败，python.exe程序绝对路径不存在')
        # else:
        #     # logger.info('正在规范化路径')
        #     python_path = os.path.normpath(python_path)

        script_dirpath = os.path.normpath(script_dirpath)
        python_path = os.path.normpath(python_path)
        if valid_flag == '':
            return  HttpResponse('保存失败，是否启用不能为空')

        if order == '': # 如果顺序为空，表明是新增
            all_objects = Running_plan.objects.all()
            if all_objects.exists():
                max_order = all_objects.aggregate(Max('order'))['order__max']
                order = max_order + 1
            else:
                order = 1
            obj = Running_plan(running_plan_num=running_plan_num, running_plan_name=running_plan_name, project_type=project_type,project_id=project_id, project_name=project_name, plan_name=plan_name, plan_id=plan_id,
                                script_dirpath=script_dirpath, python_path=python_path,running_status=running_status, valid_flag=valid_flag, order=order)
            obj.save()
        else: #表明是插入
            # logger.info('即将插入新记录，正在调整记录的顺序') # 插入记录所在行上方的记录都+1
            try:
                with transaction.atomic():
                    all_objects = Running_plan.objects.filter(order__gte=order)
                    for item in all_objects:
                        item.order = item.order + 1
                        item.save()

                    obj = Running_plan(running_plan_num=running_plan_num, running_plan_name=running_plan_name, project_type=project_type,project_id=project_id, project_name=project_name, plan_name=plan_name, plan_id=plan_id,
                                            script_dirpath=script_dirpath, python_path=python_path,running_status=running_status, valid_flag=valid_flag, order=order)
                    obj.save()
            except Exception as e:
                logger.error('%s' % e)
                return  HttpResponse('%s' % e)
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)

# 修改运行计划
def update_running_plan(request):
    try:
        params = request.POST

        id = params['id']
        running_plan_name = params['running_plan_name']
        project_type = params['project_type']
        project_id = params['project_id']
        project_name = params['project_name']
        plan_id = params['plan_id']
        plan_name = params['plan_name']
        script_dirpath = params['script_dirpath']
        python_path = params['python_path']
        valid_flag = params['valid_flag']

        if script_dirpath == '':
            return  HttpResponse('保存失败，自动化脚本所在父级目录绝对路径不能为空')
        # elif not os.path.exists(script_dirpath):
        #     return  HttpResponse('保存失败，自动化脚本所在父级路径不存在')
        # elif not os.path.isdir(script_dirpath):
        #     return  HttpResponse('保存失败，运行脚本所在父级路径不为目录')
        # else:
        #     # logger.info('正在规范化路径')
        #     script_dirpath = os.path.normpath(script_dirpath)
        # if not os.path.exists(python_path):
        #     return  HttpResponse('保存失败，python.exe程序绝对路径不存在')
        # else:
        #     # logger.info('正在规范化路径')
        #     python_path = os.path.normpath(python_path)
        if valid_flag == '':
            return  HttpResponse('保存失败，是否启用不能为空')

        obj = Running_plan.objects.get(id=id)
        obj.running_plan_name =running_plan_name
        obj.project_type = project_type
        obj.project_id = project_id
        obj.project_name = project_name
        obj.plan_id = plan_id
        obj.plan_name = plan_name
        obj.script_dirpath = script_dirpath
        obj.python_path = python_path
        obj.valid_flag = valid_flag
        obj.save()
        return  HttpResponse('success')
    except Exception as e:
        logger.error('%s' % e)
        return HttpResponse('%s' % e)

def exec_running_plan(request):
    try:
        params = request.POST
        params = request.body.decode('utf-8')
        params = json.loads(params)

        running_plan_num = params['runningPlanNum']
        script_dirpath = params['scriptDirpath']
        python_path = params['pythonPath']

        obj = Running_plan.objects.get(running_plan_num=running_plan_num)
        if Running_plan.objects.filter(running_status = '执行中').exists():
            return HttpResponse('当前还有任务未完成')
        elif obj.valid_flag == '禁用':
             return HttpResponse('运行计划已经被禁用')

        obj.running_status = '执行中'
        obj.remark = ''
        obj.save()

        def run_running_plan():
            args = 'cd /d '+ script_dirpath + '&' + '"'+ python_path + '" main.py ' + 'rop ' + str(running_plan_num)
            code = os.system(args)
            if code:
                logger.error('execute running plan fail')
                # logger.error('执行计划出错')
                obj.running_status = '执行失败'
                obj.save()
            else:
                # logger.info('执行成功')
                obj.running_status = '执行成功'
                obj.save()
        # 使用多线程取执行
        thread = threading.Thread(target=run_running_plan,
                              name="exec_thread")
        thread.start()
        return HttpResponse('正在执行程序，请稍后刷新页面查看结果')
    except Exception as e:
        obj = Running_plan.objects.get(running_plan_num=running_plan_num)
        obj.running_status = '执行失败'
        obj.save()
        return HttpResponse('%s' % e)

def reset_running_plan_status(request):
    try:
        params = request.POST

        running_plan_num = params['runningPlanNum']

        obj = Running_plan.objects.get(running_plan_num=running_plan_num)
        obj.running_status = '未执行'
        obj.remark = ''
        obj.save()
        return HttpResponse('重置成功')
    except Exception as e:
        obj = Running_plan.objects.get(running_plan_num=running_plan_num)
        obj.running_status = '重置失败'
        obj.remark = ''
        obj.save()
        return HttpResponse('%s' % e)