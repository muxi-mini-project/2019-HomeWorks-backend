import requests
from flask import jsonify, request
from . import app
from ..assign_list import assign_list

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
    
    assign_list = assign_list(cookie, userId)

    return_data = {
                'msg': 'success',
                'cookie': cookie,
                'realName': realName,
                'userName': userName,
                'total': total,
                'data': data,
            }

    return jsonify(return_data), 200
