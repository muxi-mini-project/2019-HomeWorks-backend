from . import db, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(15), unique=True, index=True)
    name = db.Column(db.String(10), unique=False, index=False)
    email = db.Column(db.String(20), unique=True, index=True)

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

