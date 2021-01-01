#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
    @author     :   xstatus
    @time       :   2020/9/8 12:50
    @email      :   crawler@88.com
    @project    :   GunicoreFlaskServer -> gunicorn.conf.py
    @IDE        :   PyCharm
    @describe   :   gunicorn配置文件
"""

import gevent.monkey
import multiprocessing

gevent.monkey.patch_all()

# 监听本机的5000端口
bind = '0.0.0.0:5555'

preload_app = True

# 开启进程
# workers=4
workers = multiprocessing.cpu_count() * 3 + 1

# 每个进程的开启线程
threads = multiprocessing.cpu_count() * 2

backlog = 2048

# 切换这个模式就能转换gevent或者meinheld，其他代码不用变
# 工作模式为gevent
worker_class = "gevent"
# 工作模式为meinheld
# worker_class = "egg:meinheld#gunicorn_worker"

# debug=True

# 如果不使用supervisord之类的进程管理工具可以是进程成为守护进程，否则会出问题
daemon = True

# 进程名称
proc_name = 'gunicorn.pid'

# 进程pid记录文件
pidfile = 'app_pid.log'

loglevel = 'debug'
logfile = 'debug.log'
accesslog = 'access.log'
access_log_format = '%(h)s %(t)s %(U)s %(q)s'