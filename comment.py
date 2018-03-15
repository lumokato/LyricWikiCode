import os
import sys
import urllib
import re
import time
import types
import urllib.request


def savedoc(filepath, content):
    f = open(filepath, 'w')
    f.write(content)
    f.close()


def getHtml(url):
    # 获取网页信息
    hds = {'Cookie': 'os=pc; osver=Microsoft-Windows-8-Professional-build-9200-64bit; appver=1.5.0.75771;',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.138 Safari/537.36',
           'Referer': 'http://music.163.com/'}
    request = urllib.request.Request(url, headers=hds)
    page = urllib.request.urlopen(request)
    html = page.read()
    return html


def timestamp_datetime(value):
    format = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(int(value)/1000)
    ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt

def getRegex(regex, data):
    dat = re.compile(regex)
    ret = re.findall(dat, data)
    return ret



def getcomment(html):
    cmdata = []
    reg1 = r'"comments"(.+)"total"'
    line = getRegex(reg1, html.decode())
    reg2 = r'"user"(.*?)"isRemoveHotComment"'
    commentlines = getRegex(reg2, line[0])
    print(len(commentlines))
    for cmline in commentlines:
        nickname = getRegex(r'"nickname":"(.*?)"', cmline)[0]
        commentid = getRegex(r'"commentId":(.*?),', cmline)[0]
        time0 = timestamp_datetime(getRegex(r'"time":(.*?),', cmline)[0])
        content = getRegex(r'"content":"(.*?)"', cmline)
        cmdata.append([nickname, commentid, time0, content])
    with open('cm_sakura.csv', 'a', encoding='utf-8') as file:
        for cm in cmdata:
            file.write('%s,%s,%s,' % (cm[0], cm[1], cm[2]))
            for ct in cm[3][::-1]:
                file.write('%s,' % ct)
            file.write('\n')



for i in range(200):
    pages = 20*i
    print(pages)
    url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_26085473?limit=20&offset=' + str(pages)
    getcomment(getHtml(url))