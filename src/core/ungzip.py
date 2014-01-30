__author__ = 'ding'


import gzip
import StringIO
data = open('debug.txt').read()
data = StringIO.StringIO(data)
gz = gzip.GzipFile(fileobj=data)
data = gz.read()
gz.close()
print data.decode("gbk",'ignore')