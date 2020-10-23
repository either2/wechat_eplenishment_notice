# -*- coding:utf-8 -*-
import pymysql
from  flask import Flask,request
import requests,time,json,datetime,random
class shop_stock:
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
    def read_data(self,sql):  #查询数据库
        self.write_data('\n' + '进入读取数据'+ '   ' + self.get_time())
        cursor,db=self.connect_mysql()
        cursor.execute(sql)
        api_list=[]
        results = cursor.fetchall()
        for i in results:
            api_list.append(i[0])
        # self.close_connect(cursor,db)
        self.write_data('\n' + '读取数据完毕' + '   ' + self.get_time())
        return api_list

    def read_more_data(self,sql):
        self.write_data('\n' + '进入更多读取数据' + '   ' + self.get_time())
        cursor, db = self.connect_mysql()
        cursor.execute(sql)
        api_url_list = []
        is_Replenishment_list=[]
        up_datetime_list=[]
        results = cursor.fetchall()
        for i in results:
            api_url_list.append(i[0])
            is_Replenishment_list.append(i[1])
            up_datetime_list.append(i[2])
        self.write_data('\n' + '读取更多数据完毕' + '   ' + self.get_time())
        return api_url_list,is_Replenishment_list,up_datetime_list

    @staticmethod
    def write_data(message):
        with open('./spider_result.txt','a',encoding='utf-8') as c:
            c.write(message)

    def up_data(self,sql):  #更新数据库
        self.write_data('\n' + '进入写入数据' + '   ' + self.get_time())
        cursor,db = self.connect_mysql()
        cursor.execute(sql)
        db.commit()
        self.close_connect(cursor, db)
        self.write_data('\n' + '写入数据完毕' + '   ' + self.get_time())
    # def count_attention(self,openid):
    #     cursor, db = self.connect_mysql()
    #     cursor.execute("SELECT stock_url FROM attention_list WHERE openid='%s'"%openid)
        # db.commit()
        # self.close_connect(cursor, db)

    @staticmethod
    def get_time():
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def api_spider(self,api_url):
        # try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
        get_requests = requests.get(api_url,headers=headers,timeout=8).text
        json_spider=json.loads(get_requests)
        try:
            key_message=str(json_spider['currentSku']['actionFlags']['isAddToBasket'])
            return key_message
        except(KeyError):
            erroy_message=str(json_spider['errorCode'])
            if erroy_message=='-4':
                return 'done'
        # except Exception as e:
        #     self.write_data('\n' + '爬虫出错%s：%s' % (e,api_url) + '  ' + self.get_time())
        # else:return None
        # except(KeyError):
        #     self.write_data('\n' + '未找到字典的key：%s' % api_url+self.get_time())
        #     return None
        # except(requests.exceptions.ProxyError):
        #     self.write_data('\n' + '代理错误：%s' % api_url+ '  '+self.get_time())
        #     return None
        # except(TimeoutError):
        #     self.write_data('\n' + '响应超时：%s' % api_url+ '  '+self.get_time())
        #     return None
        # except(IndexError):
        #     self.write_data('\n' + '找不到关键切割数据：%s' % api_url+ '  '+self.get_time())
        #     return None
        # except(requests.exceptions.ReadTimeout):
        #     self.write_data('\n' + '代理服务响应超时：%s' % api_url+ '  '+self.get_time())
        #     time.sleep(60)
        #     return None
        # except(requests.exceptions.ConnectTimeout):
        #     self.write_data('\n' + '代理服务响应超时：%s' % api_url + '  '+self.get_time())
        #     time.sleep(60)
        #     return None
        # except(json.decoder.JSONDecodeError) :
        #     self.write_data('\n' + '可能无商品，返回结果不是json数据：%s' % api_url+ '  '+self.get_time())
        #     return None
        # except(pymysql.err.OperationalError):
        #     self.write_data('\n' + '数据库连接超时：%s' % api_url + '  ' + self.get_time())
        #     time.sleep(30)
        #     return None

    def no_stock(self,key_message,api_url):
        if key_message=='done':
            self.up_data("UPDATE  wechatuser SET is_Replenishment='done'WHERE api_url='%s'" % api_url)
        if key_message=='False' or key_message=='false':
            pass
        elif key_message=='True' or key_message=='true':
            time_now = self.get_time()
            self.up_data("UPDATE  wechatuser SET is_Replenishment='rim' WHERE api_url='%s'" % api_url)
            # self.write_data('\n' + '商品已补货:%s' % api_url + '  '+time_now)
        else:pass

    def is_stock(self,key_message,api_url):
        if key_message == 'done':
            self.up_data("UPDATE  wechatuser SET is_Replenishment='done'WHERE api_url='%s'" % api_url)
        if key_message=='True' or key_message=='true':
            time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # self.write_data('\n' + '商品仍有货:%s' % api_url + '   '+time_now)
            self.up_data("UPDATE  wechatuser SET up_datetime='%s' WHERE api_url='%s'"%(time_now,api_url))
        elif key_message=='False' or key_message=='false':
            # self.write_data('\n' + '重新开始监控:%s' % api_url + '   '+self.get_time())
            self.up_data("UPDATE  wechatuser SET is_Replenishment='no' WHERE api_url='%s'"%api_url)

    def spider_sephora_stock(self):
        # for w in range(1,1000):
        #     with open("./notetime.txt",'a',encoding="utf8")as f:
        #         f.write('\n' +str(w)+'   '+self.get_time()+'开始')
        try:
            api_url_list, is_Replenishment_list, up_datetime_list=self.read_more_data("SELECT api_url,is_Replenishment,up_datetime FROM wechatuser")
            for i in range(len(is_Replenishment_list)):
                try:
                    if is_Replenishment_list[i]=="yes":
                        time1 = datetime.datetime.strptime(self.get_time(), "%Y-%m-%d %H:%M:%S")
                        time0 = datetime.datetime.strptime(up_datetime_list[i], "%Y-%m-%d %H:%M:%S")
                        if (time1 - time0).seconds >= 1000:
                            key_message = self.api_spider(api_url_list[i])
                            self.is_stock(key_message, api_url_list[i])
                            self.up_data("UPDATE  wechatuser SET up_datetime='%s' WHERE api_url='%s'" % (self.get_time(), api_url_list[i]))
                        else:pass
                    elif is_Replenishment_list[i]=="no":
                        key_message = self.api_spider(api_url_list[i])
                        self.no_stock(key_message, api_url_list[i])
                        self.up_data("UPDATE  wechatuser SET up_datetime='%s' WHERE api_url='%s'" % (self.get_time(), api_url_list[i]))
                    elif is_Replenishment_list[i]=="rim":
                        self.write_data('\n' +"这里有个时间差"+self.get_time())
                except Exception as e :
                    self.write_data('\n' + '错误信息1：%s' % (str(e)) + self.get_time())
                    time.sleep(30)
            time.sleep(random.randint(10, 30) / 2)
            # with open("./notetime.txt", 'a', encoding="utf8")as f:
            #     f.write('\n' + str(w) + '   ' + self.get_time() + '结束')
        except Exception as e :
            self.write_data('\n' + '错误信息：%s' % (str(e)) + self.get_time())
            time.sleep(30)

# app = Flask(__name__)
# @app.route("/spider_stock", methods=["get"])
# def spider_stock():
#     try:
#         shop_stock().spider_sephora_stock()
#         return 'yes'
#     except:
#         return "no"
#
# app.run(host="0.0.0.0", port=2334)
if __name__ == '__main__':
    shop_stock = shop_stock()
    while 1:
        shop_stock.spider_sephora_stock()