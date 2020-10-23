import requests,json
#["oDTM_wagt61LT7O78U4RCpfAH1wA","oDTM_weV4rIITCTKTIpBuQ1jrGo8","oDTM_wY363mW-nkF2AfpBt_1YWJw","oDTM_we5FhJuS73jj3yDon2CJ9ZA","oDTM_wQEvz5ZNr1ouqAsx4qOQPmk","oDTM_wXaBj3yvmZZOy1Jx1taxsQM","oDTM_wUXTrczOF3JSd3kYZuqMYZk","oDTM_wYYRlJ9l7gxID_E8GKgakjE","oDTM_wfKGLBl46GjUaBZ1yBOZp2s","oDTM_wfaufC5haIclxG_FG-aseAA","oDTM_wZxSIFSdox4F3c64prFxmjY","oDTM_wbqQa8xIcyiZB-uK1sQVhpk","oDTM_wceN_cv03tiq4BSnan-8h0E","oDTM_wSZMxb0OXFswmsMGkV0AbQg","oDTM_wV6qhOYBtGOVgZ0ltMhxwSQ","oDTM_wbv0aOeV0UhwTuegx4eotrM","oDTM_wfyV12mff0edBmYqo0d_o3w","oDTM_wcymYZp9SHJrD8LE30YQy7c","oDTM_wb48wSGwVdyEeVMgXSNVLQc","oDTM_wSNDD2mHzssM92FDTA0a_UQ","oDTM_wUe59qZX9ZtjzFM_Ik2KdVE","oDTM_wcBeUoecNJVP1h-rUyNql24","oDTM_wT8bSoBVoZp5NgCC2lxMt2Y"],
# appid = "wx075e6145dec8e5e9"
# secret = "35d5b46369f00465c9eb82847be53d1e"
# grant_type = 'client_credential'
# token = "zyp123456789"
# url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=%s&appid=%s&secret=%s" % (grant_type, appid, secret)
# xx = requests.get(url=url)
# access_token = (xx.text.split('_token":"')[1].split('","expires_in')[0])
access_token="36_W2k5xWYahuy06Cyj4W16UUzeZz_f--rVLFC4m_h90Ldy-bYOaWBT9rK0VygDg9P8AS8w8vO1moGHdn1UyM4yVTxX1Uu5jGkv1nQ-XVkxg88NcIbb9mjSgOAEkB5WN6QnoR-ygyszGLWqDAbyEPPhAJAMXX"
url1="https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid="%access_token
xx=requests.get(url=url1)
json_result = json.loads(xx.text, strict=False)
openid_list=json_result['data']['openid']
url2="https://api.weixin.qq.com/cgi-bin/message/mass/send?access_token=%s"%access_token
data={
   "touser":openid_list,
    "msgtype": "text",
    "text": { "content": "微信公众号新增美国卡泡（https://colourpop.com）以及梅西（https://www.macys.com）补货通知，按照指示成功关注商品后，商品补货时微信公众号会第一时间通知到您，感谢您的使用！！"}
}
def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError
# data_message = json.dumps(data, default=set_default).encode("utf8")
data_message = json.dumps(data, ensure_ascii=False,indent=2).encode('utf-8')#需要指定json编码的时候不会对中文转码为unicode，否则群发的消息会显示为unicode码,不能正确显示
xx=requests.post(url=url2, data=data_message)
# xx=requests.post(url=url,data=data)
print(xx.text)

