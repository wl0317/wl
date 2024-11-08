# -*- coding: utf-8 -*-
# @Time : 2024/11/8 下午2:25
# @Author : 王雷
# @Email : eric@uxin.com
# @File : user_services.py
# @Project : shuju

import json,requests,redis,datetime
from db.queries import AccountManager
from flask import Flask,jsonify,request
from datetime import datetime


class Service():

    def __init__(self):
        self.redis_client = redis.Redis(host='60.205.59.6', port=6326, db=0, password="uxin001")
        self.redis_client1 = redis.Redis(host='60.205.59.6', port=6333, db=0, password="uxin001")
        self.redis_6330 = redis.Redis(host='60.205.59.6', port=6330, db=0, password="uxin001")
        self.redis_6325 = redis.Redis(host='60.205.59.6', port=6325, db=0, password="uxin001")
        self.H5_redis = redis.Redis(host='redis-h5test.uxin001.com', port=16660, db=0, password="Kila@2019")
        self.current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def add_gold(self, gold, uid):
        """添加红豆"""
        try:
            db = AccountManager()
            db.connect()

            # 使用参数化查询更新金币数量
            sql = "UPDATE account_balance SET gold = %s WHERE uid = %s"
            db.execute(sql, (gold, uid))

            # 删除缓存
            self.redis_client.delete(f"balance_account_gold_{uid}")
            self.redis_client1.delete(f"balance_item_{uid}")

            # 验证更新结果
            result = db.fetch_one("SELECT gold FROM account_balance WHERE uid = %s", (uid,))
            if result and result[0] == gold:
                return jsonify({"code": "200", "message": "红豆已更新成功", "time": self.current_time}), 200
            else:
                return jsonify({"code": "1026", "message": "数据库或缓存更新失败", "time": self.current_time}), 400

        except Exception as e:
            return jsonify({"error": "发生错误: {}".format(str(e))}), 500

        finally:
            db.close()


    def add_noble_gold(self, gold, uid):
        """添加贵族红豆"""
        try:
            db = AccountManager()
            db.connect()

            # 检查用户是否已购买贵族
            if not db.fetch_one("SELECT uid FROM user_noble_info WHERE uid = %s", (uid,)):
                return jsonify({"message": "未查询到贵族信息，请先购买贵族", "time": self.current_time})

            # 更新用户贵族红豆
            db.execute("UPDATE biz_account_balance SET gold = %s WHERE biz_type = 1 AND uid = %s", (gold, uid))

            # 创建 Redis 连接并更新缓存
            self.redis_client.zadd("balance_noble_gold", {uid: gold})
            self.redis_client1.delete(f"balance_biz_account_{uid}")

            # 验证 Redis 中的值
            if self.redis_client.zscore("balance_noble_gold", uid) == gold and self.redis_client1.get(
                    f"balance_biz_account_{uid}") is None:
                return jsonify({"code": "200", "message": "贵族红豆已更新成功", "time": self.current_time}), 200

            return jsonify({"code": "1026", "message": "数据库或缓存更新失败", "time": self.current_time}), 400

        except Exception as e:
            return jsonify({"error": "发生错误: {}".format(str(e))}), 500

        finally:
            db.close()


    def add_resource_gold(self, gold, uid):
        """添加资源红豆"""
        try:
            # 创建 Redis 连接并更新缓存
            self.redis_client.set(f"balance_adv_account_gold_{uid}", gold)

            # 获取并验证 Redis 中的值
            retrieved_gold = self.redis_client.get(f"balance_adv_account_gold_{uid}")
            if retrieved_gold is not None and int(retrieved_gold) == gold:
                return jsonify({"code": "200", "message": "资源红豆添加成功", "time": self.current_time}), 200
            else:
                return jsonify({"code": "1026", "message": "资源红豆添加失败", "time": self.current_time}), 400

        except Exception as e:
            return jsonify({"code": "500", "message": f"发生错误: {str(e)}", "time": self.current_time}), 500


    def update_anchor(self, uid):
        """认证主播"""
        try:
            db = AccountManager()
            db.connect()

            # 更新认证主播字段
            db.execute("UPDATE user_info SET is_anchor = 1 WHERE id = %s", (uid,))

            # 更新缓存
            self.redis_6330.delete(f"user_item__{uid}")

            # 验证数据库中的认证状态
            result = db.fetch_one("SELECT is_anchor FROM user_info WHERE id = %s", (uid,))

            # 验证状态
            if result and result[0] == 1 and self.redis_6330.get(f"user_item__{uid}") is None:
                return jsonify({"code": "200", "message": "主播认证成功", "time": self.current_time}), 200
            else:
                return jsonify({"code": "1026", "message": "主播认证失败", "time": self.current_time}), 400

        except Exception as e:
            return jsonify({"code": "500", "message": f"发生错误: {str(e)}"}), 500

        finally:
            db.close()  # 确保数据库连接在处理完成后关闭


    def add_exp(self, exp, uid):
        """加经验(修改用户等级)"""
        try:
            db = AccountManager()
            db.connect()

            # 使用参数化查询更新经验值
            new_exp = exp
            sql = "UPDATE user_info SET exp = %s,new_exp = %s WHERE id = %s"
            db.execute(sql, (exp, new_exp, uid))

            # 删除缓存
            self.redis_6330.delete(f"user_item__{uid}")

            # 验证更新结果
            result = db.fetch_one("SELECT exp,new_exp FROM user_info WHERE id = %s", (uid,))

            if result and result[0] and result[1] == exp:
                return {"code": "200", "message": "经验添加成功", "time": self.current_time}, 200
            else:
                return {"code": "1026", "message": "数据库或缓存更新失败", "time": self.current_time}, 400

        except Exception as e:
            return {"error": f"发生错误: {str(e)}"}, 500

        finally:
            db.close()


    def add_vip(self, uid):
        """开通会员"""
        try:
            db = AccountManager()
            db.connect()

            # 使用参数化修改会员参数信息
            sql = "UPDATE user_info SET member_type = 1,type = 1,member_expire_time = '2099-11-27 23:59:59' WHERE id = %s"
            db.execute(sql, (uid))

            # 删除缓存
            self.redis_6330.delete(f"user_item__{uid}")

            # 验证更新结果
            result = db.fetch_one("SELECT member_type FROM user_info WHERE id = %s", (uid,))

            if result and result[0] == 1:
                return {"code": "200", "message": "会员开通成功", "time": self.current_time}, 200
            else:
                return {"code": "1026", "message": "更新失败", "time": self.current_time}, 400

        except Exception as e:
            return {"error": f"发生错误: {str(e)}"}, 500

        finally:
            db.close()


    def del_vip(self, uid):
        """会员过期"""
        try:
            db = AccountManager()
            db.connect()

            # 使用参数化修改会员参数信息
            sql = "UPDATE user_info SET member_type = null,type = 0,member_expire_time = null WHERE id = %s"
            db.execute(sql, (uid))

            # 删除缓存
            self.redis_6330.delete(f"user_item__{uid}")

            # 验证更新结果
            result = db.fetch_one("SELECT member_type FROM user_info WHERE id = %s", (uid,))

            if result and result[0] == None:
                return {"code": "200", "message": "修改会员过期成功", "time": self.current_time}, 200
            else:
                return {"code": "1026", "message": "更新失败", "time": self.current_time}, 400

        except Exception as e:
            return {"error": f"发生错误: {str(e)}"}, 500

        finally:
            db.close()


    def add_room_hot_list(self, roomId, score):
        """直播间添加到热门流"""
        member = roomId
        try:
            # 更新热门流缓存
            self.redis_6325.zadd("room_hot_list_0", {member: score})

            if self.redis_6325.zscore("room_hot_list_0", member) == score:
                return {"code": "200", "message": "添加热门流成功", "time": self.current_time}, 200
            else:
                return {"code": "1026", "message": "添加失败", "time": self.current_time}, 400

        except Exception as e:
            return {"error": f"发生错误: {str(e)}"}, 500


    def del_room_hot_list(self, roomId):
        """直播间从热门流移除"""
        member = roomId
        try:
            # 移除热门流缓存
            self.redis_6325.zrem("room_hot_list_0", member)

            if not self.redis_6325.zscore("room_hot_list_0", member):
                return {"code": "200", "message": "移除热门流成功", "time": self.current_time}, 200
            else:
                return {"code": "1026", "message": "更新失败", "time": self.current_time}, 400

        except Exception as e:
            return {"error": f"发生错误: {str(e)}"}, 500


    def add_intimacy(self, userId, score, uid):
        """加亲密度"""
        try:
            # 更新亲密度缓存
            a = self.H5_redis.zadd(f"anchor_intimacy_{userId}", {uid: score})
            print(a)

            if self.H5_redis.zscore(f"anchor_intimacy_{userId}", uid) == score:
                return {"code": "200", "message": "亲密度更新成功", "time": self.current_time}, 200
            else:
                return {"code": "1026", "message": "亲密度更新失败", "time": self.current_time}, 400

        except Exception as e:
            return {"error": f"发生错误: {str(e)}"}, 500


    def audit_drama(self, contentId, status):
        """审核剧或者集"""
        try:
            db = AccountManager()
            db.connect()

            # 查询content_id对应的主键id后，并将查询出来的元组数据转化为list
            dbdata = db.fetch_all('select id from drama_audit_info where status=2 and content_id=%s', (contentId,))
            ids = [item[0] for item in dbdata]

            # 将status转换为整数，避免字符串与整数比较的问题
            status = int(status)

            # 如果状态是审核通过
            if status == 3:
                for key in ids:
                    data = {
                        "auditId": key,
                        "status": status,
                        "rejectReason": "审核通过"
                    }
                    data = json.dumps(data)
                    re = requests.post(url='http://60.205.59.6:8090/oms/v1/creator/center/callback', data=data,
                                       headers={"Content-Type": "application/json"})
                    ra = re.json()
                    # 检查接口返回的状态
                    if ra['h']['code'] != 200:
                        return jsonify(ra), 400  # 返回失败的响应和状态码

                # 所有id都处理完毕且没有问题，返回审核通过的结果
                return jsonify(
                    {"code": "200", "message": "审核通过", "contentid": contentId, "time": self.current_time}), 200

            # 如果状态是审核拒绝
            if status == 4:
                for key in ids:
                    data = {
                        "auditId": key,
                        "status": status,
                        "rejectReason": "审核拒绝"
                    }
                    data = json.dumps(data)
                    re = requests.post(url='http://60.205.59.6:8090/oms/v1/creator/center/callback', data=data,
                                       headers={"Content-Type": "application/json"})
                    ra = re.json()
                    # 检查接口返回的状态
                    if ra['h']['code'] != 200:
                        return jsonify(ra), 400  # 返回失败的响应和状态码

                # 所有id都处理完毕且没有问题，返回审核拒绝的结果
                return jsonify(
                    {"code": "200", "message": "审核拒绝", "contentid": contentId, "time": self.current_time}), 200

        except Exception as e:
            # 捕获异常并返回错误信息
            return jsonify({"error": f"发生错误: {str(e)}", "time": self.current_time}), 500

        finally:
            # 确保数据库连接关闭
            db.close()
