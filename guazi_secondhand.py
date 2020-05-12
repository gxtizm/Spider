'''
@Author:风吹一夏
@Gender:man
@Hobby:coding
@Time:2020-5-11 16:56
'''
import requests,json
from pyquery import PyQuery
import pymysql
import re,json,time

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'cookie':'uuid=6d31c36c-8770-4f6c-915f-08a100927d07; antipas=539zV92801B35162a72466fX; cityDomain=xa; clueSourceCode=%2A%2300; user_city_id=176; ganji_uuid=7229646761454132794690; sessionid=ca1235f3-4fd4-463d-e293-3b27cf200591; lg=1; lng_lat=114.174328_22.316554; gps_type=1; close_finance_popup=2020-05-11; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A58163807989%7D; track_id=75632656174198784; preTime=%7B%22last%22%3A1589187430%2C%22this%22%3A1589184352%2C%22pre%22%3A1589184352%7D; guazitrackersessioncadata=%7B%22ca_kw%22%3A%22-%22%7D; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22pz_baidu%22%2C%22ca_n%22%3A%22pcbiaoti%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22%22%2C%22ca_campaign%22%3A%22%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22ca_transid%22%3A%22%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22track_id%22%3A%2275632656174198784%22%2C%22display_finance_flag%22%3A%22-%22%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%226d31c36c-8770-4f6c-915f-08a100927d07%22%2C%22sessionid%22%3A%22ca1235f3-4fd4-463d-e293-3b27cf200591%22%2C%22ca_city%22%3A%22xa%22%7D',

}
sum=0 #统计数据个数
for i in range(50):
    url = 'https://www.guazi.com/xa/buy/o%s/#bread'%str(i+1)
    print("正在获取第"+str(i+1)+"页")
    time.sleep(2)
    res = requests.get(url,headers=headers)
    # print(res.text)
    doc = PyQuery(res.text)
    ddlist = doc("ul.carlist li")#
    item={}

    for d in ddlist.items():
        data=d.text()
        dlist = ",".join(data.split(" "))
        # kw = ['急售准新车', '准新车', '急售']
        try:
            item['title'] = ",".join(data.split(" ")[:3])
            item['price'] = re.findall("(.*?)万", dlist)[1].replace("急售准新车","") + "万"
            item['orprice'] = re.findall("(.*?)万", dlist)[2].replace("急售准新车","").replace("准新车","").replace("急售","") + "万"
            kilm = re.findall("年\|(.*?)万公里", dlist)[0]
            item['mile']=str(kilm) + "万公里"
        except Exception as err:
            print("解析错误" + str(err))
        # print(data)
        print(item)
        sum+=1

        #存储到mysql数据库
        link = pymysql.connect(host="localhost",user="root",password="",database='guazi',charset='utf8')
        cursor = link.cursor()
        keys=",".join(item.keys())
        values=",".join(['%s']*len(item))
        sql='insert into cars(%s) values (%s)'%(keys,values)
        cursor.execute(sql,tuple(item.values()))
        link.commit()
        cursor.close()
        link.close()

print("共计获得：" + str(sum) + "条数据")