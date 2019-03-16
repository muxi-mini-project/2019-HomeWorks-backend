import requests
from flask import jsonify, request
from . import app
from ..models import User
from ..data import assign_list

@app.route('/notice/', methods=['GET'])
def notice():
    cookie = request.headers.get('cookie')
    token = request.headers.get('token')
    if not cookie:
        return jsonify({
                'msg': 'No cookie'}), 400 
    if not token:
        return jsonify({
                'msg': 'No token'}), 400 
    userId = User.get_userId_token(token)
    if not userId:
        return jsonify({
                'msg': 'Invalid token'}), 401 
    
    assign_data = assign_list(cookie, userId)
    assignList = assign_data.get('assignList')
    total = 0
    data = []
    for task in assignList:
        if task.get('status') == 0:
            data.append(task)
            total = total + 1

    user = User.query.filter_by(userId=userId).first()

    return_data = {
                'msg': 'success',
                'cookie': assign_data.get('cookie'),
                'realName': user.name,
                'userName': user.userName,
                'total': total,
                'data': data,
            }

    return jsonify(return_data), 200
