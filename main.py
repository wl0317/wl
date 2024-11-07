# main.py
import redis
import pymysql
from datetime import datetime
from flask import Flask, jsonify, request, render_template
from logic import login, create_plan, select_idea, oms_audit_callback, create_idea
from utils import convert_time_range_to_numbers

app = Flask(__name__)


@app.route('/shuju')
def index():
    return render_template('APP.html')


# CORS设置：通过@after_request进行处理
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # 允许所有域进行跨域访问
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'  # 允许的HTTP方法
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'  # 允许的请求头
    response.headers['Access-Control-Allow-Credentials'] = 'true'  # 允许携带凭证
    return response


@app.route('/create_plan', methods=['POST'])
def create_ad_plan():
    try:
        # 从前端请求中获取数据
        data = request.get_json()
        user_sub_location = data.get("user_sub_location")
        user_input_date1 = data.get("user_input_date1")
        user_time_range = data.get("user_time_range")
        link = data.get("link")

        # 校验输入数据
        if not user_sub_location or not user_input_date1 or not user_time_range or not link:
            return jsonify({"error": "所有字段都是必需的"}), 400

        # 转换时段
        user_input_date = convert_time_range_to_numbers(user_time_range)

        # 登录获取用户ID和token
        token, uid = login()

        # 创建广告计划
        plan_id = create_plan(uid, token, user_sub_location, user_input_date1, user_input_date)

        # 创建广告创意
        create_idea_response = create_idea(plan_id, link, token)

        # 获取创意ID
        idea_id = select_idea(plan_id)

        # 审核通过的OMS回调
        oms_response = oms_audit_callback(plan_id, 1)  # 1表示审核通过

        return jsonify({
            "plan_id": plan_id,
            "idea_id": idea_id,
            "oms_response": oms_response.text,
            "create_idea_response": create_idea_response.text
        }), 200

    except Exception as e:
        print(f"发生错误: {e}")
        return jsonify({"error": "发生了内部错误，请稍后再试"}), 500


if __name__ == '__main__':
    is_debug = False  # True 或 False 根据需要调整
    if is_debug:
        app.run(host='127.0.0.1', port=5002, debug=True)
    else:
        app.run(host='60.205.59.6', port=8877, debug=False)
