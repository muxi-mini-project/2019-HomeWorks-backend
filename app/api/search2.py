import requests
from flask import jsonify, request
from . import app
from ..models import User

@app.route('/search2/', methods=['GET'])
def search2():
    cookie = request.headers.get('cookie')
    token = request.headers.get('token')
    keyword = request.args.get('keyword')
    if not cookie:
        return jsonify({
                'msg': 'No cookie'}), 400 
    if not token:
        return jsonify({
                'msg': "No token"}), 400 
    if not keyword:
        return jsonify({
                'msg': 'No keyword'}), 400 
    userId = User.get_userId_token(token)
    if not userId:
        return jsonify({
                'msg': 'Invalid token'}), 401 

    session = requests.session()
    session.cookies.set('cookies', cookie)
    
    total = 0
    course_data = []
    assign_data = []
    content_data = []

    header = {'cookie': cookie}
    payload = {
            'userId': userId,
            'termCode': '201901',
            'pageNum': 1,
            'pageSize': 30,
            }
    url = 'http://spoc.ccnu.edu.cn/studentHomepage/getMySite'
    r = session.post(url, json = payload, headers=header)
    data_list = r.json().get('data').get('list')
    for course in data_list:
        courseName = course.get('courseName')
        siteId = course.get('siteId')
        if keyword in courseName:
            c = {}
            c['courseName'] = courseName
            c['siteId'] = siteId
            course_data.append(c)
            total = total + 1
        
        cookie = session.cookies.get_dict().get('cookies')
        url = 'http://spoc.ccnu.edu.cn/assignment/getStudentAssignmentList'
        payload = { 
                'siteId': siteId,
                'userId': userId,
                'pageNum': 1,
                'pageSize': 50, 
                }
        rp = session.post(url, json=payload, headers=header)
        assign_get_list = rp.json().get('data').get('list')
        for task in assign_get_list:
            assignName = task.get('title')
            if keyword in assignName:
                total = total + 1
                js = {
                        'assignId': task.get('id'),
                        'siteId': siteId,
                        'assignName': assignName,
                        'courseName': courseName,
                        }
                assign_data.append(js)
            if keyword in task.get('content'):
                total = total + 1
                js = {
                        'assignId': task.get('id'),
                        'siteId': siteId,
                        'assignName': assignName,
                        'courseName': courseName,
                        }
                content_data.append(js)

    return_data = {
                'msg': 'success', 
                'cookie': session.cookies.get_dict().get('cookies'),
                'total': total,
                'course_data': course_data,
                'assign_data': assign_data,
                'content_data': content_data,
            }
    return jsonify(return_data), 200

