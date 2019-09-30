import os
from datetime import timedelta, datetime

from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname(__file__))

def get_term():
    now = datetime.now()
    year = now.year
    month = now.month
    if month <= 1:
        TERM = str(year - 1) + '02'
    elif month <= 7:
        TERM = str(year) + '01'
    else:
        TERM = str(year) + '02'
    return TERM


class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY") or "Homeworks_key"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # DEBUG = True

    # 邮件服务
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'Homeworks <654957943@qq.com>'

    # 学期
    TERM = get_term() or '201901'


class Celery_config(object):
    # Broker and Backend
    BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    # Timezone
    CELERY_TIMEZONE = 'Asia/Shanghai'

    CELERY_IMPORTS = (
        'app.email_server'
    )

    # schedules
    CELERYBEAT_SCHEDULE = {
        'add-every-7': {
            'task': 'app.email_server.send_mail_notice',
            #            'schedule': timedelta(hours=1)
            'schedule': crontab(minute=57, hour='*/1'),
        }
    }
