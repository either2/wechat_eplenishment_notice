# -*- coding:utf-8 -*-
import werobot, time, pymysql, re
import requests,json
class add_stockurl:
    def __init__(self):
        pass

    @staticmethod
    def connect_mysql():
        db = pymysql.connect(
            host='47.93.149.238',
            port=3306,
            user='root',
            password='123456',
            database='sephora')
        cursor = db.cursor()
        return cursor, db

    @staticmethod
    def close_connect(cursor, db):
        cursor.close()
        db.close()

    def read_data(self, sql):
        cursor, db = self.connect_mysql()
        cursor.execute(sql)
        result_list = []
        results = cursor.fetchall()
        for i in results:
            result_list.append(i[0])
        self.close_connect(cursor, db)
        return result_list

    def up_data(self, sql):
        cursor, db = self.connect_mysql()
        cursor.execute(sql)
        db.commit()
        self.close_connect(cursor, db)

    def data_unite(self,openid, stock_url):
        openid_list = self.read_data("SELECT openid FROM attention_list")
        if openid not in openid_list:
            self.up_data("INSERT INTO  attention_list (openid,stock_url,count_attention) VALUES('%s','%s','1')" % (
                openid, stock_url))
            return "关注成功，商品补货后会第一时间通知您的哦"
        elif openid in openid_list:
            count_attention = self.read_data("SELECT count_attention FROM attention_list WHERE openid='%s'" % openid)
            try:
                if int(count_attention[0]) >= 10:
                    return "最多关注10个哦"
            except(IndexError):
                return "关注失败 - -！"
            stcok_urk_list = self.read_data("SELECT stock_url FROM attention_list WHERE openid='%s'" % openid)
            if stock_url in stcok_urk_list[0]:
                return "您已关注这个商品"
            else:
                self.up_data(
                    "UPDATE attention_list SET stock_url=CONCAT(stock_url,';%s')WHERE openid='%s'" % (stock_url,openid))
                new_count_attention = str(int(count_attention[0]) + 1)
                self.up_data(
                    "UPDATE  attention_list SET count_attention='%s' WHERE openid='%s'" % (new_count_attention, openid))
                return "关注成功，商品补货后会第一时间通知您的哦"

    def add_stockurl(self, openid, stock_url, api_url, stock_message, database):
        website_name = re.findall("[a-z]+\.com", stock_url)[0].split(".com")[0]
        api_url_list = self.read_data("SELECT api_url FROM %s WHERE website='%s'" % (database, website_name))
        if api_url in api_url_list:  # 可能出错，之前加了[0]
            sql_stock_url = self.read_data("SELECT stock_url FROM %s WHERE api_url='%s'" % (database, api_url))[0]
            openid_list = self.read_data("SELECT openid FROM %s WHERE api_url='%s'" % (database, api_url))
            if openid in openid_list[0]:
                return self.data_unite(openid, sql_stock_url)
            else:
                self.up_data(
                    "UPDATE %s SET openid=CONCAT(openid,';%s')WHERE api_url='%s'" % (database, openid, api_url))
                return self.data_unite(openid, sql_stock_url)
        else:
            stock_message = stock_message.replace("'", "")
            self.up_data(
                "INSERT INTO  %s (stock_url,openid,api_url,stock_message,website) VALUES('%s','%s','%s','%s','%s')" % (
                database,
                stock_url, openid, api_url, stock_message, website_name))
            return self.data_unite(openid, stock_url)


