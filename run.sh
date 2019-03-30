nohup flask run -h 0.0.0.0 -p 2333 > myout.file 2>&1 &
nohup celery -A celery_run worker -B > celeryout.file 2>&1 &
