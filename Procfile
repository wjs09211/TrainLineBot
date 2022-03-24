web: gunicorn TrainLineBot.wsgi --log-file -
worker: celery -A TrainLineBot worker -l info --pool=threads