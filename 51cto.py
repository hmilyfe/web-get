#!/usr/bin/python2.6
#coding=utf-8
#51cto自动领豆 by 2016-07-27
import requests
import time
from bs4 import BeautifulSoup
import random
def freedown(username,passwd):
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1','Referer':'http://home.51cto.com/index'}
    req = requests.session()
    res = req.get('http://home.51cto.com/index',headers=header)
    soup = BeautifulSoup(res.text)
    csrf = soup.find('input').attrs.get('value')
    postdata = {'LoginForm[username]': username,
                'LoginForm[password]': passwd,
                '_csrf':csrf,
                'LoginForm[rememberMe]':'0',
                }
    res_post = req.post('http://home.51cto.com/index',data=postdata)
    so = BeautifulSoup(res_post.text)
    print so
    login_list_url = []
    for script_url in so.find_all('script'):
        login_list_url.append(script_url.attrs.get('src'))
    print login_list_url
    for url in login_list_url[:-2]:
        r = req.get(url)
        print r.text
#    down_url = 'http://down.51cto.com/download.php'
 #   down_data = {'do':'getfreecredits','t':random.random()}
  #  down_res = req.post(down_url,params=down_data,data=down_data)
   # print down_res.text
    #down_url = 'http://home.51cto.com/home/ajax-to-sign'
    #down_data = {'DNT':'1'}
    #down_res = req.post(down_url,params=down_data,data=down_data)
    #print down_res.text
if __name__ == "__main__":
#    t=random.randint(60,600 )
#    time.sleep( t )
    freedown('hmilyfe','6014256')
