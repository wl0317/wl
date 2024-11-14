# -*- coding: utf-8 -*-
# @Time : 2024/11/8 下午2:21
# @Author : 王雷
# @Email : eric@uxin.com
# @File : user_routes.py
# @Project : shuju

from datetime import datetime
from flask import Flask, jsonify, request, render_template
from db.queries import AccountManager
from services.user_services import Service


app = Flask(__name__)

@app.route('/shuju')
def index():
    return render_template('APP.html')

# 获取当前时间并转化化为字符串
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

@app.route('/add/gold', methods=['POST'])
def add_gold():
    """
        接口名称: add/gold
        功能: 添加红豆
        请求参数:
            - gold: 要添加的金币数量 (必填, 整数)
            - uid: 用户ID (必填, 字符串)
        返回:
            - JSON格式的响应，包含状态码和消息
        """
    gold = request.form.get('gold')
    uid = request.form.get('uid')
    # 检查参数是否为空
    if not gold or not uid:
        return jsonify({"code": "1027","message": "uid或gold不能为空","time":current_time}), 400
    # 检查uid是否存在并验证gold
    db = AccountManager()
    db.connect()
    try:
        # 尝试将gold转换为整数
        gold = int(gold)
        if gold < 0:
            return jsonify({"code": "1028","message": "gold不能为负数", "time": current_time}), 400

        # 检查uid是否存在
        if not db.fetch_one("SELECT id FROM user_info WHERE id = %s", (uid,)):
            return jsonify({"code": "1029","message": "用户不存在", "time": current_time}), 401

        # 调用add_gold方法
        return Service().add_gold(gold, uid)

    except ValueError:
        return jsonify({"code": "1030","message": "gold必须是有效的整数", "time": current_time}), 400

    except Exception as e:
        return jsonify({"code": "500", "message": str(e), "time": current_time}), 500

    finally:
        db.close()  # 确保数据库连接在处理完成后关闭

@app.route("/add/noble/gold",methods = ["POST"])
def add_noble_gold():
    """
        接口名称: add/noble/gold
        功能: 添加贵族红豆
        请求参数:
            - gold: 要添加的金币数量 (必填, 整数)
            - uid: 用户ID (必填, 字符串)
        返回:
            - JSON格式的响应，包含状态码和消息
        """
    gold = request.form.get('gold')
    uid = request.form.get('uid')
    # 检查参数是否为空
    if not gold or not uid:
        return jsonify({"code": "1027","message": "uid或gold不能为空", "time": current_time}), 400
    # 检查uid是否存在并验证gold
    db = AccountManager()
    db.connect()
    try:
        # 尝试将gold转换为整数
        gold = int(gold)
        if gold < 0:
            return jsonify({"code": "1028","message": "gold不能为负数", "time": current_time}), 400

        # 检查uid是否存在
        if not db.fetch_one("SELECT id FROM user_info WHERE id = %s", (uid,)):
            return jsonify({"code": "1029","message": "用户不存在", "time": current_time}), 401

        # 调用add_gold方法
        return Service().add_noble_gold(gold, uid)

    except ValueError:
        return jsonify({"code": "1030","message": "gold必须是有效的整数", "time": current_time}), 400

    except Exception as e:
        return jsonify({"code": "500", "message": str(e), "time": current_time}), 500

    finally:
        db.close()  # 确保数据库连接处理完成后关闭

