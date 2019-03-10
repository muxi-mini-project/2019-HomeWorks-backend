import requests
from flask import jsonify, request
from . import app

@app.route('/api/class/list', methods = ['POST'])
def classList():
    param = request.get_json()
    userId = param.get('userId')
    cookie = request.headers.get('cookie')
    if cookie is None:
        return jsonify({
                "msg": "Invalid Cookie"
            }), 400
    header = {'cookie': cookie}
    payload = {
            'userId': userId,
            'termCode': '201901',
            'pageNum': 1,
            'pageSize': 30,
            }

    url = 'http://spoc.ccnu.edu.cn/studentHomepage/getMySite'
    session = requests.session()
    session.cookies.set('cookies', cookie)

    r = session.post(url, json = payload, headers=header)
    data_list = r.json().get('data').get('list')
    total = r.json().get('data').get('total')
    classList = []
    for i in range(total):
        course = {}
        course['className'] = data_list[i].get('courseName')
        course['teacher'] = data_list[i].get('teacherName')
        course['siteId'] = data_list[i].get('siteId')
        classList.append(course)

    cookie = session.cookies.get_dict()['cookies']
    data = {
            'cookie': cookie,
            'code': 1,
            'msg': 'successfully login',
            'userId': userId,
            'total': total,
            'classList': classList,
            }
    return jsonify(data), 200


