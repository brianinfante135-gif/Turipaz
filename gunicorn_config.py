# gunicorn_config.py
import multiprocessing

workers = 1
worker_class = 'sync'
timeout = 120
max_requests = 1000
max_requests_jitter = 50
worker_tmp_dir = '/dev/shm'
accesslog = '-'
errorlog = '-'
loglevel = 'info'
preload_app = False
graceful_timeout = 30
keepalive = 2

