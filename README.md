PyHttpProxy
===========

这是一个简单的Http代理程序，类似于Paros

可以用来搭建一个Http代理服务器，用于监控Http请求。可以用来分析一些App的请求。

初衷是使用Paros的时候经常会不明卡死，所以自己实现了一个。


为了快速实现，使用了urllib2 这个更高级的库而不是httplib，因此需要手动处理一些高级的特性，比如：

1. 禁止自动3xx 跳转

2. chunked 传输编码的反解

暂时支持https，下面的更新会支持


依赖： wxpython
