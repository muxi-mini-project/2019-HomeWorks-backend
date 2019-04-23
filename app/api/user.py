from flask import jsonify, request
from . import app
from ..models import User
from ..verify import token_required

@app.route('/userInfo/', methods=['GET'])
@token_required
def user_info():
    token = request.headers.get('token')
    userId = User.get_userId_token(token)
    user = User.query.filter_by(userId=userId).first()

    return jsonify({
            'msg': 'success',
            'realName': user.name,
            'userName': user.userName,
            'email': user.email,
        }), 200


