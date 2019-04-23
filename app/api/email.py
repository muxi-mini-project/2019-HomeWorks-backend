import re
from flask import jsonify, request
from . import app
from ..models import User
from .. import db
from ..email_server import email_verify
from ..verify import token_required

# 修改邮箱
@app.route('/mail/modify/', methods=['PUT'])
@token_required
def mail_modify():
    verify_code_token = request.headers.get('verifyCodeToken')
    if not verify_code_token:
        return jsonify({
            'msg': 'No verifyCodeToken'}), 400
    verify_code = request.get_json().get('verifyCode')
    if not verify_code:
        return jsonify({
            'msg': 'No verifyCode'}), 400
    email = request.get_json().get('email')
    if not email:
        return jsonify({
                'msg': 'No email'}), 400

    # 验证是否为合规的邮箱，需要正则表达式
    if not re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
        return jsonify({'msg': 'Invalid email'}), 400

    token = request.headers.get('token')
    userId = User.get_userId_token(token)

    if not User.verify_email(email, verify_code, verify_code_token):
        return jsonify({
                'msg': 'Wrong verifyCode'}), 400

    User.query.filter_by(userId=userId).update({'email': email})
    db.session.commit()

    return jsonify({'msg': 'success'}), 200

# 发送邮箱验证码
@app.route('/mail/modify/sendVerifyCode/', methods=['POST'])
@token_required
def mail_verify():
    email = request.get_json().get('email')
    if not email:
        return jsonify({
                'msg': 'No email'}), 400

    # 验证是否为合规的邮箱，需要正则表达式
    if not re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
        return jsonify({'msg': 'Invalid email'}), 400

    # 验证此邮箱是否已经存在，并且不可用发送邮件的服务器邮箱
    if User.query.filter_by(email=email).first() or email == '654957943@qq.com':
        return jsonify({
                'msg': 'Email has already existed'}), 400

    token = request.headers.get('token')
    userId = User.get_userId_token(token)

    u = User.query.filter_by(userId=userId).first()
    if not u:
        return jsonify({'msg': 'No user'}), 404
    get_token = u.generate_email_token(email)

    email_verify(recipient=email, code=get_token.get('code'))
#    email_verify.apply_async(recipient=email, code=get_token.get('code'))

    return jsonify({
            'verifyCodeToken': get_token.get('token'),
            'msg': '已发送验证码'}), 200

# 邮件提醒启用状态更改
@app.route("mail/isSend/modify/", methods=['PUT'])
@token_required
def is_send_modify():
    token = request.headers.get('token')
    userId = User.get_userId_token(token)
    
    u = User.query.filter_by(userId=userId).first()
    if not u:
        return jsonify({'msg': 'No user'}), 404

    u.email_send = not u.email_send
    db.session.commit()

    return jsonify({
            "msg": "success",
            "isSend": u.email_send}), 200
