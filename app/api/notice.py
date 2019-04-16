import requests, time
from flask import jsonify, request
from . import app
from ..models import User
from ..data import assign_list

# 弹窗提醒&获取未提交任务
@app.route('/notice/getAssignments/', methods=['GET'])
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
        # 未完成且未过期，则加入列表
        if task.get('status') == 0 and task.get('endTime')/1000 >= time.time():
            data.append(task)
            total += 1

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
