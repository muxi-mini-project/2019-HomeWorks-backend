from . import db, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from random import randint
import time

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(15), unique=True, index=True)
    name = db.Column(db.String(10), unique=False, index=False)
    userId = db.Column(db.String(50), unique=True, index=True)
    email = db.Column(db.String(20), unique=True, index=True)
    email_send = db.Column(db.Boolean)

    def __repr__(self):
        return '<User {} {}>'.format(self.userName, self.name)

    def generate_token(self, userId):
        s = Serializer(app.config['SECRET_KEY'], expires_in=99999999)
        return s.dumps({
                    'id': self.id,
                    'userId': userId
                    }).decode('utf-8')

    @staticmethod
    def get_userId_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return None
        id = data.get('id')
        userId = data.get('userId')
        if id is None or userId is None:
            return None
        return userId

    def generate_email_token(self, email):
        code = randint(1000, 9999)  #生成(1000,9999]的四位验证码
        s = Serializer(app.config['SECRET_KEY'], expires_in=600)    #有效时间：10分钟
        """
        return s.dumps({
                    'id': self.id,
                    'email': email,
                    'code': code
                }).decode('utf-8')
        """
        token = s.dumps({
                    'id': self.id,
                    'email': email,
                    'code': code
                }).decode('utf-8')
        return {'token': token, 'code': code}

    @staticmethod
    def verify_email(email, code, token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return None
        id = data.get('id')
        email_get = data.get("email")
        code_get = data.get('code')
        if not id or code != code_get or email != email_get:
            return False
        return True

class NoticeTimeForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(50), unique=False, index=True)
    notice_time = db.Column(db.Integer, unique=False, index=False)
    notice_time_id = db.Column(db.String(50), unique=True, index=True)
    is_active = db.Column(db.Boolean)

    def __repr__(self):
        return '<NoticeTime {} {}>'.format(self.notice_time, self.userId)


def generate_notice_time_id(userName):
    now = int(time.time())
    notice_time_id = str(now) + userName
    return notice_time_id

