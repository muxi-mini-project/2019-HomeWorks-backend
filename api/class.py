from flask import jsonify, request
from . import app

@app.route('/api/class/list', methods = ['POST'])
def classList:
    param = request.get_json()
    userId = param.get('userId')
    cookie = 




    data = {
            'cookie': cookie,
            'code': 1,
            'msg': 'success',
            'userId': userId,
            'total': total,
            'classList': classList,
            }
    return jsonify(data), 200


