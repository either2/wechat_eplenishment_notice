from  flask import Flask,request,jsonify
import pymysql,time
class judeg_url:
    def __init__(self):
        pass
    def connect_mysql(self):
        db = pymysql.connect(
            host='47.93.149.238',
            port=3306,
            user='root',
            password='123456',
            database='sephora',
            use_unicode=True,
            charset="utf8")
        cursor = db.cursor()
        return cursor, db
    @staticmethod
    def close_connect(cursor,db):
        cursor.close()
        db.close()

    def read_more_data(self,sql):
        cursor, db = self.connect_mysql()
        cursor.execute(sql)
        # api_url_list = []
        api_url_list=''
        is_Replenishment_list=''
        up_datetime_list=''
        results = cursor.fetchall()
        for i in results:
            api_url_list += i[0]+'+'
            is_Replenishment_list += i[1]+'+'
            up_datetime_list += i[2]+'+'
        self.close_connect(cursor, db)
        return api_url_list,is_Replenishment_list,up_datetime_list

    def up_data(self,sql):
        cursor,db = self.connect_mysql()
        cursor.execute(sql)
        db.commit()
        self.close_connect(cursor, db)
    def verification(self,sql):
        try:
            api_url_list, is_Replenishment_list, up_datetime_list = self.read_more_data("%s"%sql)
            message=api_url_list+','+is_Replenishment_list+','+up_datetime_list
            return message
        except:pass


app = Flask(__name__)
@app.route("/execution_sql", methods=["POST"])
def execution_sql():
    try:
        sql = request.form.get("sql")
        if 'UPDATE' in sql:
            judeg_url().up_data(sql)
        elif 'SELECT' in sql:
            return judeg_url().verification(sql)
    except:
        return "发生错误，请稍后再试"

app.run(host="0.0.0.0", port=2333)
