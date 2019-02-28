import requests
from flask import jsonify, request
from . import app


@app.route('/api/login', method = ['POST'])
def login():
    if request.method == 'POST':
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
            url =  "http://spoc.ccnu.edu.cn/userInfo/getUserInfo"
            info = session.post(url).json()
            urerInfo = info['data']['userInfoVO']['userinfo']
            js = {
                    'code': 1,
                    'msg': 'login succeed',
                    'userInfo': {
                        'username': loginName,
                        'realname': userInfo.get('realname'),
                        'userid': userInfo.get('id'),
                        }
                    }
            return jsonify(js), 200
    else:
        return jsonify({}), 500


