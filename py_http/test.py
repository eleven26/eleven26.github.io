import socket

HOST = 'localhost'
PORT = 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

http_request = """
GET /test.jpg HTTP/1.1
Host: localhost

"""

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

jpg = open('test.jpg', 'rb')
new = open('new.jpg', 'wb')

flag = 0
for line in jpg.readlines():
    if flag == 0:
        print line,
    if line == '\r\n' or line == '\n' or line == '\r':
        flag = 1
        continue
    if flag == 1:
        new.write(line)

jpg.close()
new.close()
