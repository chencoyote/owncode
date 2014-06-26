#!/usr/bin/env python
#-*- coding:utf-8 -*-
from urllib import urlencode
import urllib2
import cookielib
import re

cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36"
    }
formdata = urlencode({
    "loginfield":"username",
    'continueURI':'http://www.anying.org/forum-2-1.html',
    "questionid":0,
    'loginsubmit':'True'
    })
req = urllib2.Request(
        url = "http://anying.org/member.php?mod=logging&action=login",
        data = formdata,
        headers = headers
        )
resault = urllib2.urlopen(req)
req = urllib2.Request(
        url = "http://www.anying.org/forum-2-1.html"
        )
resault = urllib2.urlopen(req).read()
res = re.findall(r"<a.*?>.*?</a>",resault)
f = open("anyherf.html","w")
for i in res:
    f.write(i.decode("gbk").encode("utf8")+"\r\n")
f.close()
