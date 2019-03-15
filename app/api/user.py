import requests
from flask import jsonify, request
from . import app
from ..models import User

@app.route('/userInfo/', methods=['GET'])
def user_info():
    token = request.headers.get('token')
    if not token:
        return jsonify({
                'msg': 'No token'}), 400
    userId = User.get_userId_token(token)
    if not userId:
        return jsonify({
                'msg': 'Invalid token'}), 401
    
    user = User.query.filter_by(userId=userId).first()

    return jsonify({
            'msg': 'success',
            'realName': user.name,
            'userName': user.userName,
            'email': user.email,
        }), 200

