# -*- coding:utf-8 -*-
import re
import requests,time,json,datetime,random,pymysql
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
    def read_data(self,sql):
        cursor,db=self.connect_mysql()
        db.ping(reconnect=True)
        cursor.execute(sql)
        api_list=[]
        results = cursor.fetchall()
        for i in results:
            api_list.append(i[0])
        self.close_connect(cursor,db)
        return api_list

    def read_more_data(self,sql):
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
        self.close_connect(cursor, db)
        return api_url_list,is_Replenishment_list,up_datetime_list

    @staticmethod
    def write_data(message):
        with open('./spider_result.txt','a',encoding='utf-8') as c:
            c.write(message)

    def up_data(self,sql):
        cursor,db = self.connect_mysql()
        cursor.execute(sql)
        db.commit()
        self.close_connect(cursor, db)

    @staticmethod
    def get_time():
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def one_api_spider(self,api_url):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
                   "Cookie": 'SEED=-3293640680221306390%7C%7C418-20%2C485-20%2C566-21; _abck=B03C6961D0F3CFC7A374AEBCF5666EA8~-1~YAAQL/B33zOO1SJ0AQAABK3mLQS6vyq5rww/9KG7dFCQYYCsqoC4V+L4UP6J0b6uW575YZoJj1P/mgYoVeJJQcYqv05J1+dRVBk/LMrpks469/rRXECBQ20oFP25CHQQoQNWGgEBHgdxu/u/g4kvJN6zTlJSVqXTynF/Y6K891G/ASnpvFMnlHgH50tWdjm2sY6Z4YYZSraxMCqrQ7QIU/w8xQSyYrYj7JhbCfuYtqBjkoV+KeiB4MFlalxYG48DqfpAGlgdTuvHU4zkQVtQyT1laFZvkPtStq99bomgH6baXt1jel+0zCAkAFG09LUlbWenJ7H/Ww==~-1~-1~-1; AMCV_8D0867C25245AE650A490D4C%40AdobeOrg=-1891778711%7CMCIDTS%7C18501%7CMCMID%7C18246968150624710560921075543064693367%7CMCAAMLH-1598857801%7C11%7CMCAAMB-1599101282%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1598503682s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-18506%7CvVersion%7C2.4.0; mbox=PC#f44d49032569405db80b0a0409598278.38_0#1661497802|session#107e1dd5218c49e4900d2f2b9ee430c9#1598499257; utag_main=v_id:01713feaf045002ba7a1f9520c900104e001600d00978$_sn:6$_ss:0$_st:1598499727004$vapi_domain:macys.com$ses_id:1598496481380%3Bexp-session$_pn:6%3Bexp-session; _ga=GA1.2.219375090.1585915301; smtrrmkr=637340941975487689%5E01713feb-0e20-44ce-9919-456a1ec34e5a%5E01742dd0-a4a0-4272-9aa8-80f48d70f877%5E0%5E104.168.173.132; cto_bundle=x6HDrF8lMkYwNTEwaDJxN2d3Sm85UHhiNE9jTSUyQk91M1EwNWlzeVZUWHhiNm0zeE1sNmhiZzdJWVBmU0Rmd0tXJTJGUEFmVHgzc3BXcExhWERFUGtCRDJnQnhIWEREdHpYSlcwQyUyQmtEWFhUUzRHbjRUYTJ5MXFQckJ1QVQlMkZvaGo4dTd5TVNKWUpxdDRPT1NUdlV6RXBsZ05PQTMyakNRJTNEJTNE; cd_user_id=1713feb2151161-020d582e5986418-4c302f7e-144000-1713feb215240f; CONSENTMGR=ts:1585915307160%7Cconsent:true; RTD=e7aae70e7a9d40e7a6170e7a4010e7a7f50e7ab530e7a4e90e7a7a00; atgRecVisitorId=12017BE3OzR_oRPOIH54UFhuc5uH19sGbzaJCE6-uboc780BD50; RT="z=1&dm=macys.com&si=1fd02135-153e-45b3-a46e-0478bb954deb&ss=kec7j3y5&sl=8&tt=eexb&bcn=%2F%2F684d0d37.akstat.io%2F&obo=5"; _gid=GA1.2.1335125292.1598410438; sto__vuid=1ef150e98c72787540d7bd29d3da1d6e; BVBRANDID=1d3742b1-cfa2-4243-870f-0966ed929953; CRTOABE=0; shippingCountry=US; currency=USD; SignedIn=0; GCs=CartItem1_92_03_87_UserName1_92_4_02_; akavpau_www_www1_macys=1598498220~id=07fef41c85e63f95f06339c39c9cedba; bm_sz=2890D9BD32798E9E5B39658910BE3165~YAAQNfh338PdiyN0AQAAHpLQLQj0jNCHwXc4VGVcp+Lb7DyyGI/tlTDrYJ6ZLvfAJTZLM7ILg1l3O7jOfEqAiZiC0Hf4WC6Vup1nwDooCZIYAw0OCZ3rBzt574aXJIqcmD7lzPgaUL2Sda7pcoMtwrhBQPuQMadJbt/XCT44Ozh5QzHjJfcGXswzYIF65GQ=; mercury=true; ak_bmsc=EFFC347CCE54BFB785405561C6508D12DF77F835104C0000DE1E475F6ECD6210~plbFv2hs4IYBi4uuRUl5QAK2QQhnzpmVDUyHRTU8JG2fjxYAoVKufyDQ7sYMbiaGJ/T+9kB7aby97wt3nv65JK/GwZFA+H1QrRu+YrWZEdin3oIVo+unw36HObPjqNiqQehRdo4I8cd21tuEWhhKIMg86/ZEvjXPSWPkhiqfLFidxRhHsrVxIpc+tk11YX3KVMptOtVlc625TE+udOqsokLXgYDvi732yfE9qrkzbbd1ML2jDWv+9FQv6wjeNuHnma; FORWARDPAGE_KEY=https%3A%2F%2Fwww.macys.com%2Fshop%2Fproduct%2Fdr.-scholls-womens-no-chill-slip-on-sneakers%3FID%3D10204376%26CategoryID%3D56233%26sizes%3DWOMEN_SHOE_SIZE_T!!8%3B%3B8.5%26swatchColor%3DTan%252FBlack%2520Leopard; check=true; TLTSID=47381014370864944584677601668781; xdVisitorId=12017BE3OzR_oRPOIH54UFhuc5uH19sGbzaJCE6-uboc780BD50; AMCVS_8D0867C25245AE650A490D4C%40AdobeOrg=1; s_pers=%20v30%3Dproduct%7C1598499197822%3B%20c29%3Dmcom%253Apdp%253Asingle%253A10204376%253Awomens%2520no%2520chill%2520slip-on%2520sneakers%7C1598499729382%3B; s_sess=%20s_cc%3Dtrue%3B; bm_sv=DFD313CE96AAFE6BD3609E769A813026~TvESzGPp6Xssx+K/BHrFLuEal3xB8W31FUK1Oyyak7gy45gSWkJVfEPU6B3o2fFiB2lwK9s3TauxkmEulxPECATDxRMQWP5n/gTFlVm4Soj5hJ1fGeT5meMZRxDOXIwu2zfEZTcMAbnu86169RLAT7iQDT2TxMh1pnqz/fKvEaQ=; atgRecSessionId=G00t0KLi5u9YKdNlVAXUY-KZqAH34ubd5dqH-UNhOEOEb_2glhvk!-1713841853!93897707; s_fid=2D4F829CE7E58B73-26DEFAE6ADF3FA44; TS0132ea28=011c44459135c9e75a7aefce729c4d461ac86ec75b92de5d3de54f8c551ef15016a6111009ad3590a1686e544da14394336e0f9728; sto__session=1598496775152; sto__count=2; _uetsid=50d3e90100f04cc2ab39815d7ce438d6; _uetvid=9410dcc1ee615fd467023a7418fea156; BVBRANDSID=3755a33f-38ff-40fe-8562-f39a26ae386a',
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                   "Accept-Encoding": "gzip, deflate, br",
                   "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                   "Cache-Control": "max-age=0",
                   "Connection": "keep-alive",
                   "Host": "www.macys.com",
                   "Upgrade-Insecure-Requests": "1"}
        get_requests = requests.get(api_url,headers=headers,timeout=8).text
        json_result=json.loads(get_requests, strict=False)
        key_message=str(json_result['product'][0]['availability']['available'])
        return key_message
    def num_api_spider(self,num_api_url):
        stock_message = re.findall("\[[0-9]+/.*", num_api_url)[0]
        stock_color = stock_message.split("/")[0].split("[")[1]
        stock_size = stock_message.split("/")[1].split("]")[0]
        api_url=num_api_url.split("[")[0]
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
                   "Cookie": 'SEED=-3293640680221306390%7C%7C418-20%2C485-20%2C566-21; _abck=B03C6961D0F3CFC7A374AEBCF5666EA8~-1~YAAQL/B33zOO1SJ0AQAABK3mLQS6vyq5rww/9KG7dFCQYYCsqoC4V+L4UP6J0b6uW575YZoJj1P/mgYoVeJJQcYqv05J1+dRVBk/LMrpks469/rRXECBQ20oFP25CHQQoQNWGgEBHgdxu/u/g4kvJN6zTlJSVqXTynF/Y6K891G/ASnpvFMnlHgH50tWdjm2sY6Z4YYZSraxMCqrQ7QIU/w8xQSyYrYj7JhbCfuYtqBjkoV+KeiB4MFlalxYG48DqfpAGlgdTuvHU4zkQVtQyT1laFZvkPtStq99bomgH6baXt1jel+0zCAkAFG09LUlbWenJ7H/Ww==~-1~-1~-1; AMCV_8D0867C25245AE650A490D4C%40AdobeOrg=-1891778711%7CMCIDTS%7C18501%7CMCMID%7C18246968150624710560921075543064693367%7CMCAAMLH-1598857801%7C11%7CMCAAMB-1599101282%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1598503682s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-18506%7CvVersion%7C2.4.0; mbox=PC#f44d49032569405db80b0a0409598278.38_0#1661497802|session#107e1dd5218c49e4900d2f2b9ee430c9#1598499257; utag_main=v_id:01713feaf045002ba7a1f9520c900104e001600d00978$_sn:6$_ss:0$_st:1598499727004$vapi_domain:macys.com$ses_id:1598496481380%3Bexp-session$_pn:6%3Bexp-session; _ga=GA1.2.219375090.1585915301; smtrrmkr=637340941975487689%5E01713feb-0e20-44ce-9919-456a1ec34e5a%5E01742dd0-a4a0-4272-9aa8-80f48d70f877%5E0%5E104.168.173.132; cto_bundle=x6HDrF8lMkYwNTEwaDJxN2d3Sm85UHhiNE9jTSUyQk91M1EwNWlzeVZUWHhiNm0zeE1sNmhiZzdJWVBmU0Rmd0tXJTJGUEFmVHgzc3BXcExhWERFUGtCRDJnQnhIWEREdHpYSlcwQyUyQmtEWFhUUzRHbjRUYTJ5MXFQckJ1QVQlMkZvaGo4dTd5TVNKWUpxdDRPT1NUdlV6RXBsZ05PQTMyakNRJTNEJTNE; cd_user_id=1713feb2151161-020d582e5986418-4c302f7e-144000-1713feb215240f; CONSENTMGR=ts:1585915307160%7Cconsent:true; RTD=e7aae70e7a9d40e7a6170e7a4010e7a7f50e7ab530e7a4e90e7a7a00; atgRecVisitorId=12017BE3OzR_oRPOIH54UFhuc5uH19sGbzaJCE6-uboc780BD50; RT="z=1&dm=macys.com&si=1fd02135-153e-45b3-a46e-0478bb954deb&ss=kec7j3y5&sl=8&tt=eexb&bcn=%2F%2F684d0d37.akstat.io%2F&obo=5"; _gid=GA1.2.1335125292.1598410438; sto__vuid=1ef150e98c72787540d7bd29d3da1d6e; BVBRANDID=1d3742b1-cfa2-4243-870f-0966ed929953; CRTOABE=0; shippingCountry=US; currency=USD; SignedIn=0; GCs=CartItem1_92_03_87_UserName1_92_4_02_; akavpau_www_www1_macys=1598498220~id=07fef41c85e63f95f06339c39c9cedba; bm_sz=2890D9BD32798E9E5B39658910BE3165~YAAQNfh338PdiyN0AQAAHpLQLQj0jNCHwXc4VGVcp+Lb7DyyGI/tlTDrYJ6ZLvfAJTZLM7ILg1l3O7jOfEqAiZiC0Hf4WC6Vup1nwDooCZIYAw0OCZ3rBzt574aXJIqcmD7lzPgaUL2Sda7pcoMtwrhBQPuQMadJbt/XCT44Ozh5QzHjJfcGXswzYIF65GQ=; mercury=true; ak_bmsc=EFFC347CCE54BFB785405561C6508D12DF77F835104C0000DE1E475F6ECD6210~plbFv2hs4IYBi4uuRUl5QAK2QQhnzpmVDUyHRTU8JG2fjxYAoVKufyDQ7sYMbiaGJ/T+9kB7aby97wt3nv65JK/GwZFA+H1QrRu+YrWZEdin3oIVo+unw36HObPjqNiqQehRdo4I8cd21tuEWhhKIMg86/ZEvjXPSWPkhiqfLFidxRhHsrVxIpc+tk11YX3KVMptOtVlc625TE+udOqsokLXgYDvi732yfE9qrkzbbd1ML2jDWv+9FQv6wjeNuHnma; FORWARDPAGE_KEY=https%3A%2F%2Fwww.macys.com%2Fshop%2Fproduct%2Fdr.-scholls-womens-no-chill-slip-on-sneakers%3FID%3D10204376%26CategoryID%3D56233%26sizes%3DWOMEN_SHOE_SIZE_T!!8%3B%3B8.5%26swatchColor%3DTan%252FBlack%2520Leopard; check=true; TLTSID=47381014370864944584677601668781; xdVisitorId=12017BE3OzR_oRPOIH54UFhuc5uH19sGbzaJCE6-uboc780BD50; AMCVS_8D0867C25245AE650A490D4C%40AdobeOrg=1; s_pers=%20v30%3Dproduct%7C1598499197822%3B%20c29%3Dmcom%253Apdp%253Asingle%253A10204376%253Awomens%2520no%2520chill%2520slip-on%2520sneakers%7C1598499729382%3B; s_sess=%20s_cc%3Dtrue%3B; bm_sv=DFD313CE96AAFE6BD3609E769A813026~TvESzGPp6Xssx+K/BHrFLuEal3xB8W31FUK1Oyyak7gy45gSWkJVfEPU6B3o2fFiB2lwK9s3TauxkmEulxPECATDxRMQWP5n/gTFlVm4Soj5hJ1fGeT5meMZRxDOXIwu2zfEZTcMAbnu86169RLAT7iQDT2TxMh1pnqz/fKvEaQ=; atgRecSessionId=G00t0KLi5u9YKdNlVAXUY-KZqAH34ubd5dqH-UNhOEOEb_2glhvk!-1713841853!93897707; s_fid=2D4F829CE7E58B73-26DEFAE6ADF3FA44; TS0132ea28=011c44459135c9e75a7aefce729c4d461ac86ec75b92de5d3de54f8c551ef15016a6111009ad3590a1686e544da14394336e0f9728; sto__session=1598496775152; sto__count=2; _uetsid=50d3e90100f04cc2ab39815d7ce438d6; _uetvid=9410dcc1ee615fd467023a7418fea156; BVBRANDSID=3755a33f-38ff-40fe-8562-f39a26ae386a',
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                   "Accept-Encoding": "gzip, deflate, br",
                   "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                   "Cache-Control": "max-age=0",
                   "Connection": "keep-alive",
                   "Host": "www.macys.com",
                   "Upgrade-Insecure-Requests": "1"}
        get_requests = requests.get(api_url, headers=headers, timeout=8)
        json_result = json.loads(get_requests.text, strict=False)
        json_message = json_result['product'][0]['traits']
        for x in json_message['sizes']['sizeMap'].keys():
            try:
                if stock_size==json_message['sizes']['sizeMap'][x]['name']:
                    if int(stock_color) in json_message['sizes']['sizeMap'][str(x)]['colors']:
                        key_message='true'
                        return key_message
                    else:
                        key_message='false'
                        return key_message
                return "下架"
            except(KeyError):return "下架"
    def no_stock(self,key_message,api_url):
        if key_message=='下架':
            self.up_data("UPDATE  domestic_wechatuser SET is_Replenishment='下架'WHERE api_url='%s'" % api_url)
        if key_message=='False' or key_message=='false':
            pass
        elif key_message=='True' or key_message=='true':
            self.up_data("UPDATE  domestic_wechatuser SET is_Replenishment='rim' WHERE api_url='%s'" % api_url)
        else:pass

    def is_stock(self,key_message,api_url):
        if key_message == '下架':
            self.up_data("UPDATE  domestic_wechatuser SET is_Replenishment='下架'WHERE api_url='%s'" % api_url)
        if key_message=='True' or key_message=='true':
            time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.up_data("UPDATE  domestic_wechatuser SET up_datetime='%s' WHERE api_url='%s'"%(time_now,api_url))
        elif key_message=='False' or key_message=='false':
            self.up_data("UPDATE  domestic_wechatuser SET is_Replenishment='no' WHERE api_url='%s'"%api_url)

    def spider_sephora_stock(self):
        while 1:
            try:
                self.write_data('\n' + "一次开始00000000000000000" + self.get_time())
                api_url_list, is_Replenishment_list, up_datetime_list=self.read_more_data("SELECT api_url,is_Replenishment,up_datetime FROM domestic_wechatuser")
                for i in range(len(is_Replenishment_list)):
                    try:
                        if is_Replenishment_list[i]=="yes":
                            time1 = datetime.datetime.strptime(self.get_time(), "%Y-%m-%d %H:%M:%S")
                            time0 = datetime.datetime.strptime(up_datetime_list[i], "%Y-%m-%d %H:%M:%S")
                            if (time1 - time0).seconds >= 1000:
                                if re.findall("\[[0-9]+/",api_url_list[i]):
                                    key_message = self.num_api_spider(api_url_list[i])
                                else:
                                    key_message = self.one_api_spider(api_url_list[i])
                                self.is_stock(key_message, api_url_list[i])
                                self.up_data("UPDATE  domestic_wechatuser SET up_datetime='%s' WHERE api_url='%s'" % (self.get_time(), api_url_list[i]))
                        elif is_Replenishment_list[i]=="no":
                            if re.findall("\[[0-9]+/", api_url_list[i]):
                                key_message = self.num_api_spider(api_url_list[i])
                            else:
                                key_message = self.one_api_spider(api_url_list[i])
                            self.no_stock(key_message, api_url_list[i])
                            self.up_data("UPDATE  domestic_wechatuser SET up_datetime='%s' WHERE api_url='%s'" % (self.get_time(), api_url_list[i]))
                        elif is_Replenishment_list[i]=="rim":
                            self.write_data('\n' +"这里有个时间差"+self.get_time())
                    except Exception as e :
                        self.write_data('\n' + '错误信息1：%s' % (str(e)) + self.get_time())
                        time.sleep(30)
                        continue
                self.write_data('\n' + "一次正常结束1111111111111111" + self.get_time())
                time.sleep(random.randint(10, 30) / 2)
            except Exception as e :
                self.write_data('\n' + '错误信息：%s' % (str(e)) + self.get_time())
                time.sleep(30)
                continue
if __name__ == '__main__':
    shop_stock = shop_stock()
    shop_stock.spider_sephora_stock()