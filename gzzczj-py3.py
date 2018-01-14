#!/usr/bin/python2.6
# coding=utf-8


import sys
import re
import chardet
import requests
import time
from bs4 import BeautifulSoup
import random


def freedown(username, passwd):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    req = requests.session()

    res = req.get('http://www.gzpi.gov.cn/vsgzhr/PHJG/评后结果中级2.html', headers=header)
    soup = BeautifulSoup(res.text.encode(res.encoding))
    # print res.encoding
    s = '广州'
    ss = s.encode('utf-8')  # .encode('cp936')
    # print soup
    login_list_text = []
    login_list_url = []
    for script_url in soup.find_all("a", attrs={"class": "08zyjsry_14"}):
        # print script_url.text
        # print s.decode('utf-8').encode('cp936')
        # print ss

        if s in script_url.text:
            login_list_text.append(script_url.text)
            url = script_url.attrs.get('onclick').split('\'')[1]
            if 'http' not in url:
                url = 'http://www.gzpi.gov.cn/vsgzhr/PHJG/' + url
            login_list_url.append(url)
            # print script_url.text

          #  print(url)

    #        else:
    #            print 'no'
    # print login_list_url[0]
    login_list_urls = []
    user_list = []
    login_list_urls.append(login_list_url[-1])
    for url in login_list_url:

        # if 'http' not in url:
        #    url = 'http://www.gzpi.gov.cn/vsgzhr/PHJG/' + url
        print(url)
        res_1 = req.get(url, headers=header)
        res_1.encoding = 'gb2312'
        # print chardet.detect(res_1.content)
        so = BeautifulSoup(res_1.text, fromEncoding="gb18030")
        # print so
        user = '杰赛'
        #suser = user.decode('utf-8')

        nd = '时间'
        #snd = nd.decode('utf-8')

        wyh = '评委会名称'
        #ewyh = wyh.decode('utf-8')

        # print suser
        n = 0
        #        print so.find_all('td')[1]
        for title in so.find_all('p'):
            if len(title.text) == 0 or len(title.text) > 50:
                continue
            if wyh in title.text:
                print(
                '****************************************************')
                print(
                title.text)
                # print n
                print(
                '****************************************************')

            if nd in title.text:
                print(
                '----------------')
                print(
                title.text)
                # print n
                print(
                '----------------')
        for td_url in so.find_all('td'):
            n = n + 1
            if len(td_url.text) == 0 or len(td_url.text) > 50:
                continue
            if wyh in td_url.text:
                print(
                '****************************************************')
                print(
                td_url.text)
                # print n
                print(
                '****************************************************')

            if nd in td_url.text:
                print(
                '----------------')
                print(
                td_url.text)
                # print n
                print(
                '----------------')
            elif user in td_url.text:

                if len(td_url.text) > 50 or len(td_url.text) == 0:
                    continue
                else:

                    # print len(td_url.text)
                    ''' '''
                    print(
                    td_url.text.strip() + ' | ' + so.find_all('td')[n].text.strip() + ' | ' + so.find_all('td')[
                        n + 1].text.strip())
                
                    # print so.find_all('td')[n].text
                    # print so.find_all('td')[n+1].text
                    print(
                    '----------------')
                    user_list.append(
                    td_url.text.strip() + ' | ' + so.find_all('td')[n].text.strip() + ' | ' + so.find_all('td')[
                        n + 1].text.strip())
        print(
        '=============================================================================')
    #print(user_list)
        # print script_url.attrs.get('onclick').split('\'')[1]
    # print login_list_text[1]
    # postdata = {'LoginForm[username]': username,
    #           'LoginForm[password]': passwd,
    #          '_csrf':csrf,
    #         'LoginForm[rememberMe]':'0',
    #        }
    # res_post = req.post('http://home.51cto.com/index',data=postdata)
    # so = BeautifulSoup(res_post.text.encode(html.encoding))
    # print so
    # login_list_url = []


# for script_url in so.find_all('script'):
#    login_list_url.append(script_url.attrs.get('src'))
# print login_list_url
# for url in login_list_url[:-2]:
#    r = req.get(url)
#    print r.text
#    down_url = 'http://down.51cto.com/download.php'
#   down_data = {'do':'getfreecredits','t':random.random()}
#  down_res = req.post(down_url,params=down_data,data=down_data)
# print down_res.text
# down_url = 'http://home.51cto.com/home/ajax-to-sign'
# down_data = {'DNT':'1'}
# down_res = req.post(down_url,params=down_data,data=down_data)
# print down_res.text
if __name__ == "__main__":
    #    t=random.randint(60,600 )
    #    time.sleep( t )
    freedown('hmilyfe', '6014256')
