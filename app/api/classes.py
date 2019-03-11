import requests
from flask import jsonify, request
from . import app

@app.route('/api/class/list', methods = ['POST'])
def classList():
    userId = request.get_json().get('userId')
    cookie = request.headers.get('cookie')
    if cookie is None:
        return jsonify({
                "msg": "Invalid Cookie"
            }), 400
    if userId is None:
        return jsonify({
                'msg': 'Invalid userId'
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

@app.route('/api/class/assignment/', methods=['POST'])
def oneClassAssign():
    json = request.get_json()
    userId = json.get('userId')
    siteId = json.get('siteId')
    if userId is None or siteId is None:
        return jsonify({'msg': 'Invalid userId or siteId'}), 400
    cookie = request.header.get('cookie')
    if cookie is None:
        return jsonify({'msg': 'Invalid cookie'}), 400
    session = requests.session()
    session.cookies.set('cookies', cookie)

    url = 'http://spoc.ccnu.edu.cn/assignment/getStudentAssignmentList'
    header = {'cookie': cookie}
    payload = {
            'userId': userId,
            'siteId': siteId,
            'pageNum': 1,
            'pageSize': 30
            }
    r = session.post(url, json=payload, headers=header)

    data = []



    cookie = session.cookies.get_dict()['cookies']
    js_data = {
            'cookie': cookie,
            'code': 1,
            'msg': 'successful'
            'userId': userId,
            'siteId': siteId,
            'total': total,
            'data': data,
            }
    return jsonify(js_data), 200

