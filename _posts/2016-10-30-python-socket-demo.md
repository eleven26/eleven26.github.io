---
published: true
title: 2016-10-30-python-socket-传输文件-demo.md
layout: post
---
demo中的客户端和服务端脚本在同一文件夹

服务端 server.py
```python
#!/usr/bin/env python

import datetime
import time
start = time.mktime(datetime.datetime.now().timetuple())

import socket

host = '127.0.0.1'
port = 9090
file_name = 'destination.iso'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)

conn, addr = s.accept()
print "connected"
save_file = open(file_name, 'wb')
while True:
    data = conn.recv(4096000)
    if len(data) == 0:
        break
    save_file.write(data)

print "finish receive!"
conn.close()
save_file.close()

end = time.mktime(datetime.datetime.now().timetuple())
run_time = end - start

minute = run_time / 60
second = run_time - minute * 60

print "run time: %s second" % run_time
if minute < 1:
    print "run time: %s" % second
else:
    print "run time: %sm%ss" % (minute, second)
```

客户端client.py
```python
#!/usr/bin/env python

import datetime
import time
start = time.mktime(datetime.datetime.now().timetuple())

import socket
host = "127.0.0.1"
port = 9090
file_name = 'source.iso'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
print "connected"

send_file = open(file_name, 'rb')
while True:
    data = send_file.read(4096000)
    if len(data) == 0:
        break
    s.sendall(data)

print "finish send!"
s.close()
send_file.close()

end = time.mktime(datetime.datetime.now().timetuple())
run_time = end - start

minute = run_time / 60
second = run_time - minute * 60

print "run time: %s second" % run_time
if minute < 1:
    print "run time: %s" % second
else:
    print "run time: %sm%ss" % (minute, second)
```

>测试传输的文件大小为3.8G 

>data = send_file.read(4096000)
这里每次读取大小和服务端每次写多少依据具体情况而定，测试时候发现cpu占用略高，i5-6500 3.4GHz服务器端和客户端各占了10%左右，
当send_file.read()中参数为4096的时候，占用总共为30%左右。
