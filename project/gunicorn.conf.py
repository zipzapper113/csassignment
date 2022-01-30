import os
import gunicorn

bind = "0.0.0.0:8000"
accesslog = "-"
access_log_format = "%(h)s %(t)s %(m)s %(U)s %(s)s in %(D)sµs"
error_log = "-"

workers = 1
threads = 1