import flask
from flask import request  # 获取参数
import json  # post请求传入json对象时，通过json获取参数
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
    except Exception as e:
        conn.rollback()  # 发生错误时回滚
        print(e)
    cursor.close()

server = flask.Flask(__name__)  # 创建一个flask对象


# 登录接口
@server.route('/login', methods=['get', 'post'])
def login():
    # 判断请求类型
    if (request.method == 'POST'):
        # 入参为json类型时，必须用.json方式获取
        username = request.json.get('username')
        password = request.json.get('password')
    else:
        username = request.values.get('username')  # 获取参数
        password = request.values.get('password')
        # print(username,password)
        # 如果存在用户名和密码
        if username and password:
            sql = 'select * from tbluser where colUsername="%s"' % username
            data = conn_mysql(sql)
            #print(type(data['colPassword']),'\n',username,' ',type(password))
            if data['colPassword'] == int(password):
                return '{"msg":"登录成功"}'
            else:
                return '{"msg":"账号密码错误"}'
        else:
            # sql = '''insert into tbluser values("%s","%s")'''
            # par =(username,password)
            # data = insert_mysql(sql,par)
            return '{"msg":"插入成功"}'

# @server.route('/login_', methods=['get', 'post'])
# def login():
#     # 判断请求类型
#     if (request.method == 'POST'):
#         # 入参为json类型时，必须用.json方式获取
#         username = request.json.get('username')
#         password = request.json.get('password')

# debug设置为True，修改接口信息后直接刷新接口即可；添加参数host='0.0.0.0'允许同一局域网内访问
server.run(port=8000, debug=True)