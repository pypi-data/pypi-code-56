import gevent.monkey

gevent.monkey.patch_all()

import multiprocessing

# debug = True
bind = "0.0.0.0:8080"
pidfile = "gunicorn.pid"
# accesslog = "log/gaccess.log"
# errorlog = "log/gdebug.log"
loglevel = 'INFO'
capture_output = True
daemon = True

# 启动的进程数
workers = multiprocessing.cpu_count()
worker_class = 'gevent'
x_forwarded_for_header = 'X-FORWARDED-FOR'
