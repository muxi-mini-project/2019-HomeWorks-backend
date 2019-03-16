from . import app
from flask import request
import requests
from .models import User

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


def course_list(cookie, userId):
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
    for element in data_list:
        course = {}
        course['courseName'] = element.get('courseName')
        course['teacher'] = element.get('teacherName')
        course['siteId'] = element.get('siteId')
        courseList.append(course)

    cookie = session.cookies.get_dict()['cookies']
    
    return {
            'cookie': cookie,
            'total': total,
            'courseList': courseList,
            }

def assign_info(cookie, userId, siteId, assignId):
    session = requests.session()
    session.cookies.set('cookies', cookie)

    header = {'cookie': cookie}
    url = 'http://spoc.ccnu.edu.cn/siteController/getSiteBySiteId?siteId=' \
            + siteId
    courseName = session.post(url, headers=header).json().get('data').get('siteName')

    url = 'http://spoc.ccnu.edu.cn/assignment/getStudentAssignmentList'
    payload = { 
            'siteId': siteId,
            'userId': userId,
            'pageNum': 1,
            'pageSize': 50, 
            }
    assign_list = session.post(url, json=payload, headers=header).json()\
            .get('data').get('list')
    check_assignId = False
    for data in assign_list:
        if assignId != data.get('id'):
            continue
        personalPoint = data.get('personalPoint')
        groupPoint = data.get('groupPoint')
        studentNum = data.get('studentNum')
        groupNum = data.get('groupNum')
        pointNum = data.get('pointNum')
        commitNum = data.get('commitNum')

        check_assignId = True
        break

    if not check_assignId:
        return 0

    url = 'http://spoc.ccnu.edu.cn/assignment/getAssignmentInfoByStudent/' \
            + assignId + '/' + userId
    cer_info = session.post(url, headers=header).json().get('data')

    assignAttachment = []
    for attachment in cer_info.get('assignmentAttachment') or []: 
        dt = { 
                'id': attachment.get('id'),
                'name': attachment.get('attachmentName'),
                'ext': attachment.get('ext'),
                'sourceUrl': attachment.get('sourceUrl'),
                }
        assignAttachment.append(dt)
    submitAttachment = []
    for attachment in cer_info.get('submitAttachment') or []: 
        dt = { 
                'id': attachment.get('id'),
                'name': attachment.get('attachmentName'),
                'uploadTime': attachment.get('uploadTime'),
                'ext': attachment.get('ext'),
                'sourceUrl': attachment.get('sourceUrl'),
                }
        submitAttachment.append(dt)
    return_data = {
            "msg": 'success',
            "cookie": session.cookies.get_dict()['cookies'],
            "siteId": siteId,
            "assignId": assignId,
            "courseName": courseName,
            "assignName": cer_info.get('title'),
            "status": int(cer_info.get('status')),
            "beginTime": cer_info.get('begintime'),
            "endTime": cer_info.get('endtime'),
            "content": cer_info.get('content'),                 #作业要求，颁布的作业
            "pointNum": pointNum,                               #已批阅数
            "commitNum": commitNum,
            "isGroup": int(cer_info.get('isgroup')),            #是否分组
            "groupNum": cer_info.get('groupNum'),
            "studentNum": studentNum,
            "groupPoint": groupPoint,
            "personalPoint": personalPoint,
            "feedback": cer_info.get('assignmentSubmit')[0].get('feedback'),    #反馈
            "assignAttachmentNum": cer_info.get('assignmentAttachmentNum'),     #作业要求的附件数
            "assignAttachment": assignAttachment,
            "submitAttachmentNum": cer_info.get('assignmentSubmitNum'),         #提交的附件数
            "submitAttachment": submitAttachment,
            "submitContent": cer_info.get('assignmentSubmit')[0].get('content'),
            #作业内容，提交的作业
        }

    return {
            'cookie': cookie,
            "assign_info": return_data,
            }