class delete_stockurl:
    def __init__(self):
        pass

    @staticmethod
    def connect_mysql():
        db = pymysql.connect(
            host='47.93.149.238',
            port=3306,
            user='root',
            password='123456',
            database='sephora')
        cursor = db.cursor()
        return cursor, db
    @staticmethod
    def close_connect(cursor, db):
        cursor.close()
        db.close()

    def read_data(self, sql):
        cursor, db = self.connect_mysql()
        cursor.execute(sql)
        result_list = []
        results = cursor.fetchall()
        for i in results:
            result_list.append(i[0])
        self.close_connect(cursor, db)
        return result_list

    def up_data(self, sql):
        cursor, db = self.connect_mysql()
        cursor.execute(sql)
        db.commit()
        self.close_connect(cursor, db)

    def delete_stockurl(self, stock_num, openid,database):
        cursor, db = self.connect_mysql()
        try:
            cursor.execute("SELECT stock_url ,openid,stock_message FROM %s WHERE stock_num='%s'" % (database,stock_num))
            results_wechatuser = cursor.fetchone()
            if results_wechatuser == None:
                return "没找到这件商品哦"
        except(IndexError):
            return "没找到这件商品哦"
        stock_url = results_wechatuser[0]
        openid_list = results_wechatuser[1]
        stock_message = results_wechatuser[2]
        if openid in openid_list:
            if len(re.findall(';', openid_list)) == 0:
                cursor.execute("delete from %s where stock_num='%s'" % (database,stock_num))
                db.commit()
            else:
                delete_openid = re.findall(r'%s;|;%s|%s' % (openid, openid, openid), openid_list)
                new_openid_list = openid_list.replace(delete_openid[0], '')
                # print(new_openid_list)
                self.up_data("UPDATE  %s SET openid='%s' WHERE stock_num='%s'" % (database,new_openid_list, stock_num))
        else:
            return "您没关注该商品" + "\n" + results_wechatuser[2]
        try:
            cursor.execute("SELECT stock_url,count_attention FROM attention_list WHERE openid='%s'" % openid)
            results_attention_list = cursor.fetchone()
            stock_url_list = results_attention_list[0]
        except Exception as e:
            return "未知错误：%s" % e
        count_attention = results_attention_list[1]
        new_count_attention = int(count_attention) - 1
        if stock_url in stock_url_list:
            if new_count_attention == 0:
                cursor.execute("delete from attention_list where openid='%s'" % openid)
                db.commit()
                return '商品信息:' + '\n' + stock_message + '\n' + '成功取消关注'
            elif new_count_attention != 0:
                if "?" in stock_url:
                    replace_stock_url = stock_url.replace("?", "\?")
                else:
                    replace_stock_url = stock_url
                delete_url = re.findall(r'%s;|;%s|%s' % (replace_stock_url, replace_stock_url, replace_stock_url),
                                        stock_url_list)
                new_url_list = stock_url_list.replace(delete_url[0], '')
                self.up_data("UPDATE  attention_list SET stock_url='%s',count_attention='%s' WHERE openid='%s'" % (
                new_url_list, new_count_attention, openid))
                return '商品:' + '\n' + stock_message + '\n' + '成功取消关注'

