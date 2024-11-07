# logic.py
import requests
import random
from database import Database
from config import BASE_URL, OMS_URL


def login():
    """登录并获取token和用户ID"""
    url = BASE_URL + '/user/cellPhoneLogin'
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        '_c': '19'
    }
    data = {
        'code': '1111',
        'mobile': 17316103505,
        'source': '86'
    }
    re = requests.post(url=url, data=data, headers=header)
    re_data = re.json()
    token = re.headers.get('x-auth-token')
    uid = re_data.get('b', {}).get('id', None)
    if token:
        print(f"登录成功, 用户ID: {uid}")
    else:
        print("登录失败")
    return token, uid


def create_plan(uid, token, user_sub_location, user_input_date1, user_input_date):
    """创建广告计划并返回计划ID"""
    url = BASE_URL + '/adv/plan/add'
    header = {
        'Content-Type': 'application/json',
        'masterId': f"{uid}",
        '_c': '19',
        'appId': '12',
        'x-auth-token': token
    }

    # 随机生成广告计划名称
    name_value = ''.join(map(str, random.sample(range(100000, 999999), 6)))

    data = {
        "resourceLocation": {
            "appId": "0",
            "location": "8",
            "subLocation": user_sub_location,
            "interactionForm": "1",
            "promotionScope": {
                "roomRecommendPos": {
                    "roomType": "3",
                    "contentIds": "",
                    "userType": "1"
                }
            }
        },
        "source": 1,
        "createUid": 3694377177090,
        "groupId": "1940626332392095746",
        "name": name_value,
        "launchSchedule": [
            {
                "theDay": user_input_date1,
                "segments": user_input_date.split(',')
            }
        ],
        "masterId": 3694377177090
    }

    response = requests.post(url=url, json=data, headers=header)
    plan_id = response.json().get('b', {}).get('id')
    print(f"创建广告计划成功，计划ID: {plan_id}")
    return plan_id


def select_idea(planId: int):
    """从数据库中选择广告创意"""
    conn = Database.mysql_login()
    if conn:
        sql = "SELECT id FROM adv_idea_info WHERE adv_plan_id = %s"
        cur = conn.cursor()
        cur.execute(sql, (planId,))
        result = cur.fetchall()
        for row in result:
            idea_id = row['id']
            print(f"选取的创意ID: {idea_id}")
            Database.close_connection(conn)
            return idea_id
    else:
        print("数据库连接失败")
        return None


def oms_audit_callback(plan_id, status):
    """OMS回调审核"""
    url = f"{OMS_URL}/adv/plan/audit/callback"
    data = {
        'id': plan_id,
        'status': status
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, headers=headers, data=data)
    return response


def create_idea(plan_id, link, token):
    """创建广告创意"""
    url = BASE_URL + '/adv/idea/create'
    header = {
        'Content-Type': 'application/json',
        'masterId': '3694377177090',
        '_c': '19',
        'appId': '12',
        'x-auth-token': token,
        'identify': 'uxid=55935e23f2ee4d51abc67afdad6cfafa'
    }
    data = {
        "planId": plan_id,
        "resource": {
            "baseList": [
                {
                    "type": 1,
                    "width": 245,
                    "height": 200,
                    "url": "https://img.kilamanbo.com/adv/1701240521091843.png"
                }
            ]
        },
        "copyInfo": {},
        "marketVal": link,
        "marketObj": 2,
        "review": "审核说明"
    }
    response = requests.post(url, headers=header, json=data)
    return response
