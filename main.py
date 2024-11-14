# main.py
from routes.user_routes import app

if __name__ == '__main__':
    # 启动应用，调试模式或生产模式可以根据需求进行配置
    is_debug = False  # 根据需求修改
    if is_debug:
        app.run(host='127.0.0.1', port=5002, debug=True)
    else:
        app.run(host='60.205.59.6', port=8877, debug=False)