# class is_stockurl_inmysql:
#     def __init__(self):
#         pass
#     @staticmethod
#     def connect_mysql():
#         db = pymysql.connect(
#             host='47.93.149.238',
#             port=3306,
#             user='root',
#             password='123456',
#             database='sephora')
#         cursor = db.cursor()
#         return cursor, db
#
#     @staticmethod
#     def close_connect(cursor, db):
#         cursor.close()
#         db.close()
#
#     def read_data(self, sql):
#         cursor, db = self.connect_mysql()
#         cursor.execute(sql)
#         result_list = []
#         results = cursor.fetchall()
#         for i in results:
#             result_list.append(i[0])
#         self.close_connect(cursor, db)
#         return result_list

    # def is_stockurl_inmysql(self, stock_url,database): #如果商品数量较多时，挨个对比也许反而更慢
    #     #卡泡可以直接对比url，丝芙兰对比pid和stuid，梅西对比id与url后的色号与大小号，考虑将网站名加入wechhatuser表，查询更方便
    #     if "colourpop.com" in stock_url:
    #         stock_url_list = self.read_data("SELECT stock_url FROM %s WHERE website='colourpop'"%database)
    #         if stock_url in stock_url_list:
    #             stock_message = self.read_data("SELECT stock_message FROM %s WHERE stock_url='%s'" % (database,stock_url))[0]
    #             apiurl = self.read_data("SELECT api_url FROM %s WHERE stock_url='%s'" % (database,stock_url))[0]
    #             return stock_message, apiurl
    #         else:
    #             return None, None
    #     elif "sephora.com" in  stock_url:
    #         stock_url_list = self.read_data("SELECT stock_url FROM %s WHERE website='sephora'"%database)
    #         pid=re.findall("P[0-9]+",stock_url)[0]
    #         if "skuId=" in stock_url:
    #             skuid=re.findall("skuId=[0-9]+",stock_url)[0]
    #             for x in stock_url_list:
    #                 if pid in x and skuid in x:
    #                     stock_message = self.read_data("SELECT stock_message FROM %s WHERE stock_url='%s'" % (database, x))[0]
    #                     apiurl = self.read_data("SELECT api_url FROM %s WHERE stock_url='%s'" % (database, x))[0]
    #                     return stock_message, apiurl
    #         else:
    #             for y in stock_url_list:
    #                 if "skuId=" not in y and pid in y:
    #                     stock_message = self.read_data("SELECT stock_message FROM %s WHERE stock_url='%s'" % (database, y))[0]
    #                     apiurl = self.read_data("SELECT api_url FROM %s WHERE stock_url='%s'" % (database, y))[0]
    #                     return stock_message, apiurl
    #         return None, None
    #     elif "macys.com" in stock_url:
    #         stock_url_list = self.read_data("SELECT stock_url FROM %s WHERE website='macys'"%database)
    #         stockid=re.findall("ID=[0-9]+",stock_url)[0]
    #         if "[" in stock_url and "]" in stock_url:
    #             for x in stock_url_list:
    #                 if "[" in x and "]" in x and stockid in x :
    #                     colour_size=re.findall("\[.*?\]",stock_url)[0]
    #                     if colour_size in x:
    #                         stock_message = self.read_data("SELECT stock_message FROM %s WHERE stock_url='%s'" % (database, x))[0]
    #                         apiurl = self.read_data("SELECT api_url FROM %s WHERE stock_url='%s'" % (database, x))[0]
    #                         return stock_message, apiurl
    #         else:
    #             for y in stock_url_list:
    #                 if "[" not in y and stockid in y :
    #                     stock_message = self.read_data("SELECT stock_message FROM %s WHERE stock_url='%s'" % (database, y))[0]
    #                     apiurl = self.read_data("SELECT api_url FROM %s WHERE stock_url='%s'" % (database, y))[0]
    #                     return stock_message, apiurl
    #         return None, None
    #
    #     elif "belk.com" in stock_url:
    #



class my_attention:  #需要加另一张表的数据
    def __init__(self):
        self.db = pymysql.connect(
            host='47.93.149.238',
            port=3306,
            user='root',
            password='123456',
            database='sephora')
    def check_attention(self, openid):
        try:
            cursor= self.db.cursor()
            cursor.execute("SELECT stock_url FROM attention_list WHERE openid='%s'" % openid)
            try:
                results = cursor.fetchone()[0]
            except(TypeError):
                self.db.close()
                cursor.close()
                return "您还未关注任何商品哦！"
            stock_num = 1
            stock_message_summary = ''
            for i in results.split(";"):
                if "www.macys.com" in i :
                    try:
                        cursor.execute("SELECT stock_message,is_Replenishment,stock_num FROM %s WHERE stock_url='%s'" % ('domestic_wechatuser',i))
                        stock_sql = cursor.fetchone()
                        stock_message = stock_sql[0]
                        is_replenishment = stock_sql[1]
                        cursor.execute("SELECT stock_num FROM %s WHERE stock_url='%s'" % ('domestic_wechatuser',i))
                        unsubscribe_num = cursor.fetchone()[0]
                        if stock_num==1:
                            stock_message_summary += str(
                                stock_num) + ':' + stock_message + '[  库存：%s]' % is_replenishment + '   （回复"取消关注%sC"取消对该商品的关注）' % unsubscribe_num + '\n'
                            stock_num += 1
                        elif stock_num>1:
                            stock_message_summary += str(
                                stock_num) + ':' + stock_message + '[  库存：%s]' % is_replenishment + '   （回复"取消关注%sC"）' % unsubscribe_num + '\n'
                            stock_num += 1
                    except(TypeError):
                        stock_message_summary += str(stock_num) + ':' + "商品信息暂无" + '\n'
                        stock_num += 1
                else:
                    try:
                        cursor.execute(
                            "SELECT stock_message,is_Replenishment,stock_num FROM wechatuser WHERE stock_url='%s'" % i)
                        stock_sql = cursor.fetchone()
                        stock_message = stock_sql[0]
                        is_replenishment = stock_sql[1]
                        cursor.execute("SELECT stock_num FROM wechatuser WHERE stock_url='%s'" % i)
                        unsubscribe_num = cursor.fetchone()[0]
                        if stock_num==1:
                            stock_message_summary += str(
                                stock_num) + ':' + stock_message + '[  库存：%s]' % is_replenishment + '   （回复"取消关注%sF"取消对该商品的关注）' % unsubscribe_num + '\n'
                            stock_num += 1
                        elif stock_num>1:
                            stock_message_summary += str(
                                stock_num) + ':' + stock_message + '[  库存：%s]' % is_replenishment + '   （回复"取消关注%sF"）' % unsubscribe_num + '\n'
                            stock_num += 1
                    except(TypeError):
                        stock_message_summary += str(stock_num) + ':' + "商品信息暂无" + '\n'
                        stock_num += 1
            return stock_message_summary
        except:
            return "出错啦，请稍后查询"


