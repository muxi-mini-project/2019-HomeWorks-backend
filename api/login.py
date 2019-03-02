import requests
from flask import jsonify, request
from . import app


@app.route('/api/login', methods = ['POST'])
def login():
    param = request.get_json()
    loginName = param.get('userName')
    password = param.get('password')
    payload = {
            'loginName':loginName,
            'password':password,
            }
    session = requests.session()

    url = "http://spoc.ccnu.edu.cn/userLoginController/getUserProfile"
    rp = session.post(url, data=payload)
    status_code = rp.json().get('code')
    if status_code:
        return jsonify({
                'code': 0,
                'msg': 'login fall',
                }), 400
    else:
        url =  "http://spoc.ccnu.edu.cn/userInfo/getUserInfo"
        info = session.post(url).json()
        userInfo = info['data']['userInfoVO']['userInfo']
        cookie = 'SESSION' + '=' + session.cookies.get_dict()['SESSION']
        js = {
                'code': 1,
                'msg': 'login succeed',
                'cookie': cookie,
                'userInfo': {
                    'userName': loginName,
                    'realName': userInfo.get('realname'),
                    'userId': userInfo.get('id'),
                    }
                }
        return jsonify(js), 200

