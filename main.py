# -*- coding: utf-8 -*-
# @Time : 2024/10/29 下午4:40
# @Author : 王雷
# @Email : eric@uxin.com
# @File : add.py
# @Project : autoUI

import redis
import pymysql
from datetime import datetime
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/shuju')
def index():
    return render_template('APP.html')

class AccountManager:
    def __init__(self):
        self.redis_client = redis.Redis(host='60.205.59.6', port=6326, db=0, password="uxin001")
        self.redis_client1 = redis.Redis(host='60.205.59.6', port=6333, db=0, password="uxin001")

    def connect(self):
        """建立数据库连接"""
        try:
            self.connection = pymysql.connect(
                host="60.205.59.6",
                user="root",
                password="uxin.com",
                port=3306,
                charset="utf8",
                database="uxinlive"
            )
        except pymysql.MySQLError as e:
            print(f"连接 MySQL 时出错: {e}")

    def fetch_one(self, query, params=None):
        """查询单条数据"""
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()

    def fetch_all(self, query, params=None):
        """查询所有数据"""
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()

    def execute(self, query, params=None):
        """执行插入、更新和删除操作"""
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or ())
            self.connection.commit()

    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()

    def add_gold(self, gold, uid):
        try:
            db = AccountManager()
            db.connect()
            sql = "UPDATE account_balance SET gold = %s WHERE uid = %s"
            db.execute(sql, (gold, uid))
            self.redis_client.delete("balance_account_gold_{}".format(uid))
            self.redis_client1.delete("balance_item_{}".format(uid))
            result = db.fetch_one("SELECT gold FROM account_balance WHERE uid = %s", (uid,))
            list1 = list(result)
            re = self.redis_client.get("balance_account_gold_{}".format(uid))
            rs = self.redis_client1.get("balance_item_{}".format(uid))
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if re is None and rs is None:
                for i in list1:
                    if i == int(gold):
                        return jsonify({"code": "200", "message": "红豆已更新成功", "time": current_time}), 200
                    else:
                        return jsonify({"message": "数据库更新失败，没有行受到影响", "time": current_time}), 400
        except Exception as e:
            return jsonify({"error": "发生错误: {}".format(str(e))}), 500
        finally:
            db.close()


@app.route('/add_gold', methods=['POST'])
def add_gold():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    gold = request.form.get('gold')
    uid = request.form.get('uid')

    if not gold or not uid:
        return jsonify({"error": "uid或gold不能为空", "time": current_time}), 400

    db = AccountManager()
    db.connect()
    res = db.fetch_one("SELECT id FROM user_info WHERE id = %s", (uid,))

    try:
        gold = int(gold)
        if gold < 0:
            return jsonify({"error": "gold不能为负数", "time": current_time}), 400
    except ValueError:
        return jsonify({"error": "gold必须是有效的整数", "time": current_time}), 400

    if res is None:
        return jsonify({"error": "用户不存在", "time": current_time}), 401

    return AccountManager().add_gold(gold, uid)



# CORS设置：通过@after_request进行处理
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # 允许所有域进行跨域访问
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'  # 允许的HTTP方法
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'  # 允许的请求头
    response.headers['Access-Control-Allow-Credentials'] = 'true'  # 允许携带凭证
    return response


if __name__ == '__main__':
    is_debug = False  # True 或 False 根据需要调整
    if is_debug:
        app.run(host='127.0.0.1', port=5002, debug=True)
    else:
        app.run(host='60.205.59.6', port=8877, debug=False)
