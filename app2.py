import MySQLdb

conn = MySQLdb.connect(user='root', password='123456', database='myblog', charset='utf8')

# 数据库查询
def conn_mysql(sql):

    # 创建游标  指定查询字段名
    cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)  # 这里
    cur.execute(sql)
    res = cur.fetchone()
    # print(res)
    conn.commit()
    cur.close()
    conn.close()
    return res


def insert_mysql(sql,par):
    cursor = conn.cursor()
    try:
        cursor.execute(sql,par)
        conn.commit()  # 提交到数据库执行，一定要记提交哦
        print('提交成功')
    except Exception as e:
        conn.rollback()  # 发生错误时回滚
        print(e)
    cursor.close()

sql = '''insert into tbluser values("%s","%s","%s")'''
par =('002','admin1',123456789)
data = insert_mysql(sql,par)