# -*- coding: utf-8 -*-
# @Time : 2024/11/8 下午2:17
# @Author : 王雷
# @Email : eric@uxin.com
# @File : queries.py
# @Project : shuju

import pymysql
from flask import Flask,jsonify,request

class AccountManager:

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
            # print("数据库连接成功")
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
            # print("数据库连接已关闭")