from app import email_server
from app.email_server import celery_app

email_server.send_mail_notice.apply_async()
#email_server.send_email_verify.apply_async()
