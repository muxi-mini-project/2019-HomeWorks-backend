from . import app
import requests
from flask import jsonify, request
from ..models import User
from ..verify import verify_siteId
from ..data import assign_list

@app.route('/assignment/list/', methods=['GET'])
def assignList():
    cookie = request.headers.get('cookie')
    token = request.headers.get('token')
    if not cookie:
        return jsonify({'msg': 'No cookie'}), 400
    if not token:
        return jsonify({'msg': 'No token'}), 400

    userId = User.get_userId_token(token)
    if not userId:
        return jsonify({'msg': 'Invalid token'}), 401

    data = assign_list(cookie, userId)
    return_data = {
                'msg': 'success',
                'cookie': data.get('cookie'),
                'total': data.get('total'),
                'assignList': data.get('assignList'),
            }
    return jsonify(return_data), 200


@app.route('/assignment/<siteId>/<assignId>/info/', methods=['GET'])
def assignInfo(siteId, assignId):
    cookie = request.headers.get('cookie')
    token = request.headers.get('token')
    if not cookie:
        return jsonify({
                'msg': 'No cookie'
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

    if not verify_siteId(siteId, userId):
        return jsonify({
                'msg': 'Invalid siteId'
            }), 404

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
        return jsonify({
                'msg': 'Invalid assignId'
            }), 404

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

    return jsonify(return_data), 200

