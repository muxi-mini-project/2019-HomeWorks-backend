from app import email_notice
from app.email_notice import celery_app

email_notice.send_mail.apply_async()
#email_notice.hello.apply_async()

