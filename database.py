"database.py"

from pymysql import connect, cursors

class Database:
    """
    通用mysql操作
    """
    MYSQL_HOST = '60.205.59.6'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'uxin.com'
    MYSQL_DATABASE = 'test_information'
    MYSQL_CHARSET = 'utf8mb4'
    MYSQL_CURSORCLASS = cursors.DictCursor


    @classmethod
    def mysql_login(cls):
        conn = connect(
            host=cls.MYSQL_HOST,
            port=cls.MYSQL_PORT,
            user=cls.MYSQL_USER,
            password=cls.MYSQL_PASSWORD,
            database=cls.MYSQL_DATABASE,
            charset=cls.MYSQL_CHARSET,
            cursorclass=cls.MYSQL_CURSORCLASS
        )
        return conn

    @classmethod
    def close_connection(cls, conn):
        if conn:
            conn.close()
