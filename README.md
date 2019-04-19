# DynamicProxyServer

本程序可动态获取代理IP地址，浏览器或其他终端每次请求都进行换一代理IP地址进行请求内容。


# 地址池安装参照原作者

https://github.com/jhao104/proxy_pool

# 修改代理池地址

修改文件autoProxyServer.py中的proxy_pool_url为安装地址池的访问地址


# 修改本地端口

可根据个人需要，修改相应的端口号作为程序的监听端口，修改文件autoProxyServer.py中，将以下监听端口12345修改成自己所要的端口：
Proxy(addr=('0.0.0.0', 12345),proxy_pool_url=proxy_pool_url).serve_forever()


# 程序运行

修改autoProxyServer.py后，直接运行该文件。



