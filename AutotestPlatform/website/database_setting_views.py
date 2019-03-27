from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

import json
import logging
from django.core.paginator import  Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Max
from django.db import transaction

from website.models import Database_setting
from website.models import UI_test_case_step
from website.models import API_test_case_step

logger = logging.getLogger('mylogger')

# 系统配置-数据库配置
def database_setting(request):
    template = loader.get_template('website/pages/databaseSetting.html')
    return HttpResponse(template.render({}, request))

# 获取系统配置-数据库配置，列表数据
def get_database_settings(request):
    griddata = {"total": 0, "rows": []}
    rows = [] # 用于存储记录行

    # 获取总记录数
    records = Database_setting.objects.all().order_by('-order').values()
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
        if obj['db_passwd'] != '':
            obj['db_passwd'] = '**************'
        rows.append(obj)
    griddata["rows"] =  rows
    griddata = json.dumps(griddata)
    return HttpResponse(griddata)

# 新增
def add_database_setting(request):
    try:
        params = request.POST

        db_type = params['db_type']
        db_alias = params['db_alias'].replace(' ', '').replace('\t', '').replace('-', '')
        db_name = params['db_name']
        db_host = params['db_host']
        db_port = params['db_port']
        db_user = params['db_user']
        db_passwd = params['db_passwd']
        project_type = params['project_type']
        project_name = params['project_name']
        project_id = params['project_id']
        environment = params['environment']
        environment_id = params['environment_id']
        order = params['order']

        if not db_type:
            return HttpResponse('数据库类型不能为空')
        if not db_alias:
            return HttpResponse('数据库别名不能为空')
        elif Database_setting.objects.filter(db_alias=db_alias).exists():
            return HttpResponse('数据库别名已存在')
        if not db_name:
            return HttpResponse('数据库名称不能为空')
        if not db_host:
            return HttpResponse('主机地址不能为空')
        if not db_port:
            return HttpResponse('端口号不能为空')
        elif not db_port.isdigit():
            return  HttpResponse('端口号只能为数字')
        # elif Database_setting.objects.filter(db_host=db_host).filter(db_port=db_port).filter(db_user=db_user).exists():
        #     return HttpResponse('端口号(%s)已存在' % db_port)
        if not db_user:
            return HttpResponse('用户名不能为空')
        if db_type != 'Redis' and  not db_passwd:
            return HttpResponse('密码不能为空')

        if not project_type:
            return HttpResponse('项目类型不能为空')
        if not project_name:
            return HttpResponse('所属项目不能为空')
        if not environment:
            return HttpResponse('所属环境不能为空')

        if order == '': # 如果顺序为空，表明是新增
            all_objects = Database_setting.objects.all()
            if all_objects.exists():
                max_order = all_objects.aggregate(Max('order'))['order__max']
                order = max_order + 1
            else:
                order = 1
            obj = Database_setting(db_type = db_type, db_alias=db_alias, db_name=db_name, db_host=db_host, db_port=db_port, db_user=db_user,
                     db_passwd=db_passwd, project_type=project_type, project_name=project_name, environment=environment, environment_id=environment_id, order=order, project_id=project_id)
            obj.save()
        else: #表明是插入
            logger.info('即将插入新记录，正在调整记录的顺序') # 插入记录所在行上方的记录都+1
            try:
                with transaction.atomic():
                    all_objects = Database_setting.objects.filter(order__gte=order)
                    for item in all_objects:
                        item.order = item.order + 1
                        item.save()

                    obj = Database_setting(db_type = db_type, db_alias=db_alias, db_name=db_name, db_host=db_host, db_port=db_port, db_user=db_user,
                                           db_passwd=db_passwd, project_type=project_type, project_name=project_name, environment=environment, environment_id=environment_id, order=order, project_id=project_id)
                    obj.save()
            except Exception as e:
                logger.error('%s' % e)
                return HttpResponse('%s' % e)
        return  HttpResponse('success')
    except Exception as e:
         return HttpResponse('%s' % e)


# 编辑
def edit_database_setting(request):
    try:
        params = request.POST

        id = params['id']
        db_type = params['db_type']
        db_alias = params['db_alias'].replace(' ', '').replace('\t', '').replace('-', '')
        db_name = params['db_name']
        db_host = params['db_host']
        db_port = params['db_port']
        db_user = params['db_user']
        db_passwd = params['db_passwd']
        project_type = params['project_type']
        project_name = params['project_name']
        environment = params['environment']
        environment_id = params['environment_id']
        project_id = params['project_id']

        if not db_type:
            return HttpResponse('数据库类型不能为空')
        if not db_alias:
            return HttpResponse('数据库别名不能为空')
        elif Database_setting.objects.filter(db_alias=db_alias).exclude(id =id).exists():
            return HttpResponse('数据库别名已存在')
        if db_type != 'Redis' and db_name.strip() == '':
            return HttpResponse('数据库名称不能为空')
        elif db_type == 'Redis' and db_name.strip() == '':
            db_name = '0'
        if not db_host:
            return HttpResponse('主机地址不能为空')
        if not db_port:
            return HttpResponse('端口号不能为空')
        elif not db_port.isdigit():
            return  HttpResponse('端口号只能为数字')

        if db_type != 'Redis' and db_user.strip() == '':
            return HttpResponse('用户名不能为空')
        if db_type != 'Redis' and  not db_passwd:
            return HttpResponse('密码不能为空')
        if not project_type:
            return HttpResponse('项目类型不能为空')
        if not project_name:
            return HttpResponse('所属项目不能为空')
        if not environment:
            return HttpResponse('所属环境不能为空')

        obj = Database_setting.objects.get(id=id)
        obj.db_type = db_type
        obj.db_alias = db_alias
        obj.db_name = db_name
        obj.db_host = db_host
        obj.db_port = db_port
        obj.db_user = db_user
        if db_passwd.strip() != '**************':
            obj.db_passwd = db_passwd
        obj.project_type = project_type
        obj.project_name = project_name
        obj.project_id = project_id
        obj.environment = environment
        obj.environment_id = environment_id
        obj.save()

        # logger.info('同步更新UI测试用例详情表')
        ui_case_step_obj_list = UI_test_case_step.objects.filter(object_id=id)
        for ui_case_step_obj in ui_case_step_obj_list:
            ui_case_step_obj.object = db_alias
            ui_case_step_obj.save()

        # logger.info('同步更新API测试用例详情表')
        ui_case_step_obj_list = API_test_case_step.objects.filter(object_id=id)
        for ui_case_step_obj in ui_case_step_obj_list:
            ui_case_step_obj.object = db_alias
            ui_case_step_obj.save()

        return  HttpResponse('success')
    except Exception as e:
        return HttpResponse('%s' % e)