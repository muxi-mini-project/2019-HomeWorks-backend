from flask import jsonify, request
from . import app
from ..models import User
from ..verify import verify_userId_token

@app.route('/userInfo/', methods=['GET'])
def user_info():
    cookie = request.headers.get('cookie')
    token = request.headers.get('token')
    if not cookie:
        return jsonify({
                'msg': 'No cookie'}), 400
    if not token:
        return jsonify({
                'msg': 'No token'}), 400
    userId = verify_userId_token(token)
    if not userId:
        return jsonify({
                'msg': 'Invalid token'}), 401

    session = request.session()
    session.cookies.set('cookies', cookie)

    header = {'cookie': cookie}
    url = 'http://spoc.ccnu.edu.cn/studentHomepage/getUserInfo'
    userInfo_get = session.post(url, headers=header).json().get('data')
    if userInfo_get.get('id') != userId:
        return jsonify({'msg': 'Invalid token'}), 401
    userName = userInfo_get.get('username')
    email = User.query.filter_by(userName=userName).first().email
    d

    u = User.query.filter_by()
