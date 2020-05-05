import pymysql
from scrapy.utils.project import get_project_settings#引入settings配置

class DBHelper:

    def __init__(self):
        self.settings=get_project_settings()#获取settings配置数据

        # self.host=self.settings['MYSQL_HOST']
        # self.port=self.settings['MYSQL_PORT']
        # self.user=self.settings['MYSQL_USER']
        # self.passwd=self.settings['MYSQL_PASSWD']
        # self.db=self.settings['MYSQL_DBNAME']

        self.conn = pymysql.connect(host=self.settings['MYSQL_HOST'],
                                    port=self.settings['MYSQL_PORT'],
                                    user=self.settings['MYSQL_USER'],
                                    password='spdb1234',
                                    db=self.settings['MYSQL_DBNAME'],
                                    charset='utf8')
    # def connectMysql(self):
    #     conn=pymysql.connect(host=self.host,
    #                          port=self.port,
    #                          user=self.user,
    #                          passwd=self.passwd,
    #                          charset='utf8')
    #     #     # connection database
    #     #     # get cursor
    #     #     # 建立数据库连接
    #     #     self.connection = pymysql.connect(host='127.0.0.1', port=3306, user='manage', password='spdb1234', db='slife',
    #     #                                       charset='utf8')
    #     #     #     #创建操作游标
    #     #     self.cursor = self.connection.cursor()
    #     return conn
    #连接数据库
    # def connectDatabase(self):
    #     conn=pymysql.connect(host=self.host,
    #                          port=self.port,
    #                          user=self.user,
    #                          passwd=self.passwd,
    #                          db=self.db,
    #                          charset='utf8')
    #     return conn

    #创建数据库
    def createDatabase(self):
        # conn=self.connectMysql()

        sql="create database if not exists "+self.db
        cur=self.conn.cursor()
        cur.execute(sql)
        cur.close()
        # conn.close()

    #创建数据表
    def createTable(self,sql):
        # conn=self.connectDatabase()

        cur=self.conn.cursor()
        cur.execute(sql)
        cur.close()
        # conn.close()

    #插入数据
    def insert(self,sql,*params):
        # conn=self.connectDatabase()

        cur=self.conn.cursor()
        cur.execute(sql,params)
        self.conn.commit()
        cur.close()
        # conn.close()

    #更新数据
    def update(self,sql,*params):
        # conn=self.connectDatabase()

        cur=self.conn.cursor()
        cur.execute(sql,params)
        self.conn.commit()
        cur.close()
        # conn.close()

    #删除数据
    def delete(self,sql,*params):
        # conn=self.connectDatabase()

        cur=self.conn.cursor()
        cur.execute(sql,params)
        self.conn.commit()
        cur.close()
        # conn.close()

    #查询一条数据
    def query(self, sql, *params):
        # conn = self.connectDatabase()
        cur = self.conn.cursor()
        cur.execute(sql, params)
        result = cur.fetchone()
        cur.close()
        # conn.close()
        return result

#测试数据库操作
class TestDBHelper:

    def __init__(self):
        self.dbHelper=DBHelper()

    def testCreateDatebase(self):
        self.dbHelper.createDatabase()

    def testCreateTable(self):
        sql="create table testtable(id int primary key auto_increment,name varchar(50),url varchar(200))"
        self.dbHelper.createTable(sql)

    def testInsert(self, item):
        sql="insert into example(hscode, 申报名称, 申报要素, 参考均价, 参考最高价, 参考最低价) values (%s, %s, %s, %s, %s, %s)"
        params=(item['hscode'], item['申报名称'], item['申报名称'], item['参考均价'], item['参考最高价'], item['参考最低价'])
        self.dbHelper.insert(sql,*params)
    def testUpdate(self):
        sql="update testtable set name=%s,url=%s where id=%s"
        params=("update","update","1")
        self.dbHelper.update(sql,*params)

    def testDelete(self):
        sql="delete from testtable where id=%s"
        params=("1")
        self.dbHelper.delete(sql,*params)
    def testquery(self):
        # sql = "select count(1) from ct_book"
        sql = "SELECT offset FROM ct_job WHERE job_type = 1"
        print(self.dbHelper.query(sql))

if __name__=="__main__":
    testDBHelper=TestDBHelper()
    testDBHelper.testquery()