import logging
from django.http import HttpResponse

import time
import json
from datetime import datetime
from datetime import timedelta
from datetime import date

logger = logging.getLogger('mylogger')

from other.redis_client import myredis

# 获取找回密码-手机验证码
def get_reset_password_mobile_varify_code(request):
    params = request.GET
    if params:
        try:
            mobile = params['mobile']
        except Exception as e:
            msg = '参数非法 %s' % e
            logging.error(msg)
            return HttpResponse(msg)
        if not mobile.isdigit():
            return HttpResponse('手机号非法')
        else:
            # 拼接key pattern (key: req:cache:code:reset:pwd:18110000014:xxxxxx
            key_pattern = 'req:cache:code:reset:pwd:' + mobile + '*'
            key = myredis.get_keys(key_pattern)
            logging.info(key)
            if key:
                key = key[0]
            else:
                return HttpResponse('未获取到对应的key')
            result = myredis.get_value_of_key(key)
            if result:
                result = result.decode('unicode_escape')
                varify_code = result[-6:]
                temp = '{"success":true,"verify_code":' + varify_code +'}'
                return HttpResponse(temp)
            else:
                return  HttpResponse('未获key对应的值')
    else:
        return HttpResponse('参数不能为空')

# 找回密码-重置手机验证码已经发送次数
def reset_resetpwd_mobile_varify_code_num(request):
    params = request.POST
    if params:
        try:
            mobile = params['mobile']
        except Exception as e:
            msg = '参数非法 %s' % e
            logging.error(msg)
            return HttpResponse(msg)
        if not mobile.isdigit():
            return HttpResponse('手机号非法')
        else:
            # 拼接key req:cache:code:reset:pwd:18110000014
            key = 'req:limit:qty:reset:pwd:' + mobile
            result = myredis.set_key_value(key,0)
            if result:
                return HttpResponse('success')
            else:
                return  HttpResponse('fail')
    else:
        return HttpResponse('参数不能为空')

# 注册 - 重置手机号验证码发送次数
def reset_register_mobile_code_send_num(request):
    params = request.POST
    if params:
        try:
            mobile = params['mobile']
        except Exception as e:
            msg = '参数非法 %s' % e
            logging.error(msg)
            return HttpResponse(msg)
        if not mobile.isdigit():
            return HttpResponse('手机号非法')
        else:
            # 删除key
            result_key = myredis.get_keys(mobile)
            if result_key:
                result = myredis.delete_key(mobile)
                if result:
                    return HttpResponse('success')
                else:
                    return  HttpResponse('fail')
            else:
                return HttpResponse('success')
    else:
        return HttpResponse('参数不能为空')

# 注册 - 获取注册验证码
def get_register_mobile_code(request):
    params = request.GET
    if params:
        try:
            mobile = params['mobile']
        except Exception as e:
            msg = '参数非法 %s' % e
            logging.error(msg)
            return HttpResponse(msg)
        if not mobile.isdigit():
            return HttpResponse('手机号非法')
        else:
            result = myredis.get_value_of_key(mobile)
            if result:
                result = result.decode('unicode_escape')
                varify_code = result[-8:-2]
                temp = '{"success":true,"register_verify_code":' + varify_code +'}'
                return HttpResponse(temp)
            else:
                return  HttpResponse('未获key对应的值')
    else:
        return HttpResponse('参数不能为空')

