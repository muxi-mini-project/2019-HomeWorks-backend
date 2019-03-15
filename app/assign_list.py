from . import app
from flask import request
import requests

def assign_list(cookie, userId):
    session = requests.session()
    session.cookies.set("cookies", cookie)

    header = {'cookie': cookie}
    payload = {
            'userId': userId,
            'termCode': '201901',
            'pageNum': 1,
            'pageSize': 30,
            }
    url = 'http://spoc.ccnu.edu.cn/studentHomepage/getMySite'
    r = session.post(url, json=payload, headers=header)
    course_total = r.json().get('data').get('total')
    total = 0
    assignList = []
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
        total = total + assign_total
        courseName = course_list.get('courseName')
        teacher = course_list.get('teacherName')

        for j in range(assign_total):
            assignment = rp.json()['data'].get('list')[j]
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
                'total': total,
                'cookie': session.cookies.get_dict().get('cookies'),
                }

