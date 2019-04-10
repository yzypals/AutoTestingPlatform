#!/usr/bin/env python
#-*-encoding:utf-8-*-

from django.conf.urls import url

from . import logWebsocketConsumers

websocket_urlpatterns = [
    url(r'^ws/debugAPICaseOrSuit/$', logWebsocketConsumers.LogWebsocketConsumer),
    url(r'^ws/debugAPITestPlan/$', logWebsocketConsumers.LogWebsocketConsumer),
    url(r'^ws/debugAPIRunningPlan/$', logWebsocketConsumers.LogWebsocketConsumer),

]