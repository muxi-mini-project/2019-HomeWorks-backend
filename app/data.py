import requests
from flask import request

from . import app, Config
from .models import User


def assign_list(cookie, userId):
    session = requests.session()
    session.cookies.set("cookies", cookie)

    # 先获取各课堂的站点Id
    header = {'cookie': cookie}
    payload = {
            'userId': userId,
            'termCode': Config.TERM,
            'pageNum': 1,
            'pageSize': 30,
            }
    url = 'http://spoc.ccnu.edu.cn/studentHomepage/getMySite'
    r = session.post(url, json=payload, headers=header)
    course_total = r.json().get('data').get('total')
    if course_total == 0:
        return False
    #total = 0
    assignList = []

    # 根据课堂站点id获取各个课堂的任务
    for i in range(course_total):
        course_list = r.json().get('data').get('list')[i]
        siteId = course_list.get('siteId')

        payload = {
                'siteId': siteId,
                'userId': userId,
                'pageNum': 1,
                'pageSize': 50,
                }
        assign_url = 'http://spoc.ccnu.edu.cn/assignment/getStudentAssignmentList'
        rp = session.post(assign_url, json=payload, headers=header)
        assign_total = rp.json().get('data').get('total')
        if not assign_total:
            continue
        #total += assign_total
        courseName = course_list.get('courseName')
        teacher = course_list.get('teacherName')

        assignments = rp.json()['data'].get('list')
        for assignment in assignments:
            assignName = assignment.get('title')
            assignId = assignment.get('id')
            status = assignment.get('status')
            beginTime = assignment.get('begintime')
            endTime = assignment.get('endtime')
            assign_data = {
                    'assignId': assignId,
                    'assignName': assignName,
                    'status': int(status),
                    'beginTime': beginTime,
                    'endTime': endTime,
                    'siteId': siteId,
                    'courseName': courseName,
                    'teacher': teacher,
                    }
            assignList.append(assign_data)

    return {
            'assignList': assignList,
            'total': len(assignList),
            'cookie': session.cookies.get_dict().get('cookies'),
            }
