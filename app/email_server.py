import time
from celery import Celery
from flask_mail import Message
from flask import render_template
from config import Celery_config
from . import app as flask_app
from . import mail
from .data import assign_list
from .models import User, NoticeTimeForm

celery_app = Celery('email')
celery_app.config_from_object(Celery_config)

# 距ddl时间（天数）
DDL_TIME = 30

# 获取需要邮件提醒的用户
def get_recipients():
    users = User.query.all()
    recipients = []
    for u in users:
        # 是否邮箱不为空且开启邮件提醒功能
        if u.email and u.email_send:
            recipients.append({
                    'email': u.email,
                    'name': u.name,
                    'userId': u.userId
                })
    return recipients

def get_notice_time(userId):
    all_data_filter = NoticeTimeForm.query.filter_by(userId=userId).all()
    for data in all_data_filter:
        pass


# 获取需要提醒的云课堂任务
def get_assign(userId):
    data = assign_list('', userId).get('assignList')
    total = 0
    assign_data = []
    now = time.time()
    for task in data:
        # 任务未完成且当前时间距ddl短于DDL_TIME，则该任务需要提醒
        if not task.get('status') and \
                0 < (task.get('endTime')/1000 - now) / (60*60*24) <= DDL_TIME:
            #t = task.get('endTime')
            t = t / 1000 if len(str(t))==13 else task.get('endTime')
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

# 异步发送邮件提醒
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
#           return "Best wish!"
        print('Sended to U!>_<')


# 邮箱验证
def email_verify(recipient, code):
    send_email_verify(recipient, code)

# 异步发送邮箱验证码
@celery_app.task
def send_email_verify(recipient, code):
    with flask_app.app_context():
        msg = Message("邮箱验证", recipients = [recipient])
        msg.body = render_template('email_verify.txt', code=code)
        mail.send(msg)
        return 'OK'
    print("Send code to U!")

