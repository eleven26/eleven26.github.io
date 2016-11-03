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
    data = conn.recv(3072000)
    if not data:
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