@app.route("/add/resource/gold",methods = ["POST"])
def add_resource_gold():
    """
        接口名称: add/resource/gold
        功能: 添加资源红豆
        请求参数:
            - gold: 要添加的金币数量 (必填, 整数)
            - uid: 用户ID (必填, 字符串)
        返回:
            - JSON格式的响应，包含状态码和消息
        """
    gold = request.form.get('gold')
    uid = request.form.get('uid')
    # 检查参数是否为空
    if not gold or not uid:
        return jsonify({"code": "1027", "message": "uid或gold不能为空", "time": current_time}), 400
    # 检查uid是否存在并验证gold
    db = AccountManager()
    db.connect()
    try:
        # 尝试将gold转换为整数
        gold = int(gold)
        if gold < 0:
            return jsonify({"code": "1028", "message": "gold不能为负数", "time": current_time}), 400

        # 检查uid是否存在
        if not db.fetch_one("SELECT id FROM user_info WHERE id = %s", (uid,)):
            return jsonify({"code": "1029", "message": "用户不存在", "time": current_time}), 401

        # 调用业务逻辑处理
        return Service().add_resource_gold(gold, uid)

    except ValueError:
        return jsonify({"code": "1030", "message": "gold必须是有效的整数", "time": current_time}), 400

    except Exception as e:
        return jsonify({"code": "500", "message": str(e), "time": current_time}), 500

    finally:
        db.close()  # 确保数据库连接在处理完成后关闭

@app.route("/anchor/update",methods = ["POST"])
def update_anchor():
    """
        接口名称: /anchor/update
        功能: 认证主播
        请求参数:
            - uid: 用户ID (必填, 字符串)
        返回:
            - JSON格式的响应，包含状态码和消息
        """
    uid = request.form.get('uid')
    # 检查参数是否为空
    if not uid:
        return jsonify({"code": "1027", "message": "参数不能为空", "time": current_time}), 400
    db = AccountManager()
    db.connect()
    try:
        # 检查uid是否存在
        if not db.fetch_one("SELECT id FROM user_info WHERE id = %s", (uid,)):
            return jsonify({"code": "1029", "message": "用户不存在", "time": current_time}), 401

        # 调用add_gold方法
        return Service().update_anchor(uid)

    except Exception as e:
        return jsonify({"code": "500", "message": str(e), "time": current_time}), 500

    finally:
        db.close()  # 确保数据库连接在处理完成后关闭

@app.route("/add/exp",methods = ["POST"])
def add_exp():
    """
        接口名称: add/exp
        功能: 添加用户经验，修改等级
        请求参数:
            - exp: 要添加的经验值 (必填, 整数)
            - uid: 用户ID (必填, 字符串)
        返回:
            - JSON格式的响应，包含状态码和消息
        """
    exp = request.form.get('exp')
    uid = request.form.get('uid')
    # 检查参数是否为空
    if not exp or not uid:
        return jsonify({"code": "1027","message": "exp或uid不能为空","time":current_time}), 400
    # 检查uid是否存在并验证exp
    db = AccountManager()
    db.connect()
    try:
        # 尝试将exp转换为整数
        exp = int(exp)
        if exp < 0:
            return jsonify({"code": "1028","message": "exp不能为负数", "time": current_time}), 400

        # 检查uid是否存在
        if not db.fetch_one("SELECT id FROM user_info WHERE id = %s", (uid,)):
            return jsonify({"code": "1029","message": "用户不存在", "time": current_time}), 401

        # 调用add_exp方法
        return Service().add_exp(exp,uid)

    except ValueError:
        return jsonify({"code": "1030","message": "exp必须是有效的整数", "time": current_time}), 400

    except Exception as e:
        return jsonify({"code": "500", "message": str(e), "time": current_time}), 500

    finally:
        db.close()  # 确保数据库连接在处理完成后关闭

@app.route("/add/vip",methods = ["POST"])
def add_vip():
    """
        接口名称: add/vip
        功能: 开通会员
        请求参数:
            - uid: 用户ID (必填, 字符串)
        返回:
            - JSON格式的响应，包含状态码和消息
        """
    uid = request.form.get('uid')
    # 检查参数是否为空
    if not uid:
        return jsonify({"code": "1027","message": "uid不能为空","time":current_time}), 400
    # 检查uid是否存在
    db = AccountManager()
    db.connect()
    try:
        # 检查uid是否存在
        if not db.fetch_one("SELECT id FROM user_info WHERE id = %s", (uid,)):
            return jsonify({"code": "1029","message": "用户不存在", "time": current_time}), 401

        # 调用add_vip方法
        return Service().add_vip(uid)

    except Exception as e:
        return jsonify({"code": "500", "message": str(e), "time": current_time}), 500

    finally:
        db.close()  # 确保数据库连接在处理完成后关闭

