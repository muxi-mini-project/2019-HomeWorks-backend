import requests
from flask import jsonify, request
from . import app
from ..verify import verify_siteId
from ..models import User

@app.route('/course/list/', methods = ['GET'])
def courseList():
    cookie = request.headers.get('cookie')
#    userId = request.get_json().get('userId')
    token = request.headers.get('token')
#    if cookie is None:
    if not cookie:
        return jsonify({
                "msg": "No cookie"
                }), 400
    if not token:
        return jsonify({
                'msg': 'No token'
                }), 400

    userId = User.get_userId_token(token)
    if not userId:
        return jsonify({
                'msg': 'Invalid token'
                }), 401

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
    courseList = []
    for i in range(total):
        course = {}
        course['courseName'] = data_list[i].get('courseName')
        course['teacher'] = data_list[i].get('teacherName')
        course['siteId'] = data_list[i].get('siteId')
        courseList.append(course)

    cookie = session.cookies.get_dict()['cookies']
    data = {
            'cookie': cookie,
            'msg': 'Successfully login',
            'total': total,
            'courseList': courseList,
            }
    return jsonify(data), 200


@app.route('/course/<siteId>/assignment/list/', methods=['GET'])
def oneClassAssign(siteId):
    cookie = request.headers.get('cookie')
    if not cookie:
        return jsonify({
            'msg': 'No cookie'}), 400

    token = request.headers.get('token')
    if not token:
        return jsonify({
            'msg': 'No token'}), 400

    userId = User.get_userId_token(token)
    if not userId:
        return jsonify({
            'msg': 'Invalid token'}), 401

    if not verify_siteId(siteId, userId):
        return jsonify({
            'msg': 'Wrong siteId'}), 404

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
    rp_data = r.json().get('data')
    total = rp_data.get('total')
    data = []
    for i in range(total):
        t = rp_data.get('list')[i]
        course_data = {
                'status': t.get('status'),
                'assignName': t.get('title'),
                'assignId': t.get('id'),
                'beginTime': t.get('begintime'),
                'endTime': t.get('endtime'),
                }
        data.append(course_data)

    cookie = session.cookies.get_dict()['cookies']
    js_data = {
            'cookie': cookie,
            'msg': 'successful',
            'siteId': siteId,
            'total': total,
            'data': data,
            }
    return jsonify(js_data), 200

