from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.utils.safestring import mark_safe

import json
import logging
from website.models import Navigation

logger = logging.getLogger('mylogger')

def index(request):
    template = loader.get_template('website/pages/index.html')
    #return render(request, template)
    return HttpResponse(template.render({}, request))

# 返回左侧导航
def get_nav(request):
    nav_menus = {'menus':[]}
    nav_menus_queryset = Navigation.objects.filter(parent_id=0).order_by('order').values()

    # logger.debug('获取的一级菜单有:')
    # logger.debug(nav_menus_queryset)

    for menu in nav_menus_queryset:
        menu['sub_menus'] = []
        sub_nav_menus_queryset = Navigation.objects.filter(parent_id=menu['id']).order_by('order').values()
        for sub_menu  in  sub_nav_menus_queryset:
            menu['sub_menus'].append(sub_menu)

        nav_menus['menus'].append(menu)
    # logger.info(nav_menus)

    nav_menus = json.dumps(nav_menus)
    return HttpResponse(nav_menus, content_type="application/json")
