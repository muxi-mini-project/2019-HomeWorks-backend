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

# 获取需要提醒的云课堂任务
def get_assign(userId):
    data = assign_list('', userId).get('assignList')
    total = 0
    assign_data = []
    # 当前时间，17位的浮点型数值，转换为10位整数，单位为秒
    now = int(time.time())
    # 距现在最近的任务的时间，初始为最大的13位整数
    closest_time = 9999999999999

    for task in data:
        # 13位整数
        endTime = task.get('endTime')
        # 任务未完成且当前时间距ddl短于DDL_TIME，则该任务需要提醒
        if not task.get('status') and \
                0 < (endTime / 1000 - now) / (60*60*24) <= DDL_TIME:

            # 获取距现在最近的任务时间
            closest_time = endTime if closest_time > endTime else closest_time

            # 将时间戳转化为字符串形式的时间
            #t = task.get('endTime')
            t = endTime / 1000 if len(str(endTime))==13 else endTime
            end_time_string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
            assign_data.append({
                    'courseName': task.get('courseName'),
                    'assignName': task.get("assignName"),
                    'endTime': end_time_string,
                })
            total += 1

    return {
            'total': total,
            'assignList': assign_data,
            'closest_time': closest_time,
            }

# 与设置的时间节点是否吻合
def confirm_notice_time(userId, closest_time):
    # 当前时间，17位浮点数，转换为10位整数，单位为秒
    now = int(time.time())
    # 当前时间与最近的任务ddl间隔的小时
    time_interval = (closest_time /1000 - now) / 3600
    notice_time_data = NoticeTimeForm.query.filter_by(userId=userId).all()

    # 未设置时间节点默认情况下为1小时，前后偏差6分钟
    if not notice_time_data and 0.9 <= time_interval <= 1.1:
        return True
    else:
        return False

    # 查找符合的时间节点
    for data in notice_time_data:
        # 前后偏差6分钟
        if data.notice_time - 0.1 <= time_interval <= data.notice_time + 0.1:
            return True
    return False

# 异步发送邮件提醒
@celery_app.task
def send_mail_notice():
    recipients = get_recipients()
    for user in recipients:
        assign_data = get_assign(user.get('userId'))
        print(user.get('name') +' '+ str(assign_data.get('total'))+ '项任务')
        if not assign_data.get('total') or \
            not confirm_notice_time(user.get('userId'), assign_data.get('closest_time')):
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

