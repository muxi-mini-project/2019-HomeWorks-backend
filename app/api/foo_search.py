# 放弃的搜索版本

from flask import jsonify, request
from . import app
from ..models import User
from ..data import assign_list


@app.route('/search/', methods=['GET'])
def search():
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

    total = 0

    course_get_data = course_list(cookie, userId)
    course_list_data = course_get_data.get('courseList')
    course_data = []
    for course in course_list_data:
        if keyword in course.get('courseName'):
            course_data.append(course)
            total = total + 1
    cookie = course_get_data.get('cookie')

    assign_get_data = assign_list(cookie, userId)
    assign_list_data = assign_get_data.get('assignList')
    assign_data = []
    content_data =[]
    for task in assign_list_data:
        if keyword in task.get('assignName'):
            assign_data.append(task)
            total = total + 1
        assignId = task.get('assignId')
        siteId = task.get('siteId')
        cookie = assign_get_data.get('cookie')

        info_get_data = assign_info(cookie, userId, siteId, assignId)
        assign_info_data = info_get_data.get('assign_info')
        if keyword in assign_info_data.get('content'):
            content_data.append(assign_info_data)
            total = total + 1
        cookie = info_get_data.get('cookie')

    return_data = {
                'msg': 'success',
                'total': total,
                'cookie': cookie,
                'assign_data': assign_data,
                'course_data': course_data,
                'content_data': content_data,
            }
    return jsonify(return_data), 200
