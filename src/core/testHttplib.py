__author__ = 'ding'

import httplib
conn = httplib.HTTPConnection("www.baidu.com")
conn.request("GET","/ind")
res = conn.getresponse()
print res.status, res.reason
print dir(res)
print res.chunked
data = res.read()
print len(data)