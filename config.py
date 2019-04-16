import os
from datetime import timedelta
from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY") or "Homeworks_key"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

#    DEBUG = True,
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'Shadow <1142319190@qq.com>'

class Celery_config(object):
    # Broker and Backend
    BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    # Timezone
    CELERY_TIMEZONE='Asia/Shanghai'

    CELERY_IMPORTS = ( 
        'app.email_server'
    )   

    # schedules
    CELERYBEAT_SCHEDULE = {
        'add-every-7': {
            'task': 'app.email_server.send_mail_notice',
#            'schedule': crontab(hour=7, minute=30),
#            'schedule': timedelta(hours=1)
            'schedule': crontab(minute=57, hour='*/1'),
        }
    }
