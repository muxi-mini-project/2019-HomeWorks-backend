from flask import jsonify, request
from . import app
from ..models import User, NoticeTimeForm
from .. import db
from ..models import generate_notice_time_id
from ..verify import token_required

# 添加提醒时间节点
@app.route('/mail/noticeTime/add/', methods=["POST"])
@token_required
def add_notice_time():
    # 是否有请求数据
    post_data = request.get_json()
    if not post_data or not post_data.get('noticeTime'):
        return jsonify({
            'msg': 'No new noticeTime'
        }), 400
    notice_time_value = post_data.get('noticeTime')

    token = request.headers.get('token')
    userId = User.get_userId_token(token)
    
    user = User.query.filter_by(userId=userId).first()
    if not user:
        return jsonify({'msg': 'No such user'}), 404

    # 排除重复时间点的添加
    records = NoticeTimeForm.query.filter_by(userId=userId).all()
    for record in records:
        if record.notice_time == notice_time_value:
            return jsonify({
                    'msg': "该时间节点已经存在"
                }), 400

    #生成时间节点id
    notice_time_id = generate_notice_time_id(userName = user.userName)
    #创建数据库新记录
    new_notice_time = NoticeTimeForm(
            userId = userId,
            notice_time = notice_time_value,
            notice_time_id = notice_time_id,
            is_active = True,
        )
    db.session.add(new_notice_time)
    db.session.commit()

    return jsonify({
            'msg': 'added successfully',
            'noticeTimeId': notice_time_id,
        }), 200


# 获取全部提醒时间节点及邮箱提醒设置
@app.route('/mail/noticeConfig/get/', methods=['GET'])
@token_required
def get_notice_time():
    token = request.headers.get('token')
    userId = User.get_userId_token(token)

    # 从数据库中获取时间节点数据
    time_get_data = NoticeTimeForm.query.filter_by(userId=userId).all()
    notice_time_list = []
    for data in time_get_data:
        time_data = {
            'noticeTime': data.notice_time,
            'noticeTimeId': data.notice_time_id,
            'noticeTimeStatus': data.is_active,
            }
        notice_time_list.append(time_data)

    # 从数据库中获取邮件提醒服务是否开启设置
    isSend = User.query.filter_by(userId=userId).first().email_send

    return jsonify({
            'msg': 'success',
            'isSend': isSend,
            'noticeTimeList': notice_time_list,
            'total': len(time_get_data),
        }), 200


# 修改时间节点
@app.route('/mail/noticeTime/<notice_time_id>/modify/', methods=['PUT'])
@token_required
def modify_notice_time(notice_time_id):
    # 是否有请求数据
    post_data = request.get_json()
    if not post_data or not post_data.get('noticeTime'):
        return jsonify({
            'msg': 'No new noticeTime'
        }), 400
    new_notice_time = post_data.get('noticeTime')

    token = request.headers.get('token')
    userId = User.get_userId_token(token)

    # 时间节点是否存在
    time_data = NoticeTimeForm.query.filter_by(
            userId=userId, notice_time_id=notice_time_id).first()
    if not time_data:
        return jsonify({
            'msg': '该时间节点不存在',
        }), 404

    time_data.notice_time = new_notice_time
    db.session.commit()

    return jsonify({
            'msg': 'modified successfully',
            'noticeTimeId': notice_time_id,
        }), 200
    

# 移除时间节点
@app.route('/mail/noticeTime/delete/', methods=['DELETE'])
@token_required
def delete_notice_time():
    # 是否有请求数据
    post_data = request.get_json()
    if not post_data or not post_data.get('noticeTimeId'):
        return jsonify({
            'msg': 'No noticeTimeId'
        }), 400
    notice_time_id = post_data.get('noticeTimeId')

    token = request.headers.get('token')
    userId = User.get_userId_token(token)

    # 时间节点是否存在
    time_data = NoticeTimeForm.query.filter_by(
            userId=userId, notice_time_id=notice_time_id).first()
    if not time_data:
        return jsonify({
            'msg': '该时间节点不存在',
        }), 404

    # 移除该条数据
    db.session.delete(time_data)
    db.session.commit()

    return jsonify({
            'msg': 'removed successfully',
        }), 200


# 改变时间节点启用状态
@app.route('/mail/noticeTime/<notice_time_id>/changeStatus/', methods=['PUT'])
@token_required
def change_notice_time_status(notice_time_id):
    token = request.headers.get('token')
    userId = User.get_userId_token(token)
 
    # 时间节点是否存在
    time_data = NoticeTimeForm.query.filter_by(
            userId=userId, notice_time_id=notice_time_id).first()
    if not time_data:
        return jsonify({
            'msg': '该时间节点不存在',
        }), 404

    time_data.is_active = not time_data.is_active
    db.session.commit()

    status = '已启用' if time_data.is_active else '已停用'
    return jsonify({
            'msg': 'success',
            'statusMessage': status,
        }), 200