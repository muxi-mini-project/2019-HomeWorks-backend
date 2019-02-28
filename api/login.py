import requests
from flask import jsonify, request
from . import app


@app.route('/api/login', method = ['POST'])
def login():
    param = request.get_json()
    loginName = param.get('loginName')
    password = param.get('password')
    payload = {
            'loginName':loginName,
            'password':password,
            }
    session = requests.session()

    url = "http://spoc.ccnu.edu.cn/userLoginController/getUserProfile"
    rp = session.post(url, data=payload)
    status_code = rp.json().get('msg')
    if status_code:
        return jsonify({
                'code': 0,
                'msg': 'login fall',
                }), 400
    else:
        js = {
                'code': 1,
                'msg': 'login succeed',
                'loginName': loginName
                }
        return jsonify(js), 200


