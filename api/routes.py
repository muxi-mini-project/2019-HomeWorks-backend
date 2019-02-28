import requests
from flask import jsonify, request
from . import app
#from flask import login_required

def logincheck(loginname, password, verifcode):
    url = "http://spoc.ccnu.edu.cn/starmoocHomepage"
    data = {
            "loginname":loginname,
            'password':password,
            'verifcode':verifcode
            }
    r = requests.post(url, data=data)
    check = r.headers.get('Location') or ''
    if check:
        return True
    else:
        return False
    
@app.route('/login', methods = ['POST', 'GET'])
#def login(loginname, password, verifcode):
def login():
    jv = request.get_json()
#    if not jv:
#        return ' ', 401
    loginname = jv.get('loginname')
    password = jv.get('password')
    verifcode = jv.get('verifcode')

    check = logincheck(loginname, password, verifcode)
    if check is True:
        data = {
                'loginname':loginname,
                'message': 'login succeed'
                }
        return jsonify(data), 200
    else:
        return jsonify({'message': 'login fall'}), 401

@app.route('/index')
@app.route('/')
def index():
    return 'ok'
