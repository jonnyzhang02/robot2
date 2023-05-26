import socket
import time

# 用于测试socket连接是否通畅
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 创建 socket 对象
host = '192.168.163.1'
port = 20055
# 连接服务，指定主机和端口
sock.connect((host, port))

# 检测socket连接
info=sock.recv(1024).decode('utf-8')

while True:
    text = "hello world"
    # 发送数据
    sock.send(text.encode('utf-8'))
    # 接收数据
    gpt_reply=sock.recv(1024).decode('utf-8')

    time.sleep(10)
