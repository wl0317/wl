# logic.py
import random
import requests
from config import BASE_URL, OMS_URL
from database import Database


# 生成广告计划名称
def generate_name():
    numbers_batch = list(range(100000, 999999))
    random.shuffle(numbers_batch)
    return ''.join(map(str, numbers_batch[:6]))


# 转换时间段为数字
def convert_time_range_to_numbers(time_range):
    start_time, end_time = map(lambda x: tuple(map(int, x.split(':'))), time_range.split('-'))
    start_number = start_time[0] * 6 + start_time[1] // 10
    end_number = end_time[0] * 6 + end_time[1] // 10
    return ",".join(map(str, range(start_number, end_number + 1)))


# 获取数据库中的广告创意ID
def select_idea(planId: int):
    conn = Database.mysql_login()
    sql = "SELECT id FROM adv_idea_info WHERE adv_plan_id = %s"
    cur = conn.cursor()
    cur.execute(sql, (planId,))
    result = cur.fetchall()
    Database.close_connection(conn)

    if result:
        return result[0]['id']
    return None


# 处理JSON响应
def process_json_response(response):
    try:
        json_response = response.json()
        print("JSON Response:", json_response)
        return json_response.get('result')
    except ValueError:
        print("Response is not in JSON format.")
        return None


# 登录函数
def login():
    url = BASE_URL + '/user/cellPhoneLogin'
    header = {'Content-Type': 'application/x-www-form-urlencoded', '_c': '19'}
    data = {'code': '1111', 'mobile': 17316103505, 'source': '86'}

    response = requests.post(url=url, data=data, headers=header)
    token = response.headers.get('x-auth-token')
    user_data = response.json().get('b', {})
    uid = user_data.get('id', None)

    if token:
        print("Login successful, User ID:", uid)
        return token, uid
    else:
        print("Login failed")
        return None, None


# 添加广告计划
def add_advertisement_plan(token, uid, name_value, user_sub_location, user_input_date1, user_input_date, link):
    url = BASE_URL + '/adv/plan/add'
    headers = {
        'Content-Type': 'application/json',
        'masterId': str(uid),
        '_c': '19',
        'appId': '12',
        'x-auth-token': token
    }
    data = {
        "resourceLocation": {"appId": "0", "location": "8", "subLocation": user_sub_location},
        "source": 1,
        "createUid": 3694377177090,
        "groupId": "1940626332392095746",
        "name": name_value,
        "launchSchedule": [{"theDay": user_input_date1, "segments": user_input_date.split(',')}],
        "masterId": 3694377177090
    }

    response = requests.post(url, json=data, headers=headers)
    return process_json_response(response)


# 审核广告计划
def audit_advertisement_plan(plan_id, token):
    url = BASE_URL + '/adv/plan/audit'
    data = {'id': plan_id}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'masterId': '3694377177090',
        '_c': '19',
        'appId': '12',
        'x-auth-token': token
    }
    response = requests.post(url, headers=headers, data=data)
    return process_json_response(response)


# 创建广告创意
def create_advertisement_idea(plan_id, token, link):
    url = BASE_URL + '/adv/idea/create'
    headers = {
        'Content-Type': 'application/json',
        'masterId': '3694377177090',
        '_c': '19',
        'appId': '12',
        'x-auth-token': token,
        'identify': 'uxid=55935e23f2ee4d51abc67afdad6cfafa',
    }
    data = {
        "planId": plan_id,
        "resource": {
            "baseList": [
                {"type": 1, "width": 245, "height": 200, "url": "https://img.kilamanbo.com/adv/1701240521091843.png"}]
        },
        "copyInfo": {},
        "marketVal": link,
        "marketObj": 2,
        "review": "审核说明"
    }
    response = requests.post(url, headers=headers, json=data)
    return process_json_response(response)


# 回调处理创意审核
def callback_advertisement_idea(id, status):
    url = OMS_URL + '/adv/idea/audit/callback'
    data = {'id': id, 'status': status}
    response = requests.post(url, data=data)
    return process_json_response(response)
