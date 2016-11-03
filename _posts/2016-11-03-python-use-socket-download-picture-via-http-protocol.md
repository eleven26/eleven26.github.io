---
published: true
title: Python使用socket下载图片(使用http协议)
layout: post
category: Python
---
　　本文的目的并不是真的让大家学习用socket去下载东西，这样做的意义(造轮子)其实不大，毕竟这些东西前辈们已经做过了，下面会说到。

　　下面是一个无比繁杂的例子，还没去优化，特别的低效，因为以行的方式遍历了整个二进制格式图片文件，事实上应该有更好的方法，想到了应该怎么做，但是还不知道用python应该怎么实现，http协议报文格式一个比较显著的特征是: 请求头(响应头)-**空行**-请求实体(响应)，一般情况下我们需要的信息其实只是实体部分。

　　当我们通过socket连接上某个网站，并请求了图片资源之后，socket接收到的只是字节流，响应的实体部分就是我们的图片了，我们要做的是把http响应实体从http报文中分离出来保存到文件中。(注意: 不要把接收到的所有信息全部保存到文件中，那样做系统识别不了其中包含的图片)

download_picture.py
{% highlight python %}
import socket

HOST = 'localhost'
PORT = 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT)) # 通过socket与服务器连接

# http请求头，下载服务器上uri为'/test.jpg'的图片
http_request = """
GET /test.jpg HTTP/1.1
Host: localhost

"""
# 发送http请求，把响应先保存在test.jpg中，这个test.jpg并不是正确的图片格式，里面还包含有http响应头，如果不做转换是没法打开的
s.sendall(http_request)
f = open('test.jpg', 'wb')
try:
    while True:
        http_response = s.recv(9192)
        if not http_response:
            f.close()
            break
        f.write(http_response)
except socket.error:
    print socket.error.message
finally:
    f.close()

# 把实际下载的图片保存在new.jpg中
jpg = open('test.jpg', 'rb')
new = open('new.jpg', 'wb')

flag = 0
for line in jpg.readlines():
    if flag == 0:
        print line,
    # 空行是区分http响应头和响应实体的标志，因为http头是不能有空行的
    if line == '\r\n' or line == '\n' or line == '\r':
        flag = 1
        continue
    if flag == 1:
        new.write(line)

# 下载完成后关闭文件资源
jpg.close()
new.close()
{% endhighlight %}


　　上面的例子做了很繁琐的处理，实际上这类工作在Python已经有非常成熟的第三方库了，如urllib2:
{% highlight Python%}
import urllib2

http_response = urllib2.urlopen('http://localhost/test.jpg')
f = open('download.jpg', 'wb')
f.write(http_response.read())
f.close()
{% endhighlight%}
　　这里用几行就实现了下载的功能，虽然看起来是只有几行，实际上urllib2已经帮我们做了所有的重复性工作。

　　summary: 写本文只是了解一下http协议报文格式。
