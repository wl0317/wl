#main.py
import redis
import pymysql
from datetime import datetime
from flask import Flask, jsonify, request, render_template

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


if __name__ == '__main__':
    is_debug = False  # True 或 False 根据需要调整
    if is_debug:
        app.run(host='127.0.0.1', port=5002, debug=True)
    else:
        app.run(host='60.205.59.6', port=8877, debug=False)
