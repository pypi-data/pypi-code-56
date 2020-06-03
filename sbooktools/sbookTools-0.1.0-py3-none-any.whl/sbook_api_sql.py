
import pymysql

def api_mysql(sql, mysql_condition):
    db = pymysql.connect(**mysql_condition)  # 连接数据库
    cursor = db.cursor()  # 创建游标。
    cursor.execute(sql)
    db.commit()
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result