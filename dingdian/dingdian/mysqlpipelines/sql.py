from dingdian import settings
import pymysql

MYSQL_HOST = settings.MYSQL_HOST
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_POST = settings.MYSQL_POST
MYSQL_DB = settings.MYSQL_DB
db = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB)
cursor = db.cursor()
class Sql(object):

    @classmethod
    def insert_dd_name(cls,xs_name, xs_author, category, name_id):
        print(type(xs_name),'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        sql = "INSERT INTO dd_name(xs_name, xs_author, category, name_id) VALUES ('{0}', '{1}', '{2}', '{3}');".format(xs_name, xs_author, category, name_id)#存入字符串类型 format必须用''
        print(sql)
        cursor.execute(sql)
        db.commit()
    @classmethod
    def select_name(cls, name_id):
        sql = "SELECT EXISTS(SELECT 1 FROM dd_name WHERE name_id = {})".format(name_id)
        #print(sql)
        cursor.execute(sql)
        # if_exists = cursor.fetchall()[0][0]
        # a = cursor.fetchall()[0][0]
        # print(if_exists)  #fetchall只能使用一次
        return cursor.fetchall()[0]