@app.route("/del/vip",methods = ["POST"])
def del_vip():
    """
        接口名称: add/vip
        功能: 会员过期
        请求参数:
            - uid: 用户ID (必填, 字符串)
        返回:
            - JSON格式的响应，包含状态码和消息
        """
    uid = request.form.get('uid')
    # 检查参数是否为空
    if not uid:
        return jsonify({"code": "1027","message": "uid不能为空","time":current_time}), 400
    # 检查uid是否存在
    db = AccountManager()
    db.connect()
    try:
        # 检查uid是否存在
        if not db.fetch_one("SELECT id FROM user_info WHERE id = %s", (uid,)):
            return jsonify({"code": "1029","message": "用户不存在", "time": current_time}), 401

        # 调用del_vip方法
        return Service().del_vip(uid)

    except Exception as e:
        return jsonify({"code": "500", "message": str(e), "time": current_time}), 500

    finally:
        db.close()  # 确保数据库连接在处理完成后关闭

@app.route("/add/room/hot/list",methods = ["POST"])
def add_room_hot_list():
    """
        接口名称: /add/room/hot/list
        功能: 直播间添加到热门流
        请求参数:
            - roomId: 直播间Id (必填, 整数)
            - score: 排名分 (必填,整数 )
        返回:
            - JSON格式的响应，包含状态码和消息
        """
    roomId = request.form.get('roomId')
    score = request.form.get('score')
    # 检查参数是否为空
    if not roomId or not score:
        return jsonify({"code": "1027", "message": "score或roomId不能为空", "time": current_time}), 400
    # 检查roomId是否存在并验证gold
    db = AccountManager()
    db.connect()
    try:
        # 尝试将score转换为整数
        score = int(score)
        if score < 0:
            return jsonify({"code": "1028", "message": "score不能为负数", "time": current_time}), 400

        # 检查roomId是否存在
        if not db.fetch_one("SELECT room_id FROM room_info where room_id = %s ", (roomId,)):
            return jsonify({"code": "1029", "message": "roomId不存在", "time": current_time}), 401

        # 调用业务逻辑处理
        return Service().add_room_hot_list(roomId,score)

    except ValueError:
        return jsonify({"code": "1030", "message": "score必须是有效的整数", "time": current_time}), 400

    except Exception as e:
        return jsonify({"code": "500", "message": str(e), "time": current_time}), 500

    finally:
        db.close()  # 确保数据库连接在处理完成后关闭

@app.route("/del/room/hot/list",methods = ["POST"])
def del_room_hot_list():
    """
        接口名称: /del/room/hot/list
        功能: 直播间从热门流移除
        请求参数:
            - roomId: 直播间Id (必填, 整数)
        返回:
            - JSON格式的响应，包含状态码和消息
        """
    roomId = request.form.get('roomId')
    # 检查参数是否为空
    if not roomId:
        return jsonify({"code": "1027", "message": "roomId不能为空", "time": current_time}), 400
    # 检查roomId是否存在
    db = AccountManager()
    db.connect()
    try:
        # 检查roomId是否存在
        if not db.fetch_one("SELECT room_id FROM room_info where room_id = %s ", (roomId,)):
            return jsonify({"code": "1029", "message": "roomId不存在", "time": current_time}), 401

        # 调用业务逻辑处理
        return Service().del_room_hot_list(roomId)

    except ValueError:
        return jsonify({"code": "1030", "message": "score必须是有效的整数", "time": current_time}), 400

    except Exception as e:
        return jsonify({"code": "500", "message": str(e), "time": current_time}), 500

    finally:
        db.close()  # 确保数据库连接在处理完成后关闭

