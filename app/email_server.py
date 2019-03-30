import time
from celery import Celery
from flask_mail import Message
from flask import render_template
from config import Celery_config
from . import app as flask_app
from . import mail
from .data import assign_list
from .models import User

celery_app = Celery('email')
celery_app.config_from_object(Celery_config)

def get_recipients():
    users = User.query.all()
    recipients = []
    for u in users:
        if u.email:
            recipients.append({
                    'email': u.email,
                    'name': u.name,
                    'userId': u.userId
                })
    return recipients


def get_assign(userId):
    data = assign_list('', userId).get('assignList')
    total = 0
    assign_data = []
    now = time.time()
    for task in data:
        if not task.get('status') and \
                0 < (task.get('endTime')/1000 - now) / (60*60*24) <=5:
            t = task.get('endTime')
            t /= 1000 if len(str(t))==13 else None
            endTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
            assign_data.append({
                    'courseName': task.get('courseName'),
                    'assignName': task.get("assignName"),
                    'endTime': endTime
                })
            total += 1
    return {
            'total': total,
            'assignList': assign_data,
            }

@celery_app.task
def send_mail_notice():
    recipients = get_recipients()
    for user in recipients:
        assign_data = get_assign(user.get('userId'))
        print(user.get('name') + str(assign_data.get('total')))
        if not assign_data.get('total'):
            continue

        with flask_app.app_context():
            msg = Message("云课堂作业提醒!",
                    recipients = [user.get('email')])
            msg.body = render_template('email_notice.txt', name=user.get('name'), data=assign_data)
            msg.html = render_template('email_notice.html', name=user.get('name'), data=assign_data)
            mail.send(msg)
#            return "Best wish!"
        print('Sended to U!>_<')


def email_verify(recipient, code):
    send_email_verify(recipient, code)

@celery_app.task
def send_email_verify(recipient, code):
    with flask_app.app_context():
        msg = Message("邮箱验证", recipients = [recipient])
        msg.body = render_template('email_verify.txt', code=code)
        mail.send(msg)
        return 'OK'
    print("Send code to U!")


#send_mail()