class wechat_development:
    robot = werobot.WeRoBot(token='zyp123456789', app_id='wx075e6145dec8e5e9',
                            app_secret='35d5b46369f00465c9eb82847be53d1e')
    try:
        @robot.text
        def text_message(message):
            openid = message.source
            if re.findall("丝芙兰" + '.*?' + 'sephora.com' + '.*?' + 'P' + "[0-9]+", message.content):
                stock_url = re.findall("https://"+ '.*?'+"sephora.com" + '.*', message.content)[0]
                # sql_stock_message, sql_apiurl = is_stockurl_inmysql().is_stockurl_inmysql(stock_url,'wechatuser')
                data = {
                    "url": "%s" % stock_url}
                url = "http://54.255.165.203:2333/stockmessage"
                api_message = requests.post(url=url, data=data)
                if not re.findall("https://", api_message.text):
                    return "未找到商品，请核对商品链接"
                stock_message = api_message.text.split("https://")[0]
                api_url = "https://" + api_message.text.split("https://")[1]
                if "skuId=" in stock_url:
                    result = add_stockurl().add_stockurl(openid, stock_url, api_url, stock_message,'wechatuser')
                    return "商品信息：\n" + stock_message + '\n' + result
                else:
                    sku_number = "?skuId=" + api_url.split("Sku=")[1]
                    new_stock_url = stock_url + sku_number
                    result = add_stockurl().add_stockurl(openid, new_stock_url, api_url, stock_message,'wechatuser')
                    return "商品信息：\n" + stock_message + '\n' + result
                # else:
                #     result = add_stockurl().add_stockurl(openid, stock_url, sql_apiurl, sql_stock_message,'wechatuser')
                #     return "商品信息：\n" + sql_stock_message + '\n' + result

            if re.findall("卡泡" + '.*?' + 'colourpop.com/products' + '.*?', message.content):
                stock_url = re.findall("https://colourpop.com" + '.*', message.content)[0]
                # sql_stock_message, sql_apiurl = is_stockurl_inmysql().is_stockurl_inmysql(stock_url,'wechatuser')
                # if sql_stock_message == None:
                data = {
                    "url": "%s" % stock_url}
                url = "http://54.255.165.203:2333/stockmessage"
                api_message = requests.post(url=url, data=data)
                if not re.findall("https://", api_message.text):
                    return api_message.text
                stock_message = api_message.text.split("https://")[0]
                api_url = "https://" + api_message.text.split("https://")[1]
                result = add_stockurl().add_stockurl(openid, stock_url, api_url, stock_message,'wechatuser')
                return "商品信息：\n" + stock_message + '\n' + result
                # else:
                #     result = add_stockurl().add_stockurl(openid, stock_url, sql_apiurl, sql_stock_message,'wechatuser')
                #     return "商品信息：\n" + sql_stock_message + '\n' + result

            if re.findall("梅西"+ '.*?'+"macys.com" + '.*?' + 'ID=' + '.*?', message.content):
                stock_url = re.findall("https://"+ '.*?'+"macys.com" + '.*', message.content)[0]
                # sql_stock_message, sql_apiurl = is_stockurl_inmysql().is_stockurl_inmysql(stock_url,'domestic_wechatuser')
                # if sql_stock_message == None:
                data = {
                    "url": "%s" % stock_url}
                url = "http://47.93.149.238:2334/stockmessage"
                api_message = requests.post(url=url, data=data).text
                if "示例"  in api_message or "https://" not in api_message:
                    return api_message
                else:
                    stock_message=api_message.split("https://")[0]
                    api_url="https://"+api_message.split("https://")[1]
                    result = add_stockurl().add_stockurl(openid, stock_url, api_url, stock_message,'domestic_wechatuser')
                    return "商品信息：\n" + stock_message + '\n' + result
                # else:
                #     result = add_stockurl().add_stockurl(openid, stock_url, sql_apiurl, sql_stock_message,'domestic_wechatuser')
                #     return "商品信息：\n" + sql_stock_message + '\n' + result



            if re.findall('.*?' + 'belk.com/p' + '.*?', message.content):
                stock_url = re.findall("https:" + '.*?' + "belk.com/p" + '.*', message.content)[0]
                # sql_stock_message, sql_apiurl = is_stockurl_inmysql().is_stockurl_inmysql(stock_url,'wechatuser')
                # if sql_stock_message == None:
                data = {
                    "url": "%s" % stock_url}
                url = "http://54.255.165.203:2333/stockmessage"
                api_message = requests.post(url=url, data=data).text
                print(api_message)
                if "示例" in api_message or "https://" not in api_message:
                    return api_message
                else:
                    stock_message = api_message.split("https://")[0]
                    api_url = "https://" + api_message.split("https://")[1]
                    result = add_stockurl().add_stockurl(openid, stock_url, api_url, stock_message,'wechatuser')
                    return "商品信息：\n" + stock_message + '\n' + result
                # else:
                #     result = add_stockurl().add_stockurl(openid, stock_url, sql_apiurl, sql_stock_message,'wechatuser')
                #     return "商品信息：\n" + sql_stock_message + '\n' + result


            if re.findall("取消关注" + '[0-9]+[a-zA-Z]', message.content) and len(message.content)<10:
                user_message = re.findall('[0-9]+[a-zA-Z]', message.content)[0]
                if "f" in user_message or "F" in user_message:
                    stock_num = re.findall('[0-9]+', user_message)[0]
                    return delete_stockurl().delete_stockurl(stock_num, openid,'wechatuser')
                elif "c" in user_message or "C" in user_message:
                    stock_num = re.findall('[0-9]+', user_message)[0]
                    return delete_stockurl().delete_stockurl(stock_num, openid, 'domestic_wechatuser')
                else:return "您忘记加编号的字母了- -！"
            else:
                return "目前支持：丝芙兰、卡泡、梅西、belk网站商品的补货通知，如果您想关注商品请发送正确的商品链接给我哦"

        @robot.click
        def click_event(message):
            if message.key == 'attention_sephora':
                return "请回复 丝芙兰+要关注的商品地址" + '\n' + "示例：丝芙兰https://www.sephora.com/product/powermatte-lip-pigment-P421485"
            if message.key == 'attention_colorpop':
                return "请回复 卡泡+要关注的商品地址" + '\n' + "示例：卡泡https://colourpop.com/products/mulan-eyeshadow-palette"
            if message.key == 'attention_macys':
                return "请回复 梅西+要关注的商品地址" + '\n' + "示例：梅西https://www.macys.com/shop/product/fitbit-charge-4-black-band-touchscreen-smart-watch-22.6mm?ID=11041254&CategoryID=76406"
            if message.key == 'attention_belk':
                return "请直接回复belk网站上商品地址" + '\n' + "示例：https://www.belk.com/p/coach-branding-30-field-tote/260036889488.html"
            if message.key == 'attention_list':
                openid = message.source
                return my_attention().check_attention(openid)
            if message.key == 'help':
                return "1.提供境外商品补货通知服务，直接按照指示回复商品链接就可以了哦，商品补货后这边会第一时间通知您的！" + '\n' + '2.若商品有多个色号或大小，商品链接请精确到具体的色号或大小哦' + '\n' + 'ps(若需更多帮助可加微信：either2  记得备注“微信公众号”哦)'

        @robot.subscribe
        def subscribe(message):
            return "终于等到你！"

        robot.config['HOST'] = '0.0.0.0'
        robot.config['PORT'] = 80
        robot.run()
    except Exception as e:
        with open("./wechat_development.txt", 'a', encoding='utf8') as f:
            f.write(str(e))

if __name__ == '__main__':
    wechat_development = wechat_development()
    # wechat_development.replay_message()