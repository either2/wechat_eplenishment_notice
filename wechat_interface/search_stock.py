#coding:utf-8
from  flask import Flask,request
import requests,json,re
from bs4 import BeautifulSoup
class judeg_url:
    try:
        pass
    except:
        pass
    # def is_pid(self,url):
    #     xx = re.findall(r'P\d+', url, re.I)
    #     if len(xx)>1:
    #         if xx[0].upper()==xx[1].upper():
    #             pid=xx[0].upper()
    #             return pid
    #     elif len(xx)==1:
    #         pid=xx[0].upper()
    #         return pid
    #     elif len(xx) == 0:
    #         pid=None
    #         return pid
    #
    # def is_sku(self, url):
    #     aa = re.findall(r'skuId=\d+', url, re.I)
    #     if len(aa) == 1:
    #         sduid = aa[0].split('=')[1]
    #         return sduid
    #     if len(aa) == 0:
    #         stuid = None
    #         return stuid

    # def judeg_url(self,url):
    #     pid=self.is_pid(url)
    #     stuid=self.is_sku(url)
    #     if pid!=None and stuid!=None:
    #         api_url = "https://www.sephora.com/api/users/profiles/current/product/%s?skipAddToRecentlyViewed=false&preferedSku=%s"%(pid,stuid)
    #     elif pid!=None and stuid==None:
    #         api_url="https://www.sephora.com/api/users/profiles/current/product/%s"%pid
    #     elif pid==None:
    #         api_url="wrong"
    #     else:
    #         api_url="wrong"
    #         return api_url
    #     return api_url,pid,stuid

    def sephora_stock_message(self,url):
        "前端色号列表在css-1j1jwa4，选中的颜色在css-cl742e标签里,所有色号都在css-6qi1i9标签里"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
        r = requests.get(url=url, headers=headers)
        r.encoding = 'utf8'
        demo = r.text  # 服务器返回响应
        soup = BeautifulSoup(demo, "html.parser")
        no_stock_message = soup.find("h1", class_="css-1wag3se e65zztl0")
        if no_stock_message != None:
            return "不存在该商品"
        else:
            color_list = []
            color_num_list = []
            message_dict = {}
            message = []
            soup_stock_name = soup.find("h1", class_="css-1wd4e6l e65zztl0")
            stock_name = str(soup_stock_name).split('<span>')[-1].split('</')[0].replace('™','')
            color_num_api = "https://www.sephora.com/api/users/profiles/current/full?=&skipApis=targetersResult&productId=%s" % (
                re.findall("P[0-9]+", url)[0])
            soup_color_num = requests.get(url=color_num_api, headers=headers).text
            json_color_num = json.loads(soup_color_num)
            if soup.find("div", class_="css-6qi1i9") == None:
                stock_num = json_color_num['product']['currentSku']['skuId']
                message_dict['stock_message'] = ['(' + '单品' + ')' + stock_num]
                message_dict[
                    'stock_image'] = 'https://www.sephora.com/productimages/sku/s%s-main-zoom.jpg?imwidth=300' % stock_num
                message_dict['stock_name'] = stock_name
                message_dict["website_name"] = "sephora"
            else:
                for i in soup.findAll("div", class_="css-6qi1i9"):
                    for x in i.contents:
                        color_or_size_message = str(x).split('aria-label="')[1].split('"')[0]
                        if color_or_size_message == "":
                            new_color_or_size_message = str(x).split('">')[-1].split('</')[0]
                            color_list.append(new_color_or_size_message)
                        else:
                            color_list.append(color_or_size_message)
                if len(color_list) == 1:
                    color_num_list.append(json_color_num['product']['currentSku']['skuId'])
                elif len(color_list) > 1:
                    for i in json_color_num['product']['regularChildSkus']:
                        color_num_list.append(i['skuId'])
                    color_num_list.append(json_color_num['product']['currentSku']['skuId'])
                is_add = False
                for x in range(len(color_list)):
                    if 'Selected' in color_list[x]:
                        message.append('(' + color_list[x] + ')' + color_num_list[-1])
                        is_add = True
                    else:
                        if is_add:
                            message.append('(' + color_list[x] + ')' + color_num_list[x - 1])
                        else:
                            message.append('(' + color_list[x] + ')' + color_num_list[-1])
                stock_num = color_num_list[-1]
                message_dict['stock_message'] = message
                message_dict[
                    'stock_image'] = 'https://www.sephora.com/productimages/sku/s%s-main-zoom.jpg?imwidth=300' % stock_num
                message_dict['stock_name'] = stock_name
                message_dict["website_name"] = "sephora"
            return message_dict
        # global color_message, stock_size
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
        # r = requests.get(url=url, headers=headers)
        # r.encoding = 'utf8'
        # demo = r.text  # 服务器返回响应
        # soup = BeautifulSoup(demo, "html.parser")
        # stock_soup_color = soup.findAll('button', class_='css-1j1jwa4')  # 色号列表
        # stock_soup_size = soup.find('div', class_='css-1nfx0y4 e65zztl0')  # 商品大小  css-1cvjr95
        # stock_soup_size2 = soup.findAll('button', class_='css-1q3i4ga')
        #
        # if len(stock_soup_size2) > 1:
        #     if "skuId=" not in url:
        #         color_soup = soup.find('span', class_='css-ta42ek e65zztl0')
        #         stock_size = str(color_soup).split('">')[1].split('</')[0]
        #         return stock_size
        #     elif "skuId=" in url:
        #         skuid = str(re.findall('skuId=\d+', url)[0])
        #         for x in stock_soup_size2:
        #             if skuid.split("skuId=")[1] in str(x):
        #                 stock_size = str(x).split('aria-label="')[1].split('"')[0]
        #                 return stock_size
        #         color_soup = soup.find('span', class_='css-ta42ek e65zztl0')
        #         # color_message = str(color_soup).split("COLOR:")[1].split("</span>")[0].replace("<!-- -->", " ")
        #         stock_size = str(color_soup).split('">')[1].split('</')[0]
        #         return stock_size
        #
        # if len(stock_soup_color) == 0:
        #     color_soup = soup.find('span', class_='css-ta42ek e65zztl0')  # css-ng5oyv
        #     if color_soup != None:
        #         if "COLOR:" in str(color_soup):
        #             color_message = str(color_soup).split('">')[1].split("</")[0].replace("<!-- -->", " ")
        #     else:
        #         color_message = "无"
        # if stock_soup_size == None:
        #     stock_size = '无'
        #
        # if stock_soup_size != None:
        #     try:
        #         stock_size = str(stock_soup_size).split('>')[1].split("<")[0]
        #     except:
        #         stock_size = "暂无"
        #
        # if len(stock_soup_color) > 1:
        #     if "skuId=" not in url:
        #         color_soup = soup.find('span', class_='css-ta42ek e65zztl0')
        #         color_message = str(color_soup).split('">')[1].split("</")[0].replace("<!-- -->", " ")
        #     elif "skuId=" in url:
        #         skuid = str(re.findall('skuId=\d+', url)[0])
        #         is_color_message = False
        #         for x in stock_soup_color:
        #             if skuid.split("skuId=")[1] in str(x):
        #                 color_message = str(x).split('aria-label="')[1].split('"')[0]
        #                 is_color_message = True
        #         if is_color_message == False:
        #             color_soup = soup.find('span', class_='css-ta42ek e65zztl0')
        #             color_message = str(color_soup).split('">')[1].split("</")[0].replace("<!-- -->", " ")
        # elif len(stock_soup_color) == 1:
        #     color_message = "无"
        #
        # if "无" in color_message and "无" in stock_size:
        #     try:
        #         size_soup = soup.find('div', class_='css-128n72s e65zztl0')
        #         stock_size = re.findall('SIZE.*?<', str(size_soup))[0].replace('<', '')
        #         return stock_size
        #     except:
        #         pass
        # return "%s (%s)" % (color_message, stock_size)

    def pop_stock_message(self,url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
        r = requests.get(url=url, headers=headers)
        r.encoding = 'utf8'
        demo = r.text
        soup = BeautifulSoup(demo, "html.parser")
        message_dict = {}
        stock_message=["单品"]
        try:
            if soup.find('input', class_='quantity product-actions__quantity--input') !=None:
                stock_image=soup.find('div', class_='product-images__carousel product-images__carousel--desktop hidetablet')
                big_stock_image_url=str(stock_image).split('data-src="')[1].split('"')[0]
                pic_size=re.findall("[0-9]+x[0-9]+",str(stock_image).split('data-src="')[1].split('"')[0])[0]
                stock_image_url="https:"+big_stock_image_url.replace(pic_size,"300x")
                stock_name = soup.find('label', class_='product-details__title').string
                message_dict["stock_message"] = stock_message
                message_dict["stock_image"] = stock_image_url
                message_dict["stock_name"] = stock_name
                message_dict["website_name"] = "colourpop"
                return message_dict
        except(json.decoder.JSONDecodeError):
            api_url = url + "?view=json"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
            r = requests.get(url=api_url, headers=headers)
            r.encoding = 'utf8'
            demo = r.text
            soup = BeautifulSoup(demo, "html.parser")
            stock_soup_color = soup.find('h1', class_='404__hero-content--title')
            if "OMG" in str(stock_soup_color):
                return None
        except Exception as E:
            return "商品链接错误"
    def belk_stock_message(self,url):
        # if re.findall("\[[0-9]+\]",url):
        #     user_stock_id=re.findall("[0-9]+",re.findall("\[[0-9]+\]",url)[0])[0]
        # else:user_stock_id='None'
        stock_name=url.split("p/")[1].split("/")[0]
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0"}
            r = requests.get(url=url, headers=headers)
            r.encoding = 'utf8'
            demo = r.text
            soup = BeautifulSoup(demo, "html.parser")
            stock_soup_color = soup.find('script', id='colorSizeMapping')
        except:return "查询失败，请稍后再试 > <"
        message_dict = {}
        message = []
        if "colorToSize" not in str(stock_soup_color): #无颜色或大小
            stock_soup_color = soup.find('head').find_next("script", id="notify-lib-js").find_next("script")
            json_list = json.loads('{"' + str(stock_soup_color).split('{"')[1].split("};")[0] + '}')
            stock_name = json_list['product_name'][0]
            color_message = json_list['product_color'][0]
            size_message = json_list['product_size'][0]
            stock_id = json_list['sku_id'][0]
            # api_url = "https://www.belk.com/on/demandware.store/Sites-Belk-Site/default//Product-GetRealTimeInventory?pid=" + stock_id
            soup_image = soup.find("div", class_="product-col-1 product-image-container").find_next("img")
            stock_image_url="https://belk.scene7.com/is/image/Belk?layer=0&src=" + str(soup_image).split("src=")[2].split("&amp")[0]
            message.append("(%s/%s)%s"%(color_message,size_message,stock_id))
            message_dict["stock_message"]=message
            message_dict["stock_image"]=stock_image_url
            message_dict["stock_name"] = stock_name
            message_dict["website_name"] = "belk"
            return message_dict
            # return '商品名：%s，商品颜色：%s，商品大小：%s' % (stock_name, color_message, size_message) + stock_image_url
        else:
            json_list = '{"colorToSize' + str(stock_soup_color).split("colorToSize")[1].split("};")[0] + '}'
            json_message = json.loads(json_list)
            for x in json_message['colorToSize'].keys():
                color_message = json_message['colors'][x]['name']
                for y in json_message['colorToSize'][x].keys():
                    for i in json_message['sizes']:
                        if y == i['id']:
                            size_message = i['name']
                            stock_id = json_message['colorToSize'][x][y]
                            message.append('('+color_message + '/' + size_message +')'+ stock_id)
            json_list = '{"colorToSize' + str(stock_soup_color).split("colorToSize")[1].split("};")[0] + '}'
            json_message = json.loads(json_list)
            stock_image_url="https"+str(json_message["colors"]).split("https")[1].split("'")[0]
            message_dict["stock_message"]=message
            message_dict["stock_image"]=stock_image_url
            message_dict["stock_name"] = stock_name
            message_dict["website_name"] = "belk"
            return message_dict



        # json_list = '{"colorToSize' + str(stock_soup_color).split("colorToSize")[1].split("};")[0] + '}'
        # json_message = json.loads(json_list)
        # message = ''
        # is_only_color=len(json_message['colors'].keys())
        # is_only_size=len(json_message['sizes'])
        # if is_only_color==1 and is_only_size==1:
        #     # if user_stock_id !='None':
        #     #     return "该商品无多个色号或尺寸，请勿添加编号"
        #     for x in json_message['colorToSize'].keys():
        #         color_message = json_message['colors'][x]['name']
        #         for y in json_message['colorToSize'][x].keys():
        #             for i in json_message['sizes']:
        #                 if y == i['id']:
        #                     size_message = i['name']
        #                     stock_id = json_message['colorToSize'][x][y]
        #                     api_url="https://www.belk.com/on/demandware.store/Sites-Belk-Site/default//Product-GetRealTimeInventory?"+stock_id
        #                     sock_message = '商品名：%s，商品颜色：%s，商品大小：%s'%(stock_name,color_message,size_message)+api_url
        #                     return sock_message
        # else:
        #     if user_stock_id != 'None':
        #         for x in json_message['colorToSize'].keys():
        #             if [k for k, v in json_message['colorToSize'][x].items() if v == user_stock_id]:
        #                 size_id=[k for k, v in json_message['colorToSize'][x].items() if v == user_stock_id]
        #                 color_message=json_message['colors'][x]['name']
        #                 for i in json_message['sizes']:
        #                     if i['id']==size_id[0]:
        #                         api_url = "https://www.belk.com/on/demandware.store/Sites-Belk-Site/default//Product-GetRealTimeInventory?" + user_stock_id
        #                         size_message=i['name']
        #                         return '商品名：%s，商品颜色：%s，商品大小：%s'%(stock_name,color_message,size_message)+api_url
        #         return '您指明的编号不在已知列表中，请核实后重新关注'
        #     stock_id='0438662010417'
        #     for x in json_message['colorToSize'].keys():
        #         color_message = json_message['colors'][x]['name']
        #         for y in json_message['colorToSize'][x].keys():
        #             for i in json_message['sizes']:
        #                 if y == i['id']:
        #                     size_message = i['name']
        #                     stock_id = json_message['colorToSize'][x][y]
        #                     message += '('+color_message + '/' + size_message +')'+'---' + stock_id + '\n'
        #     return message+"该商品包含多个颜色或尺寸，以上信息为（颜色/尺寸---该颜色与尺寸对应编号）"+'\n'+'请在关注时的地址后面加上[色号/尺码]指明商品的颜色编号和尺寸。示例:%s[%s]'%(url,stock_id)

    def verification(self,url):

        if "sephora.com" in url:
            try:
                return self.sephora_stock_message(url)
            except:return "查询失败，请核对商品链接或稍后再试"

            #         json_spider = json.loads(get_requests)
            # api_url, pid, stuid = self.judeg_url(url)
            # try:
            #     if api_url != "wrong":
            #         get_requests = requests.get(api_url, timeout=6).text
            #         json_spider = json.loads(get_requests)
            #         try:
            #             pid2 = str(json_spider['productId'])
            #             stuid2 = str(json_spider['currentSku']['skuId'])
            #             if (pid == pid2 and stuid == stuid2):
            #                 color_message = self.sephora_stock_message(url)
            #                 stock_name = str(url).split("product/")[1].split("-P")[0]
            #                 return "商品名:%s(-中文名-),商品编号：%s,商品信息：%s" % (stock_name, stuid2, color_message) + api_url
            #             elif pid == pid2 and stuid == None:
            #                 color_message = self.sephora_stock_message(url)
            #                 stock_name = str(url).split("product/")[1].split("-P")[0]
            #                 api_url2 = "https://www.sephora.com/api/users/profiles/current/product/%s?skipAddToRecentlyViewed=false&preferedSku=%s" % (
            #                 pid, stuid2)
            #                 return "商品名:%s(-中文名-),商品编号：%s,商品信息：%s" % (stock_name, stuid2, color_message) + api_url2
            #         except(KeyError):
            #             erroy_message = str(json_spider['errors']['invalidInput'])
            #             if re.findall('There is no matching product for the product', erroy_message):
            #                 return ("抱歉没有这个商品哟")
            #     else:
            #         return "商品链接错误"
            # except:
            #     return "出错啦，请稍后再试"

        if "colourpop.com" in url:
            apiurl=url+"?view=json"
            try:
                if self.pop_stock_message(url) !=None:
                    return self.pop_stock_message(url)
                else:return "抱歉没有这个商品哟"
            except:return "查询失败，请核对商品链接或稍后再试"


        if "belk.com" in url:
            try:
                return self.belk_stock_message(url)
            except:return "查询失败，请核对商品链接或稍后再试"
# app = Flask(__name__)
# @app.route("/stockmessage", methods=["POST"])
# def stockmessage():
#     try:
#         stock_url = request.form.get("url")
#         return judeg_url().verification(stock_url)
#     except:
#         return "发生错误，请稍后再试"
# app.run(host="0.0.0.0", port=2335)

if __name__ == '__main__':
    print(judeg_url().verification("https://www.sephora.com/product/allure-homme-sport-P70400?icid2=products%20grid:p70400"))