@app.route("/add/intimacy",methods = ["POST"])
def add_intimacy():
    """
        接口名称: /add/intimacy
        功能: 加亲密度
        请求参数:
            - userId: 主播id(必填, 整数)
            - score: 排名分 (必填,整数 )
            - uid: 用户id (必填,整数 )

        返回:
            - JSON格式的响应，包含状态码和消息
        """
    userId = request.form.get('userId')
    score = request.form.get('score')
    uid = request.form.get("uid")
    # 检查参数是否为空
    if not userId or not score or not uid:
        return jsonify({"code": "1027", "message": "参数错误", "time": current_time}), 400
    # 检查userId是否存在并验证score
    db = AccountManager()
    db.connect()
    try:
        # 尝试将score转换为整数
        score = int(score)
        if score < 0:
            return jsonify({"code": "1028", "message": "score不能为负数", "time": current_time}), 400

        # 检查userId是否存在
        if not db.fetch_one("SELECT id FROM user_info where id = %s ", (userId,)):
            return jsonify({"code": "1029", "message": "主播不存在", "time": current_time}), 401

        # 检查uid是否存在
        if not db.fetch_one("SELECT id FROM user_info WHERE id = %s", (uid,)):
            return jsonify({"code": "1029", "message": "用户不存在", "time": current_time}), 401

        # 调用业务逻辑处理
        return Service().add_intimacy(userId,score,uid)

    except ValueError:
        return jsonify({"code": "1030", "message": "score必须是有效的整数", "time": current_time}), 400

    except Exception as e:
        return jsonify({"code": "500", "message": str(e), "time": current_time}), 500

@app.route("/audit/drama",methods = ["POST"])
def audit_drama():
    """
        接口名称: audit/drama
        功能: 审核接口
        请求参数:
            - status: 审核状态 3：审核通过 4：审核拒绝 (必填, 整数)
            - contentId: 剧、集id (必填, 字符串)
        返回:
            - JSON格式的响应，包含状态码和消息
    """
    contentId = request.form.get('contentId')
    status = request.form.get('status')

    # 检查参数是否为空
    if not contentId or not status:
        return jsonify({"code": "1027", "message": "参数不能为空", "time": current_time}), 400

    # 将status转换为整数
    status = int(status)

    db = AccountManager()
    db.connect()
    try:
        # 检查contentId是否存在
        if not db.fetch_all('select * from drama_audit_info where status=2 and content_id=%s', (contentId,)):
            return jsonify({"code": "1029", "message": "contentId不存在", "time": current_time}), 401

        # 检查status是否为3或4
        if status != 3 and status != 4:
            return jsonify({"code": "1027", "message": "参数错误", "time": current_time}), 401

        # 调用audit_drama方法
        return Service().audit_drama(contentId, status)

    except Exception as e:
        return jsonify({"code": "500", "message": str(e), "time": current_time}), 500

    finally:
        db.close()  # 数据库连接在处理完成后关闭

@app.route("/user/forbiduser",methods = ["POST"])
def user_forbid():
    """
        接口名称: /user/forbidUser
        功能: 用户解封/封禁接口
        请求参数:
            - status: 用户状态 1：接禁状态 0：封禁状态 (必填, 整数)
            - uid: 用户id (必填, 字符串)
        返回:
            - JSON格式的响应，包含状态码和消息
    """
    uid = request.form.get('uid')
    status = request.form.get('status')

    # 检查参数是否为空
    if not uid or not status:
        return jsonify({"code": "1027", "message": "参数不能为空", "time": current_time}), 400

    # 将status转换为整数
    status = int(status)
    db = AccountManager()
    db.connect()
    try:
        # 检查uid是否存在
        if not db.fetch_one("SELECT id FROM user_info WHERE id = %s", (uid,)):
            return jsonify({"code": "1029", "message": "用户不存在", "time": current_time}), 401
        # 检查status是否为0或1
        if status != 0 and status != 1:
            return jsonify({"code": "1027", "message": "参数错误", "time": current_time}), 401

        # 调用audit_drama方法
        return Service().user_forbid(uid, status)

    except Exception as e:
        return jsonify({"code": "500", "message": str(e), "time": current_time}), 500


@app.route('/create/room', methods=['POST'])
def create_room():
    phone = request.form.get('phone')
    if not phone:
        return jsonify({"error": "手机号不能为空"}), 400

    return Service().create_room(phone)


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

