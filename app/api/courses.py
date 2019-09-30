import requests
from flask import jsonify, request

from ..models import User
from ..verify import token_required, verify_siteId
from .. import Config
from . import app


@app.route('/course/list/', methods = ['GET'])
@token_required
def courseList():
    cookie = request.headers.get('cookie')
    token = request.headers.get('token')

    if not cookie:
        return jsonify({
                "msg": "No cookie"
                }), 400

    userId = User.get_userId_token(token)

    header = {'cookie': cookie}
    payload = {
            'userId': userId,
            'termCode': Config.TERM,
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
    for element in data_list:
        course = {}
        course['courseName'] = element.get('courseName')
        course['teacher'] = element.get('teacherName')
        course['siteId'] = element.get('siteId')
        courseList.append(course)

    cookie = session.cookies.get_dict()['cookies']
    data = {
            'cookie': cookie,
            'msg': 'Success',
            'total': total,
            'courseList': courseList,
            }
    return jsonify(data), 200


@app.route('/course/<siteId>/assignment/list/', methods=['GET'])
@token_required
def oneClassAssign(siteId):
    cookie = request.headers.get('cookie')
    if not cookie:
        return jsonify({
            'msg': 'No cookie'}), 400

    token = request.headers.get('token')
    userId = User.get_userId_token(token)

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
    for element in rp_data.get('list'):
        course_data = {
                'status': int(element.get('status')),
                'assignName': element.get('title'),
                'assignId': element.get('id'),
                'beginTime': element.get('begintime'),
                'endTime': element.get('endtime'),
                }
        data.append(course_data)

    cookie = session.cookies.get_dict()['cookies']
    js_data = {
            'cookie': cookie,
            'msg': 'success',
            'siteId': siteId,
            'total': total,
            'data': data,
    }
    return jsonify(js_data), 200
