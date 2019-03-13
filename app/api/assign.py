from . import app
import requests
from flask import jsonify, request

@app.route('/assignment/list/', methods=['GET'])
def assignList():
    cookie = request.headers.get('cookie')
    token = request.headers.get('token')
    if not cookie:
        return jsonify({'msg': 'No cookie'}), 400
    if not token:
        return jsonify({'msg': 'No token'}), 400

    session = requests.session()
    session.cookies.set('cookies', cookie)

    url = ''


    assignList = []


    return jsonify({
            'msg': 'success',
            'cookie': session.cookies.get_dict().get('cookies'),
            'total': total,
            'assignList': assignList,
        }), 200


@app.route('/assignment/<siteId>/<assignId>/info/', methods=['GET'])
def assignInfo():
    pass
