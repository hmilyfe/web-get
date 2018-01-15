#!/usr/bin/python3
# coding=utf-8

import sys
import difflib
import chardet
import requests
import time
from bs4 import BeautifulSoup
import filecmp
import getopt
import os
import json
import jsonpath
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def get_result() :
    filename = 'd:\\test\\monitor.txt'
    m_list = []
    #m1= {'url':url_value, 'method':method_value, 'word':word_value, 'post-data':data_value}
    with open(filename, 'r') as f:
        for line in f.readlines():
            m_list.append(line)
            #print(eval(line)['url'])
    f.close()
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
             }
    for i in m_list :
        payload_value = eval(i)['post-data']
        method_value = eval(i)['method']
        url_value = eval(i)['url']
        word_value = eval(i)['word']
        response = requests.request(method_value, url_value, data=payload_value, headers=headers)

        if response.text :
            if method_value == 'post':
                value = json.loads(response.text)
                w = word_value.split(':')
                #print(w[0])
                result = []
                title_list = jsonpath.jsonpath(value , '$..'+ w[0] )
            else :
                so = BeautifulSoup(response.text.encode(response.encoding), "html.parser")
                for title in so.find_all(w[0]):
                    if w[1] in title :
                        if len(title.text) == 0 or len(title.text) > 50:
                            continue
                        else  :
                            result.append(title.text.strip())
            #print(title_list)
            if title_list and len(w) > 1 :
                for t in title_list :
                    #print(type(t))
                    if w[1] in t :
                        result.append(t)
            #print(result)
            result_txt = 'd:\\test\\' +  url_value.split('/')[2] + '.txt'
            if os.path.exists(result_txt) :
                result_file =  'd:\\test\\'+ url_value.split('/')[2]+  '-new.txt'

            else :
                result_file = result_txt
            with open(result_file, 'w') as f:
                for line in result:
                    f.write(line)
                    f.write('\r\n')
                    # print(eval(line)['url'])
            f.close()
            flag = filecmp.cmp(result_txt, result_file)
            #print(flag)
        if  not flag :
            a = open(result_txt,'U').readlines()
            b = open(result_file,'U').readlines()
            diff = difflib.ndiff(a, b)
            mail_body = ''.join(diff)
            print(mail_body)
            from_addr = 'jimin-q@gcidesign.com'
            password = '1a2b3c'
            to_addr = 'hmilyfe@vip.qq.com'
            smtp_server = 'smtp.263.net'

            msg = MIMEText("您监控的网站:" + url_value.split('/')[2] + "  有变动!\n"+r''+ mail_body ,'plain','utf-8')
            msg['From'] =  _format_addr('网站监控<%s>' % from_addr)
            msg['To'] =  _format_addr('管理员 <%s>' % to_addr)
            msg['Subject'] = Header(u'网页变动：'+url_value.split('/')[2],'utf-8').encode()
            server = smtplib.SMTP(smtp_server, 25)
            #server.set_debuglevel(1)
            server.login(from_addr, password)
            server.sendmail(from_addr, [to_addr], msg.as_string())
            server.quit()
        else :
            print ('same')
           # print('==============================')
    #print(response.text)

    #for req_url in req_urls :#print(req_url)
    #    if method_value == 'get' :
     #       res = req.get(req_url, headers=header)
    #    else:
    #        res = req.post(req_url,data_value)
    #    soup = BeautifulSoup(res.text.encode(res.encoding), "html.parser")
    #    value = json.loads(res.content)



        # print soup
    '''    login_list_text = []
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
'''
def help():
    print('usage： python ', sys.argv[0] ,'-m [get | post] -u [http://] -d [需要post的data] -w [需要检测的字符]')
    '''print("default: " ,     method_value ,
    psnd_value ,\
    jb_value  ,\
    lb_value ,\
    comp_value )
'''
    sys.exit()
def filecomp():
    return
if __name__ == "__main__":
    #def get_result(u='ALL', psnd='ALL', jb='ALL', lb='电子电气',comp='杰赛')
    #get_result(u='杨洁燕',lb='教',comp='汇侨')
    opts, args = getopt.getopt(sys.argv[1:], 'm:u:w:d:h', ["method=", "url=", "word=","data=",'help'])
    method_value = 'get'
    url_value = ''
    word_value = ''
    data_value = ''

    for opt, value in opts:
        if opt in ("-m", "--method"):
            method_value = value
            # 如果有传参，则重新赋值。
        if opt in ("-u", "--url"):
            url_value = value
        if opt in ("-w", "--word"):
            word_value = value
        if opt in ("-d", "--data"):
            data_value = value
            '''  if opt in ("-c", "--comp"):
         comp_value = value
         '''
        if opt in ("-h", "--help"):
            help()
    #get_result(method_value,url_value,word_value,data_value)
    get_result()

