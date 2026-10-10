"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
import os

bind = "0.0.0.0:8000"
backlog = 2048

workers = (os.cpu_count() or 1) * 2
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

errorlog = "-"
loglevel = "info"
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

proc_name = "omspy-api"


def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)


def pre_exec(server):
    server.log.info("Forked child, re-executing.")


def when_ready(server):
    server.log.info("Server is ready. Spawning workers.")


def worker_int(worker):
    worker.log.info("Worker received INT or QUIT signal.")


def worker_abort(worker):
    worker.log.info("Worker received SIGABRT signal.")
