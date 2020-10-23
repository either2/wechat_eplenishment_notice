#coding:gbk
from  flask import Flask,request,jsonify
import requests,json,re
from bs4 import BeautifulSoup
class judeg_url:
    def is_pid(self,url):
        xx = re.findall(r'P\d+', url, re.I)
        if len(xx)>1:
            if xx[0].upper()==xx[1].upper():
                pid=xx[0].upper()
                return pid
        elif len(xx)==1:
            pid=xx[0].upper()
            return pid
        elif len(xx) == 0:
            pid=None
            return pid

    def is_sku(self, url):
        aa = re.findall(r'skuId=\d+', url, re.I)
        if len(aa) == 1:
            sduid = aa[0].split('=')[1]
            return sduid
        if len(aa) == 0:
            stuid = None
            return stuid

    def judeg_url(self,url):
        pid=self.is_pid(url)
        stuid=self.is_sku(url)
        if pid!=None and stuid!=None:
            api_url = "https://www.sephora.com/api/users/profiles/current/product/%s?skipAddToRecentlyViewed=false&preferedSku=%s"%(pid,stuid)
        elif pid!=None and stuid==None:
            api_url="https://www.sephora.com/api/users/profiles/current/product/%s"%pid
        elif pid==None:
            api_url="wrong"
        else:
            api_url="wrong"
            return api_url
        return api_url,pid,stuid

    def stock_message(self,url):
    # try:
        global color_message, stock_size
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
        r = requests.get(url=url, headers=headers)
        r.encoding = 'utf8'
        demo = r.text  # 服务器返回响应
        soup = BeautifulSoup(demo, "html.parser")
        stock_soup_color = soup.findAll('button', class_='css-1j1jwa4')  # 色号列表
        stock_soup_size = soup.find('div', class_='css-1nfx0y4 e65zztl0')  # 商品大小  css-1cvjr95
        stock_soup_size2 = soup.findAll('button', class_='css-1q3i4ga')

        if len(stock_soup_size2)>1:
            if "skuId=" not in url:
                color_soup = soup.find('span', class_='css-ta42ek e65zztl0')
                stock_size = str(color_soup).split('">')[1].split('</')[0]
                return stock_size
            elif "skuId=" in url:
                skuid = str(re.findall('skuId=\d+', url)[0])
                for x in stock_soup_size2:
                    if skuid.split("skuId=")[1] in str(x):
                        stock_size = str(x).split('aria-label="')[1].split('"')[0]
                        return stock_size
                color_soup = soup.find('span', class_='css-ta42ek e65zztl0')
                # color_message = str(color_soup).split("COLOR:")[1].split("</span>")[0].replace("<!-- -->", " ")
                stock_size = str(color_soup).split('">')[1].split('</')[0]
                return stock_size


        if len(stock_soup_color) == 0:
            color_soup=soup.find('span', class_='css-ta42ek e65zztl0')    #   css-ng5oyv
            if  color_soup!=None:
                if "COLOR:" in str(color_soup):
                    color_message=str(color_soup).split('">')[1].split("</")[0].replace("<!-- -->", " ")
                    print("cccccccccccc")
            else:color_message="无"
        if stock_soup_size == None:
            stock_size = '无'

        if stock_soup_size != None:
            try:
                stock_size=str(stock_soup_size).split('>')[1].split("<")[0]
                # if len(stock_soup_color) == 0:
                #     print("999999999999999")
                #     color_soup = soup.find('span', class_='css-ta42ek e65zztl0')
                #     print(color_soup)
                #     stock_size = str(color_soup).split('">')[1].split("</span>")[0]
                # else:
                #     print("-------------------------")
                #     stock_size = str(stock_soup_size).split(">")[1].split("</div>")[0]
            except:
                stock_size = "暂无"

        if len(stock_soup_color) >1:
            if "skuId=" not in url:
                color_soup = soup.find('span', class_='css-ta42ek e65zztl0')
                print(color_soup)
                color_message = str(color_soup).split('">')[1].split("</")[0].replace("<!-- -->", " ")
            elif "skuId=" in url:
                skuid = str(re.findall('skuId=\d+', url)[0])
                is_color_message=False
                for x in stock_soup_color:
                    if skuid.split("skuId=")[1] in str(x):
                        color_message = str(x).split('aria-label="')[1].split('"')[0]
                        is_color_message=True
                if is_color_message==False:
                    color_soup = soup.find('span', class_='css-ta42ek e65zztl0')
                    color_message = str(color_soup).split('">')[1].split("</")[0].replace("<!-- -->", " ")
        elif len(stock_soup_color) ==1:
            color_message="无"

        if "无" in color_message and "无" in stock_size:
            try:
                size_soup=soup.find('div', class_='css-128n72s e65zztl0')
                stock_size=re.findall('SIZE.*?<',str(size_soup))[0].replace('<','')
                return stock_size
            except:pass
        return "%s (%s)"%(color_message,stock_size)

    def verification(self,url):
        api_url,pid,stuid=self.judeg_url(url)
        try:
            if api_url!="wrong":
                get_requests = requests.get(api_url, timeout=6).text
                json_spider = json.loads(get_requests)
                try:
                    pid2 = str(json_spider['productId'])
                    stuid2 = str(json_spider['currentSku']['skuId'])
                    if (pid==pid2 and stuid==stuid2):
                        color_message=self.stock_message(url)
                        stock_name=str(url).split("product/")[1].split("-P")[0]
                        return "商品名:%s(-中文名-),商品编号：%s,商品信息：%s"%(stock_name,stuid2,color_message)+api_url
                    elif pid == pid2 and stuid==None:
                        color_message = self.stock_message(url)
                        stock_name=str(url).split("product/")[1].split("-P")[0]
                        api_url2 = "https://www.sephora.com/api/users/profiles/current/product/%s?skipAddToRecentlyViewed=false&preferedSku=%s" % (pid, stuid2)
                        return "商品名:%s(-中文名-),商品编号：%s,商品信息：%s"%(stock_name,stuid2,color_message)+api_url2
                except(KeyError):
                    erroy_message=str(json_spider['errors']['invalidInput'])
                    if re.findall('There is no matching product for the product',erroy_message):
                        return ("抱歉没有这个商品哟")
                except:return "出错啦，稍后再试"
            else:return "商品链接错误"
        except:return "出错啦，请稍后再试"

# app = Flask(__name__)
# @app.route("/stockmessage", methods=["POST"])
# def stockmessage():
#     try:
#         stock_url = request.form.get("url")
#         return judeg_url().verification(stock_url)
#     except:
#         return "发生错误，请稍后再试"
#
# app.run(host="0.0.0.0", port=2333)
if __name__ == '__main__':
    print(judeg_url().verification("https://www.sephora.com/product/lock-it-blotting-powder-P418800?skuId=1914472"))

