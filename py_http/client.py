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
    data = send_file.read(3072000)
    if not data:
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
