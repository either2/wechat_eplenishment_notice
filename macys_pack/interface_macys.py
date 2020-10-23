import random
from  flask import Flask,request  #应该用apiurl地址来判断商品是否已存在数据库中
import requests,json,re
class juge_macsy_url:
    try:
        def multiple_color_size(self,json_message):
            color_message = '商品颜色与颜色编码'
            for i in json_message['colors']['colorMap'].keys():
                color_name = json_message['colors']['colorMap'][i]['name']
                # color_num=json_message['colors']['colorMap'][i]['id']
                color_message += '\n' + '%s ---%s' % (color_name, i)
            if len(json_message['sizes']['sizeMap'].keys()) > 1:
                size_message = '商品尺寸大小包括：'
                for x in json_message['sizes']['sizeMap'].keys():
                    size = json_message['sizes']['sizeMap'][x]['name']
                    size_message += '(%s)  ' % size
            else:
                size_message = ''
            totle_message = color_message + '\n' + size_message
            random_color = random.choice(list(json_message['colors']['colorMap']))
            random_size=json_message['sizes']['sizeMap'][random.choice(list(json_message['sizes']['sizeMap']))]['name']
            return totle_message,random_color,random_size
        def url_requests(self,api_url):
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
                       "Cookie": 'SEED=-3293640680221306390%7C%7C418-20%2C485-20%2C566-21; _abck=B03C6961D0F3CFC7A374AEBCF5666EA8~-1~YAAQL/B33zOO1SJ0AQAABK3mLQS6vyq5rww/9KG7dFCQYYCsqoC4V+L4UP6J0b6uW575YZoJj1P/mgYoVeJJQcYqv05J1+dRVBk/LMrpks469/rRXECBQ20oFP25CHQQoQNWGgEBHgdxu/u/g4kvJN6zTlJSVqXTynF/Y6K891G/ASnpvFMnlHgH50tWdjm2sY6Z4YYZSraxMCqrQ7QIU/w8xQSyYrYj7JhbCfuYtqBjkoV+KeiB4MFlalxYG48DqfpAGlgdTuvHU4zkQVtQyT1laFZvkPtStq99bomgH6baXt1jel+0zCAkAFG09LUlbWenJ7H/Ww==~-1~-1~-1; AMCV_8D0867C25245AE650A490D4C%40AdobeOrg=-1891778711%7CMCIDTS%7C18501%7CMCMID%7C18246968150624710560921075543064693367%7CMCAAMLH-1598857801%7C11%7CMCAAMB-1599101282%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1598503682s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-18506%7CvVersion%7C2.4.0; mbox=PC#f44d49032569405db80b0a0409598278.38_0#1661497802|session#107e1dd5218c49e4900d2f2b9ee430c9#1598499257; utag_main=v_id:01713feaf045002ba7a1f9520c900104e001600d00978$_sn:6$_ss:0$_st:1598499727004$vapi_domain:macys.com$ses_id:1598496481380%3Bexp-session$_pn:6%3Bexp-session; _ga=GA1.2.219375090.1585915301; smtrrmkr=637340941975487689%5E01713feb-0e20-44ce-9919-456a1ec34e5a%5E01742dd0-a4a0-4272-9aa8-80f48d70f877%5E0%5E104.168.173.132; cto_bundle=x6HDrF8lMkYwNTEwaDJxN2d3Sm85UHhiNE9jTSUyQk91M1EwNWlzeVZUWHhiNm0zeE1sNmhiZzdJWVBmU0Rmd0tXJTJGUEFmVHgzc3BXcExhWERFUGtCRDJnQnhIWEREdHpYSlcwQyUyQmtEWFhUUzRHbjRUYTJ5MXFQckJ1QVQlMkZvaGo4dTd5TVNKWUpxdDRPT1NUdlV6RXBsZ05PQTMyakNRJTNEJTNE; cd_user_id=1713feb2151161-020d582e5986418-4c302f7e-144000-1713feb215240f; CONSENTMGR=ts:1585915307160%7Cconsent:true; RTD=e7aae70e7a9d40e7a6170e7a4010e7a7f50e7ab530e7a4e90e7a7a00; atgRecVisitorId=12017BE3OzR_oRPOIH54UFhuc5uH19sGbzaJCE6-uboc780BD50; RT="z=1&dm=macys.com&si=1fd02135-153e-45b3-a46e-0478bb954deb&ss=kec7j3y5&sl=8&tt=eexb&bcn=%2F%2F684d0d37.akstat.io%2F&obo=5"; _gid=GA1.2.1335125292.1598410438; sto__vuid=1ef150e98c72787540d7bd29d3da1d6e; BVBRANDID=1d3742b1-cfa2-4243-870f-0966ed929953; CRTOABE=0; shippingCountry=US; currency=USD; SignedIn=0; GCs=CartItem1_92_03_87_UserName1_92_4_02_; akavpau_www_www1_macys=1598498220~id=07fef41c85e63f95f06339c39c9cedba; bm_sz=2890D9BD32798E9E5B39658910BE3165~YAAQNfh338PdiyN0AQAAHpLQLQj0jNCHwXc4VGVcp+Lb7DyyGI/tlTDrYJ6ZLvfAJTZLM7ILg1l3O7jOfEqAiZiC0Hf4WC6Vup1nwDooCZIYAw0OCZ3rBzt574aXJIqcmD7lzPgaUL2Sda7pcoMtwrhBQPuQMadJbt/XCT44Ozh5QzHjJfcGXswzYIF65GQ=; mercury=true; ak_bmsc=EFFC347CCE54BFB785405561C6508D12DF77F835104C0000DE1E475F6ECD6210~plbFv2hs4IYBi4uuRUl5QAK2QQhnzpmVDUyHRTU8JG2fjxYAoVKufyDQ7sYMbiaGJ/T+9kB7aby97wt3nv65JK/GwZFA+H1QrRu+YrWZEdin3oIVo+unw36HObPjqNiqQehRdo4I8cd21tuEWhhKIMg86/ZEvjXPSWPkhiqfLFidxRhHsrVxIpc+tk11YX3KVMptOtVlc625TE+udOqsokLXgYDvi732yfE9qrkzbbd1ML2jDWv+9FQv6wjeNuHnma; FORWARDPAGE_KEY=https%3A%2F%2Fwww.macys.com%2Fshop%2Fproduct%2Fdr.-scholls-womens-no-chill-slip-on-sneakers%3FID%3D10204376%26CategoryID%3D56233%26sizes%3DWOMEN_SHOE_SIZE_T!!8%3B%3B8.5%26swatchColor%3DTan%252FBlack%2520Leopard; check=true; TLTSID=47381014370864944584677601668781; xdVisitorId=12017BE3OzR_oRPOIH54UFhuc5uH19sGbzaJCE6-uboc780BD50; AMCVS_8D0867C25245AE650A490D4C%40AdobeOrg=1; s_pers=%20v30%3Dproduct%7C1598499197822%3B%20c29%3Dmcom%253Apdp%253Asingle%253A10204376%253Awomens%2520no%2520chill%2520slip-on%2520sneakers%7C1598499729382%3B; s_sess=%20s_cc%3Dtrue%3B; bm_sv=DFD313CE96AAFE6BD3609E769A813026~TvESzGPp6Xssx+K/BHrFLuEal3xB8W31FUK1Oyyak7gy45gSWkJVfEPU6B3o2fFiB2lwK9s3TauxkmEulxPECATDxRMQWP5n/gTFlVm4Soj5hJ1fGeT5meMZRxDOXIwu2zfEZTcMAbnu86169RLAT7iQDT2TxMh1pnqz/fKvEaQ=; atgRecSessionId=G00t0KLi5u9YKdNlVAXUY-KZqAH34ubd5dqH-UNhOEOEb_2glhvk!-1713841853!93897707; s_fid=2D4F829CE7E58B73-26DEFAE6ADF3FA44; TS0132ea28=011c44459135c9e75a7aefce729c4d461ac86ec75b92de5d3de54f8c551ef15016a6111009ad3590a1686e544da14394336e0f9728; sto__session=1598496775152; sto__count=2; _uetsid=50d3e90100f04cc2ab39815d7ce438d6; _uetvid=9410dcc1ee615fd467023a7418fea156; BVBRANDSID=3755a33f-38ff-40fe-8562-f39a26ae386a',
                       "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                       "Accept-Encoding": "gzip, deflate, br",
                       "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                       "Cache-Control": "max-age=0",
                       "Connection": "keep-alive",
                       "Host": "www.macys.com",
                       "Upgrade-Insecure-Requests": "1"}
            xx = requests.get(url=api_url, headers=headers)  # headers要放完整
            json_result = json.loads(xx.text, strict=False)
            return json_result
        def is_only(self,url):
            if "ID=" not in url:
                return "请使用完整的商品地址"
            api_url = "https://www.macys.com/xapi/digital/v1/product/" +re.findall("\?ID=" + '[0-9]+', url)[0].split("=")[1]
            if re.findall("\[[0-9]+/",url):
                stock_message=re.findall("\[[0-9]+/.*", url)[0]
                stock_color=stock_message.split("/")[0].split("[")[1]
                stock_size=stock_message.split("/")[1].split("]")[0]
                json_result = self.url_requests(api_url)
                json_message = json_result['product'][0]['traits']
                if "colors" in json_message.keys():
                    if 'colorMap'in json_message['colors'].keys():
                        size_list=[]
                        try:
                            for x in json_message['sizes']['sizeMap'].keys():
                                size = json_message['sizes']['sizeMap'][x]['name']
                                size_list.append(size)
                        except:return "该商品无多个尺寸，请勿添加色号编号和大小"
                        if stock_color in json_message['colors']['colorMap'].keys() and stock_size in size_list:
                            stock_name = json_result['product'][0]['detail']['name']
                            color_message=json_message['colors']['colorMap'][stock_color]['name']
                            return "商品名：%s,商品颜色：%s,商品大小：%s"%(stock_name,color_message,stock_size)+api_url+"[%s/%s]"%(stock_color,stock_size)
                        else:return '您指明的商品色号或大小不在已知列表中，请核实后重新关注'
                    else:return '该商品无色号，请勿添加色号编号和大小'
                else:return '该商品无色号，请勿添加色号编号和大小'
            else:
                json_result = self.url_requests(api_url)
                json_message=json_result['product'][0]['traits']
                stock_name=json_result['product'][0]['detail']['name']
                if "colors" in json_message.keys():
                    if 'colorMap'in json_message['colors'].keys():
                        if len(json_message['colors']['colorMap'].keys()) == 1:
                            if "sizes" in json_message.keys():
                                if len(json_message['sizes']['sizeMap'].keys()) == 1:
                                    color_id=json_message['colors']['selectedColor']
                                    color_message=json_message['colors']['colorMap'][str(color_id)]['name']
                                    size_message=json_message['sizes']['sizeMap']['0']['name']
                                    return "商品名：%s,商品颜色：%s,商品大小%s"%(stock_name,color_message,size_message)+api_url #该商品只有一个色号,一个大小  直接关注
                                elif len(json_message['sizes']['sizeMap'].keys()) > 1:
                                    totle_message,random_color,random_size=self.multiple_color_size(json_message)
                                    return totle_message+'\n'+'该商品包括多个尺寸，请在关注时的地址后面加上 [色号/尺码] 指明商品的颜色编号和尺寸。示例:%s[%s/%s]'%(url,random_color,random_size)
                                    # return "该商品有多个大小，请联系那个他关注"
                            else:
                                color_id = json_message['colors']['selectedColor']
                                color_message = json_message['colors']['colorMap'][str(color_id)]['name']
                                return "商品名：%s,商品颜色：%s"%(stock_name,color_message)+api_url # "该商品只有一个色号,无大小"  直接关注
                        elif len(json_message['colors']['colorMap'].keys()) > 1:#多颜色一个尺寸与多颜色多尺寸的处理情况相同，反之一样
                            totle_message,random_color,random_size=self.multiple_color_size(json_message)
                            return totle_message+'\n'+'该商品包括多个颜色和尺寸，请在关注时的地址后面加上[色号/尺码]指明商品的颜色编号和尺寸。示例:%s[%s/%s]'%(url,random_color,random_size)
                        # else:return "该商品有多个色号，请联系那个他关注"
                    else:return "商品名：%s"%stock_name+api_url  #无颜色标签但有多个大小的情况未覆盖
                else:return "商品名：%s"%stock_name+api_url
    except Exception as E :
        with open("./wechat_development.txt", 'a', encoding='utf8') as f:
            f.write(str(E))

# app = Flask(__name__)
# @app.route("/stockmessage", methods=["POST"])
# def stockmessage():
#     try:
#         stock_url = request.form.get("url")
#         return juge_macsy_url().is_only(stock_url)
#     except:
#         return "发生错误，请稍后再试"
#
# app.run(host="0.0.0.0", port=2334)
if __name__ == '__main__':
    aaa=juge_macsy_url().is_only("https://www.macys.com/shop/product/fitbit-charge-4-black-band-touchscreen-smart-watch-22.6mm?ID=11041254")
    print(aaa)