# 获取时间和日期
def get_date_and_time(request):
    # ---------------------------当前时间---------------------------
    curtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) # 形如 2017-11-30 17:14:02
    # logger.info('当前时间curtime：%s' % curtime)

    curtime_puls10s = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()+10))

    #---------------------------当前日期(本地日期)---------------------------
    current_date = date.today() # 等同于 date.fromtimestamp(time.time()).
    today_yyyy_mm_dd = time.strftime('%Y-%m-%d', current_date.timetuple())
    # logger.info('当前日期today_yyyy_mm_dd：%s' % today_yyyy_mm_dd)

    today_yyyymmdd = time.strftime('%Y%m%d', current_date.timetuple())
    # logger.info('当前日期today_yyyymmdd：%s' % today_yyyymmdd)



    #---------------------------昨天(本地日期)---------------------------
    yesterday  = current_date - timedelta(days = 1)
    yesterday_yyyy_mm_dd = time.strftime('%Y-%m-%d', yesterday.timetuple())
    # logger.info('昨日yesterday_yyyy_mm_dd：%s' % yesterday_yyyy_mm_dd)

    yesterday_yyyymmdd = time.strftime('%Y%m%d', yesterday.timetuple())
    # logger.info('昨日yesterday_yyyymmdd：%s' % yesterday_yyyymmdd)


    # ---------------------------1号---------------------------
    # 当月1号
    curmonth_first_day_yyyymmdd = time.strftime('%Y%m01', current_date.timetuple())
    # logger.info('当月1号curmonth_first_day_yyyymmdd：%s' % curmonth_first_day_yyyymmdd)

    curmonth_first_day_yyyy_mm_dd = time.strftime('%Y-%m-01', current_date.timetuple())
    # logger.info('当月1号curmonth_first_day_yyyy_mm_dd：%s' % curmonth_first_day_yyyy_mm_dd)

    # 下月1号
    next_month_first_day_yyyymmdd = time.strftime('%Y%m01',(current_date + timedelta(days=32 - current_date.day)).timetuple())
    # logger.info('下月1号next_month_first_day_yyyymmdd：%s' % next_month_first_day_yyyymmdd)

    next_month_first_day_yyyy_mm_dd = time.strftime('%Y-%m-01',(current_date + timedelta(days=32 - current_date.day)).timetuple())
    # logger.info('下月1号next_month_first_day_yyyy_mm_dd：%s' % next_month_first_day_yyyy_mm_dd)

    # 上月1号
    last_month_first_day_yyyy_mm_dd = time.strftime('%Y-%m-01', (current_date - timedelta(days=current_date.day)).timetuple())
    # logger.info('上月1号last_month_first_day_yyyy_mm_dd：%s' % last_month_first_day_yyyy_mm_dd)

    last_month_first_day_yyyymmdd = time.strftime('%Y%m01', (current_date - timedelta(days=current_date.day)).timetuple())
    # logger.info('上月1号last_month_first_day_yyyymmdd：%s' % last_month_first_day_yyyymmdd)

    # ---------------------------月末---------------------------
    # 当前月末
    curmonth_final_day_date_yyyymmdd = datetime.strptime(next_month_first_day_yyyymmdd, '%Y%m%d') - timedelta(days=1)
    curmonth_final_day_yyyymmdd = time.strftime('%Y%m%d',curmonth_final_day_date_yyyymmdd.timetuple())
    # logger.info('当月月末curmonth_final_day_yyyymmdd：%s' % curmonth_final_day_yyyymmdd)

    curmonth_final_day_yyyy_mm_dd = time.strftime('%Y-%m-%d',curmonth_final_day_date_yyyymmdd.timetuple())
    # logger.info('当月月末curmonth_final_day_yyyy_mm_dd：%s' % curmonth_final_day_yyyy_mm_dd)

    # 上月月末
    last_month_final_day_date_yyyymmdd = datetime.strptime(curmonth_first_day_yyyymmdd, '%Y%m%d') - timedelta(days=1)
    last_month_final_day_yyyymmdd = time.strftime('%Y%m%d',last_month_final_day_date_yyyymmdd.timetuple())
    # logger.info('上月月末last_month_final_day_yyyymmdd：%s'% last_month_final_day_yyyymmdd)

    last_month_final_day_yyyy_mm_dd = time.strftime('%Y-%m-%d',last_month_final_day_date_yyyymmdd.timetuple())
    # logger.info('上月月末last_month_final_day_yyyy_mm_dd：%s' % last_month_final_day_yyyy_mm_dd)

    #---------------------------最近7天(昨日往前算7天)---------------------------
    recent_7_day_date = current_date - timedelta(days=7)
    recent_7day_range_yyyymmdd = time.strftime('%Y%m%d', recent_7_day_date.timetuple()) + '-' + time.strftime('%Y%m%d', yesterday.timetuple())
    # logger.info('最近7天recent_7day_range_yyyymmdd：%s' % recent_7day_range_yyyymmdd)

    recent_7day_range_yyyy_mm_dd = time.strftime('%Y-%m-%d', recent_7_day_date.timetuple()) + '-' + time.strftime('%Y-%m-%d', yesterday.timetuple())
    # logger.info('最近7天recent_7day_range_yyyy_mm_dd：%s' % recent_7day_range_yyyy_mm_dd)


    #---------------------------最近30天(昨日往前算30天)---------------------------
    recent_30day_date = current_date - timedelta(days=30)
    recent_30day_range_yyyy_mm_dd =  time.strftime('%Y%m%d', recent_30day_date.timetuple()) + '-' + time.strftime('%Y%m%d', yesterday.timetuple())
    # logger.info('最近30天recent_30day_range_yyyy_mm_dd：%s' % recent_30day_range_yyyy_mm_dd)

    recent_30day_range_yyyymmdd =  time.strftime('%Y-%m-%d', recent_30day_date.timetuple()) + '-' + time.strftime('%Y-%m-%d', yesterday.timetuple())
    # logger.info('最近30天recent_30day_range_yyyymmdd：%s' % recent_30day_range_yyyymmdd)

    #---------------------------月初-月末---------------------------
    # 当月月初-月末
    curmonth_range_yyyymmdd = curmonth_first_day_yyyymmdd + '-' + curmonth_final_day_yyyymmdd
    # logger.info('当月月初-月末curmonth_range_yyyymmdd：%s' % curmonth_range_yyyymmdd)

    curmonth_range_yyyy_mm_dd = curmonth_first_day_yyyy_mm_dd + '-' + curmonth_final_day_yyyy_mm_dd
    # logger.info('当月月初-月末curmonth_range_yyyy_mm_dd：%s' % curmonth_range_yyyy_mm_dd)

    # 上月初-月末
    lastmonth_range_yyyymmdd = curmonth_first_day_yyyymmdd + '-' + curmonth_final_day_yyyymmdd
    # logger.info('上月月初-月末lastmonth_range_yyyymmdd：%s' % lastmonth_range_yyyymmdd)

    lastmonth_range_yyyy_mm_dd = curmonth_first_day_yyyy_mm_dd + '-' + curmonth_final_day_yyyy_mm_dd
    # logger.info('上月月初-月末lastmonth_range_yyyymmdd：%s' % lastmonth_range_yyyy_mm_dd)


    # ---------------------------月份---------------------------
    # 当年当月
    current_month_yyyy_mm = time.strftime('%Y-%m', current_date.timetuple())
    # logger.info('当年当月current_month_yyyy_mm：%s' % current_month_yyyy_mm)

    current_month_yyyymm = time.strftime('%Y%m', current_date.timetuple())
    # logger.info('当年当月current_month_yyyymm：%s' % current_month_yyyymm)


    # 当年上月
    last_month_yyyy_mm = time.strftime('%Y-%m', (current_date - timedelta(days=current_date.day)).timetuple())
    # logger.info('当年上月last_month_yyyy_mm：%s' % last_month_yyyy_mm)

    last_month_yyyymm = time.strftime('%Y%m', (current_date - timedelta(days=current_date.day)).timetuple())
    # logger.info('当年上月last_month_yyyymm：%s' % last_month_yyyymm)

    # 去年当月
    current_month_last_year_yyyy_mm = time.strftime('%Y-%m', current_date.replace(year=current_date.year-1).timetuple())
    # logger.info('去年当月current_month_last_year_yyyy_mm：%s' % current_month_last_year_yyyy_mm)

    current_month_last_year_yyyymm = time.strftime('%Y-%m', current_date.replace(year=current_date.year-1).timetuple())
    # logger.info('去年当月current_month_last_year_yyyymm：%s' % current_month_last_year_yyyymm)

    # 去年12月
    december_month_last_year_yyyy_mm = time.strftime('%Y-%m', current_date.replace(year=current_date.year-1, month=12).timetuple())
    # logger.info('去年12月december_month_last_year_yyyy_mm：%s' % december_month_last_year_yyyy_mm)

    december_month_last_year_yyyymm = time.strftime('%Y%m', current_date.replace(year=current_date.year-1, month=12).timetuple())
    # logger.info('去年12月december_month_last_year_yyyymm：%s' % december_month_last_year_yyyymm)


    # ---------------------------周数---------------------------
    # 本周对应的周数,即第几周
    week_num = time.strftime('%Y%U', current_date.timetuple())
    current_week_num_yyyymm = str(int(week_num) + 1) # python的第几周，周数从0开始的，所以+1
    # logger.info('本周是第几周current_week_num_yyyymm：%s' % current_week_num_yyyymm)

    current_week_num_yyyy_mm = current_week_num_yyyymm[0:4] + '-' + current_week_num_yyyymm[4:]
    # logger.info('本周是第几周current_week_num_yyyymm：%s' % current_week_num_yyyy_mm)

    # 上周是第几周
    week_num = time.strftime('%Y%U', (current_date - timedelta(days=7)).timetuple())
    last_week_num_yyyyno = str(int(week_num) + 1)
    # logger.info('上周是第几周last_week_num_yyyyno：%s' % last_week_num_yyyyno)


    # ---------------------------时间戳(毫秒)---------------------------
    # 当前本地时间对应的时间戳(毫秒)
    millisecond_for_curtime = int(time.mktime(datetime.now().timetuple()) * 1000)
    # logger.info('当前本地时间对应的时间戳millisecond_for_curtime：%s' % millisecond_for_curtime)

    # 当前本地日期对应的时间戳(毫秒)
    millisecond_for_curdate = int(int(time.mktime(current_date.timetuple()) * 1000))
    # logger.info('当前本地日期对应的时间戳millisecond_for_curdate：%s' % millisecond_for_curdate)

    # 昨日本地日期对应的时间戳(毫秒)
    millisecond_for_yesterday = int(time.mktime(yesterday.timetuple()) * 1000)
    # logger.info('昨日本地日期对应的时间戳millisecond_for_yesterday：%s' % millisecond_for_yesterday)

    # ---------------------------周x对应的日期---------------------------
    # 本周一(当前日期所在周周一)
    weekday1_date = date.today() - timedelta(days=date.today().isoweekday()) + timedelta(days=1)
    weekday1_yyyymmdd = time.strftime('%Y%m%d', weekday1_date.timetuple())
    # logger.info('本周一weekday1_yyyymmdd：%s' % weekday1_yyyymmdd)

    weekday1_yyyy_mm_dd = time.strftime('%Y%m%d', weekday1_date.timetuple())
    # logger.info('本周一weekday1_yyyy_mm_dd：%s' % weekday1_yyyy_mm_dd)

    # 本周日
    weekday7_date = date.today() - timedelta(days=date.today().isoweekday()) + timedelta(days=7)
    weekday7_yyyymmdd = time.strftime('%Y%m%d', weekday7_date.timetuple())
    # logger.info('本周日weekday7_yyyymmdd：%s' % weekday7_yyyymmdd)

    weekday7_yyyy_mm_dd = time.strftime('%Y%m%d', weekday7_date.timetuple())
    # logger.info('本周日weekday7_yyyy_mm_dd：%s' % weekday7_yyyy_mm_dd)

    # 上周一
    last_weekday1_date = weekday1_date - timedelta(days=7)
    last_weekday1_yyyymmdd = time.strftime('%Y%m%d', last_weekday1_date.timetuple())
    # logger.info('上周一last_weekday1_yyyymmdd：%s' % last_weekday1_yyyymmdd)

    last_weekday1_yyyy_mm_dd = time.strftime('%Y-%m-%d', last_weekday1_date.timetuple())
    # logger.info('上周一last_weekday1_yyyymmdd：%s' % last_weekday1_yyyy_mm_dd)

    # 上周日
    last_weekday7_date = weekday7_date - timedelta(days=7)
    last_weekday7_yyyymmdd = time.strftime('%Y%m%d', last_weekday7_date.timetuple())
    # logger.info('上周日last_weekday7_yyyymmdd：%s' % last_weekday7_yyyymmdd)

    last_weekday7_yyyy_mm_dd = time.strftime('%Y-%m-%d', last_weekday7_date.timetuple())
    # logger.info('上周日last_weekday7_yyyy_mm_dd：%s' % last_weekday7_yyyy_mm_dd)

    # 上周、上上周周一（# 如果当前日期为周日，则为上周周一，否则上上周一）
    if (date.today().isoweekday() == 7):
        pre_weekday1_date = weekday1_date - timedelta(days=7)
    else:
        pre_weekday1_date = weekday1_date - timedelta(days=14)
    pre_weekday1_yyyymmdd = time.strftime('%Y%m%d', pre_weekday1_date.timetuple())
    # logger.info('上周、上上周周一pre_weekday1_yyyymmdd：%s' % pre_weekday1_yyyymmdd)

    pre_weekday1_yyyy_mm_dd = time.strftime('%Y-%m-%d', pre_weekday1_date.timetuple())
    # logger.info('上周、上上周周一pre_weekday1_yyyy_mm_dd：%s' % pre_weekday1_yyyy_mm_dd)


    # 上周、上上周的周日（# 如果当前日期为周日，则为上周周日，否则上上周日）
    if (date.today().isoweekday() == 7):
        pre_weekday7_date = weekday7_date - timedelta(days=7)
    else:
        pre_weekday7_date = weekday7_date - timedelta(days=14)
    pre_weekday7_yyyymmdd = time.strftime('%Y%m%d', pre_weekday7_date.timetuple())
    # logger.info('上周、上上周周日pre_weekday7_yyyymmdd：%s' % pre_weekday7_yyyymmdd)

    pre_weekday7_yyyy_mm_dd = time.strftime('%Y-%m-%d', pre_weekday7_date.timetuple())
    # logger.info('上周、上上周周日pre_weekday7_yyyy_mm_dd：%s' % pre_weekday7_yyyy_mm_dd)

    # last_weekday7_date_of_week_chosen = pre_weekday7_date - timedelta(days=7) # 所选择自然周的上周日
    # last_weekday7_of_week_chosen =  time.strftime('%Y-%m-%d', last_weekday7_date_of_week_chosen.timetuple())

    # ---------------------------周一到周日---------------------------
    # 本周一到本周日
    weekday1_to_weekday7_yyyymmdd = weekday1_yyyymmdd + '-' + weekday7_yyyymmdd
    # logger.info('本周一到本周日weekday1_to_weekday7_yyyymmdd：%s' % weekday1_to_weekday7_yyyymmdd)

    weekday1_to_weekday7_yyyy_mm_dd = weekday1_yyyy_mm_dd + '-' + weekday7_yyyy_mm_dd
    # logger.info('本周一到本周日weekday1_to_weekday7_yyyy_mm_dd：%s' % weekday1_to_weekday7_yyyy_mm_dd)

    # 上周一到上周日
    last_weekday1_to_weekday7_yyyymmdd = last_weekday1_yyyymmdd + '-' + last_weekday7_yyyymmdd
    # logger.info('上周一到上周日last_weekday1_to_weekday7_yyyymmdd：%s' % last_weekday1_to_weekday7_yyyymmdd)

    last_weekday1_to_weekday7_yyyy_mm_dd = last_weekday1_yyyy_mm_dd + '-' + last_weekday7_yyyy_mm_dd
    # logger.info('上周一到上周日last_weekday1_to_weekday7_yyyy_mm_dd：%s' % last_weekday1_to_weekday7_yyyy_mm_dd)

    # pre_pre_weekday1_yyyy_mm_dd = time.strftime('%Y-%m-%d', (pre_weekday1_date - timedelta(days=7)).timetuple())
    # logger.info('上周、上上周周一pre_pre_weekday1_yyyy_mm_dd：%s' % pre_pre_weekday1_yyyy_mm_dd)

    # # 上周、上上周周一到周日（# 如果当前日期为周日，则为上周1-上周日，否则上上周周1-上上周日）
    # if (date.today().isoweekday() == 7):
    #     pre_weekday1_to_weekday7 = weekday1_yyyymmdd + '-' + weekday7_yyyymmdd
    # else:
    #     pre_weekday1_to_weekday7 =  pre_weekday1_yyyymmdd + '-' + pre_weekday7_yyyymmdd
    #

    var_dic =  {
        "curtime":curtime,															    #当前时间curtime：2018-03-19 15:08:15
        "curtime_puls10s":curtime_puls10s,                                           #当前时间+10秒：2018-03-19 15:11:15
        "today_yyyy_mm_dd":today_yyyy_mm_dd,										    #当前日期today_yyyy_mm_dd：2018-03-19
        "today_yyyymmdd":today_yyyymmdd,											    #当前日期today_yyyymmdd：20180319
        "yesterday_yyyy_mm_dd":yesterday_yyyy_mm_dd,								    #昨日yesterday_yyyy_mm_dd：2018-03-18
        "yesterday_yyyymmdd":yesterday_yyyymmdd,								    	#昨日yesterday_yyyymmdd：20180318
        "curmonth_first_day_yyyymmdd":curmonth_first_day_yyyymmdd,					#当月1号curmonth_first_day_yyyymmdd：20180301
        "curmonth_first_day_yyyy_mm_dd":curmonth_first_day_yyyy_mm_dd,				#当月1号curmonth_first_day_yyyy_mm_dd：2018-03-01
        "next_month_first_day_yyyymmdd":next_month_first_day_yyyymmdd,				#下月1号next_month_first_day_yyyymmdd：20180401
        "next_month_first_day_yyyy_mm_dd":next_month_first_day_yyyy_mm_dd,			#下月1号next_month_first_day_yyyy_mm_dd：2018-04-01
        "last_month_first_day_yyyy_mm_dd":last_month_first_day_yyyy_mm_dd,			#上月1号last_month_first_day_yyyy_mm_dd：2018-02-01
        "last_month_first_day_yyyymmdd":last_month_first_day_yyyymmdd,				#上月1号last_month_first_day_yyyymmdd：20180201
        "curmonth_final_day_yyyymmdd":curmonth_final_day_yyyymmdd,					#当月月末curmonth_final_day_yyyymmdd：20180331
        "curmonth_final_day_yyyy_mm_dd":curmonth_final_day_yyyy_mm_dd,				#当月月末curmonth_final_day_yyyy_mm_dd：2018-03-31
        "last_month_final_day_yyyymmdd":last_month_final_day_yyyymmdd,				#上月月末last_month_final_day_yyyymmdd：20180228
        "last_month_final_day_yyyy_mm_dd":last_month_final_day_yyyy_mm_dd,			#上月月末last_month_final_day_yyyy_mm_dd：2018-02-28
        "recent_7day_range_yyyymmdd":recent_7day_range_yyyymmdd,					#最近7天recent_7day_range_yyyymmdd：20180312-20180318
        "recent_7day_range_yyyy_mm_dd":recent_7day_range_yyyy_mm_dd,				#最近7天recent_7day_range_yyyy_mm_dd：2018-03-12-2018-03-18
        "recent_30day_range_yyyy_mm_dd":recent_30day_range_yyyy_mm_dd,				#最近30天recent_30day_range_yyyy_mm_dd：20180217-20180318
        "recent_30day_range_yyyymmdd":recent_30day_range_yyyymmdd,					#最近30天recent_30day_range_yyyymmdd：2018-02-17-2018-03-18
        "curmonth_range_yyyymmdd":curmonth_range_yyyymmdd,      					#当月月初-月末curmonth_range_yyyymmdd：20180301-20180331
        "curmonth_range_yyyy_mm_dd":curmonth_range_yyyy_mm_dd,						#当月月初-月末curmonth_range_yyyy_mm_dd：2018-03-01-2018-03-31
        "lastmonth_range_yyyymmdd":lastmonth_range_yyyymmdd,						#上月月初-月末lastmonth_range_yyyymmdd：20180301-20180331
        "lastmonth_range_yyyy_mm_dd":lastmonth_range_yyyy_mm_dd,					#上月月初-月末lastmonth_range_yyyymmdd：2018-03-01-2018-03-31
        "current_month_yyyy_mm":current_month_yyyy_mm,      						    #当年当月current_month_yyyy_mm：2018-03
        "current_month_yyyymm":current_month_yyyymm,        						    #当年当月current_month_yyyymm：201803
        "last_month_yyyy_mm":last_month_yyyy_mm,            						    #当年上月last_month_yyyy_mm：2018-02
        "last_month_yyyymm":last_month_yyyymm,              						    #当年上月last_month_yyyymm：201802
        "current_month_last_year_yyyy_mm":current_month_last_year_yyyy_mm,			#去年当月current_month_last_year_yyyy_mm：2017-03
        "current_month_last_year_yyyymm":current_month_last_year_yyyymm,           #去年当月current_month_last_year_yyyymm：201703
        "december_month_last_year_yyyy_mm":december_month_last_year_yyyy_mm,		#去年12月december_month_last_year_yyyy_mm：2017-12
        "december_month_last_year_yyyymm":december_month_last_year_yyyymm,			#去年12月december_month_last_year_yyyymm：201712
        "current_week_num_yyyymm":current_week_num_yyyymm,  						#本周属于第几周current_week_num_yyyymm：201812
        "current_week_num_yyyy_mm":current_week_num_yyyy_mm,   						#本周属于第几周current_week_num_yyyymm：2018-12
        "last_week_num_yyyyno":last_week_num_yyyyno,                                #上周是第几周last_week_num_yyyyno：201811
        "millisecond_for_curtime":millisecond_for_curtime,  						#当前本地时间对应的时间戳millisecond_for_curtime：1521443295000
        "millisecond_for_curdate":millisecond_for_curdate,  						#当前本地日期对应的时间戳millisecond_for_curdate：1521388800000
        "millisecond_for_yesterday":millisecond_for_yesterday,						#昨日本地日期对应的时间戳millisecond_for_yesterday：1521302400000
        "weekday1_yyyymmdd":weekday1_yyyymmdd,              						    #本周一weekday1_yyyymmdd：20180319
        "weekday1_yyyy_mm_dd":weekday1_yyyy_mm_dd,          						    #本周一weekday1_yyyy_mm_dd：20180319
        "weekday7_yyyymmdd":weekday7_yyyymmdd,              						    #本周日weekday7_yyyymmdd：20180325
        "weekday7_yyyy_mm_dd":weekday7_yyyy_mm_dd,          						    #本周日weekday7_yyyy_mm_dd：20180325
        "last_weekday1_yyyymmdd":last_weekday1_yyyymmdd,                            #上周一last_weekday1_yyyymmdd：20180312
        "last_weekday1_yyyy_mm_dd":last_weekday1_yyyy_mm_dd,                        #上周一last_weekday1_yyyy_mm_dd：2018-03-12
        "last_weekday7_yyyymmdd":last_weekday7_yyyymmdd,    						#上周日last_weekday7_yyyymmdd：20180318
        "last_weekday7_yyyy_mm_dd":last_weekday7_yyyy_mm_dd,						#上周日last_weekday7_yyyy_mm_dd：2018-03-18
        "weekday1_to_weekday7_yyyymmdd":weekday1_to_weekday7_yyyymmdd,             #本周一到本周日weekday1_to_weekday7_yyyymmdd：20180319-20180325
        "weekday1_to_weekday7_yyyy_mm_dd":weekday1_to_weekday7_yyyy_mm_dd,         #本周一到本周日last_weekday1_to_weekday7_yyyy_mm_dd：20180319-20180325
        "last_weekday1_to_weekday7_yyyymmdd":last_weekday1_to_weekday7_yyyymmdd,        #上周一到上周日last_weekday1_to_weekday7_yyyymmdd：20180312-20180318
        "last_weekday1_to_weekday7_yyyy_mm_dd":last_weekday1_to_weekday7_yyyy_mm_dd,        #上周一到上周日last_weekday1_to_weekday7_yyyy_mm_dd：2018-03-12-2018-03-18
        "pre_weekday1_yyyymmdd":pre_weekday1_yyyymmdd,      						          #上周、上上周周一pre_weekday1_yyyymmdd：20180305
        "pre_weekday1_yyyy_mm_dd":pre_weekday1_yyyy_mm_dd,       					      #上周、上上周周一pre_weekday1_yyyy_mm_dd：2018-03-05
        "pre_weekday7_yyyymmdd":pre_weekday7_yyyymmdd,      						          #上周、上上周周日pre_weekday7_yyyymmdd：20180311
        "pre_weekday7_yyyy_mm_dd":pre_weekday7_yyyy_mm_dd   						      #上周、上上周周日pre_weekday7_yyyy_mm_dd：2018-03-11
    }

    var = json.dumps(var_dic)
    return HttpResponse(var)