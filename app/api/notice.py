import requests, time
from flask import jsonify, request
from . import app
from ..models import User
from ..data import assign_list
from ..verify import token_required

# 弹窗提醒&获取未提交任务
@app.route('/notice/getAssignments/', methods=['GET'])
@token_required
def notice():
    cookie = request.headers.get('cookie')
    if not cookie:
        return jsonify({
                'msg': 'No cookie'}), 400 

    token = request.headers.get('token')
    userId = User.get_userId_token(token)

    
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
