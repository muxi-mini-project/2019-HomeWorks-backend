import requests, re
from flask import jsonify, request
from . import app
from ..models import User
from .. import db

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

@app.route('/mail/modify/', methods=['PUT'])
def mail_modify():
    token = request.headers.get('token')
    if not token:
        return jsonify({
            'msg': 'No token'}), 400
    email = request.get_json().get('email')
    if not email:
        return jsonify({
                'msg': 'No email'}), 400

    # 验证是否为合规的邮箱，需要正则表达式
    if not re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
        return jsonify({'msg': 'Invalid email'}), 400

    userId = User.get_userId_token(token)
    if not userId:
        return jsonify({
                'msg': 'Invalid token'}), 401

    User.query.filter_by(userId=userId).update({'email': email})
    db.session.commit()

    return jsonify({'msg': 'success'}), 200
