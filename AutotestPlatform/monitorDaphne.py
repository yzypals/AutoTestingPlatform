#!/usr/bin/env python
#-*-encoding:utf-8-*-

__author__ = 'shouke'


import subprocess
import shlex


if __name__ == '__main__':
    print('关闭该窗口\按Ctrl+C键，可关闭daphne')
    while True:
        # 判断是否存在任务
        cmd = 'tas1klist | findstr daphne.exe'
        args = shlex.split(cmd)
        with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines = True) as proc:
            try:
                outs, errs = proc.communicate(timeout=60) #超时时间为15秒
                outs = outs.strip()
                errs = errs.strip()
                if outs == '' and errs != '': # 不存在进程
                    # 启动进程
                    cmd = 'daphne -b 0.0.0.0 -p 8001 AutotestPlatform.asgi:application'
                    args = shlex.split(cmd)
                    with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines = True) as proc:
                        outs, errs = proc.communicate() #超时时间为15秒
            except subprocess.TimeoutExpired:
                proc.kill()
                outs, errs = proc.communicate()
            except Exception as e:
                print('运行出错：%s' % e)
