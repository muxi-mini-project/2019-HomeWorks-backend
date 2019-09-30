import requests
from flask import session, jsonify, request
from functools import wraps

from . import Config
from .models import User


# 课堂站点验证
def verify_siteId(siteId, userId):
    url = 'http://spoc.ccnu.edu.cn/studentHomepage/getMySite'
    payload = {
            'userId': userId,
            'termCode': Config.TERM,
            'pageNum': 1,
            'pageSize': 30,
    }
    r = requests.post(url, json=payload)
    total = r.json().get('data').get('total')
    data = r.json().get('data').get('list')
    for i in range(total):
        aim_siteId = data[i].get('siteId')
        if siteId == aim_siteId:
            return True
    return False

# token验证
def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('token')
        if not token:
            return jsonify({
                'msg': 'No token'
            }), 400

        userId = User.get_userId_token(token)
        if not userId:
            return jsonify({
                'msg': 'Invalid token'}), 401
        return func(*args, **kwargs)

    return wrapper
