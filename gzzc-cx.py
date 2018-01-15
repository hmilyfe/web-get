#!/usr/bin/python3
# coding=utf-8

import sys
import re
import chardet
import requests
import time
from bs4 import BeautifulSoup
import random
import getopt
import os

def get_result(u='ALL',psnd='ALL',jb='ALL',lb= '电子电气',comp='杰赛'):
#    print(u)
#    print(psnd)
#    print(jb)
#    print(lb)
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    req = requests.session()
    req_urls = []
    filename = comp + ".txt"
    fp = open(filename, 'w+')
    if jb == 'ALL' :
        req_urls.append('http://www.gzpi.gov.cn/vsgzhr/PHJG/评后结果中级2.html')
        req_urls.append('http://www.gzpi.gov.cn/vsgzhr/PHJG/评后结果高级2.html')
    else:
        req_urls.append('http://www.gzpi.gov.cn/vsgzhr/PHJG/评后结果' + jb + '2.html')
    for req_url in req_urls :#print(req_url)
        res = req.get(req_url, headers=header)
        soup = BeautifulSoup(res.text.encode(res.encoding), "html.parser")
        # print res.encoding

        # ss = s.decode('utf-8')#.encode('cp936')
        # print soup
        login_list_text = []
        login_list_url = []
        result = []
        for script_url in soup.find_all("a", attrs={"class": "08zyjsry_14"}):
            # print script_url.text
            # print s.decode('utf-8').encode('cp936')
            # print ss
            if lb == 'ALL' :
                login_list_text.append(script_url.text)
            elif lb in script_url.text :
                login_list_text.append(script_url.text)
                url = script_url.attrs.get('onclick').split('\'')[1]
                if 'http' not in url:
                    url = 'http://www.gzpi.gov.cn/vsgzhr/PHJG/' + url
                login_list_url.append(url)
                # print script_url.text

                # print url

        #        else:
        #            print 'no'
       # print (login_list_url[0])
        login_list_urls = []
        login_list_urls.append(login_list_url[-2])
        for url in login_list_url:
            titles = []
            times = []
            users = []
            # if 'http' not in url:
            #    url = 'http://www.gzpi.gov.cn/vsgzhr/PHJG/' + url
            # print url
            res_1 = req.get(url, headers=header)
            res_1.encoding = 'GB18030'
            # print chardet.detect(res_1.content)
            # so = BeautifulSoup(res_1.text,fromEncoding="gb18030")
            so = BeautifulSoup(res_1.text.encode('utf-8'), "html.parser")
            #print (so)
            user = comp
            # suser = user.decode('utf-8')

            nd = '时间'
            # snd = nd.decode('utf-8')

            wyh = '评委会名称'
            # ewyh = wyh.decode('utf-8')

            # print (user)
            user_list = []
            n = 0
            #        print so.find_all('td')[1]
            for title in so.find_all('p'):
                #print (title.text)
                if len(title.text) == 0 or len(title.text) > 50:
                    continue
                if wyh in title.text:
                    # print '****************************************************'

                    titles.append(title.text)
                    # print n
                    # print '****************************************************'
                if nd in title.text  :
                    # print '----------------'
                    # print title.text
                    if psnd == 'ALL':
                        times.append(title.text)
                    elif psnd in title.text :
                        times.append(title.text)
                    # print n
                    # print '----------------'
            for td_url in so.find_all('td'):
                n = n + 1

                #print (td_url.text)
                if len(td_url.text) == 0 or len(td_url.text) > 50:
                    continue
                if wyh in td_url.text:
                    # print '****************************************************'
                    #print (td_url.text.strip())
                    titles.append(td_url.text.strip())
                    # print n
                    # print '****************************************************'

                if nd in td_url.text:
                    # print '----------------'
                    # rq = td_url.text.encode('GB18030')[0:22]
                    # if '08' in rq :
                    #   rq = td_url.text.encode('GB18030')[0:20]
                    #  print rq
                    # else:
                    # print td_url.text.encode('utf-8')
                    # print '----------------'
                    # print title.text

                    if psnd == 'ALL':
                        times.append(td_url.text)
                        #print(td_url.text)
                    elif psnd in td_url.text:
                        #print(td_url.text)
                        times.append(td_url.text)

                # print n
                # print '----------------'
                elif user in td_url.text :

                    if len(td_url.text) > 50 or len(td_url.text) == 0:
                        continue
                    else:
                        #print(u)
                        # print len(td_url.text)
                        # user_all = td_url.text.strip().encode('utf-8') + ' | ' + so.find_all('td')[n].text.strip().encode('utf-8') + ' | ' + \
                        #so.find_all('td')[n + 1].text.strip()[0:1].encode('utf-8')   replace(' ','')
                        u1 = so.find_all('td')[n].text.replace(' ','').split()
                        u2 = u1[0]
                        if u1[0] != u1[-1] :
                            u2 = u2 + u1[1]
                        xb =  so.find_all('td')[n + 1].text.strip()
                        user_all = td_url.text.strip() + ' | ' + u2  + ' | ' + xb

                        if u == 'ALL' :
                            users.append(user_all)
                        elif u in u2:
                            #print(u)
                            users.append(user_all)
                        # print so.find_all('td')[n].text
                        # print so.find_all('td')[n+1].text
                        # print '----------------'
            # print '============================================================================='
            #os.mknod("d:\myifles\test.txt")

            #创建空文件

            #直接打开一个文件，如果文件不存在则创建文件
            if  len(users) > 0 and len(times) > 0 and len(titles) > 0 :
                filename = comp + ".txt"
                fp = open(filename, 'a+')
                fp.write(url+'\n')
                fp.write(titles[0]+'\n')
                #fp.write(times[0].encode('utf-8'))
                for x in users :
                    fp.write(x+'\n')
                fp.close()

                print(url)
                print(titles[0])
                print(times[0])
                print('人数:', len(users))
                for x in users:
                    print(x)
                print('=============================================================================')





def help():
    print('usage： python ', sys.argv[0] ,'-u 用户名 -p 评审年度 -j 级别 -l 类别 -c 公司名')
    print("default:    username_value = 'ALL'\
    psnd_value = 'ALL'\
    jb_value = 'ALL'\
    lb_value = '电子电气'\
    comp_value = '杰赛'")
    print("optinos:    username_value = '杨洁燕'\
    psnd_value = '2015'\
    jb_value = 中级'\
    lb_value = '教师'\
    comp_value = '汇侨中学'")
    sys.exit()

if __name__ == "__main__":
    #def get_result(u='ALL', psnd='ALL', jb='ALL', lb='电子电气',comp='杰赛')
    #get_result(u='杨洁燕',lb='教',comp='汇侨')
    opts, args = getopt.getopt(sys.argv[1:], 'u:p:j:l:c:h', ["username=", "psnd=", "jb=", "lb=", "comp=",'help'])
    username_value = 'ALL'
    psnd_value = 'ALL'
    jb_value = 'ALL'
    lb_value = '电子电气'
    comp_value = '杰赛'
    for opt, value in opts:
        if opt in ("-u", "--username"):
            username_value = value
            # 如果有传参，则重新赋值。
        if opt in ("-p", "--psnd"):
            psnd_value = value
        if opt in ("-j", "--jb"):
            jb_value = value
        if opt in ("-l", "--lb"):
            lb_value = value
        if opt in ("-c", "--comp"):
            comp_value = value
        if opt in ("-h", "--help"):
            help()
    get_result(username_value,psnd_value,jb_value,lb_value,comp_value)

