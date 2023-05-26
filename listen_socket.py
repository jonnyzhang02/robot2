'''
Author: jonnyzhang02 71881972+jonnyzhang02@users.noreply.github.com
Date: 202-05-19 16:12:51
LastEditors: jonnyzhang02 71881972+jonnyzhang02@users.noreply.github.com
LastEditTime: 2023-05-26 13:39:43
FilePath: /robot2/listen_socket.py
Description: coded by ZhangYang@BUPT, my email is zhangynag0207@bupt.edu.cn

Copyright (c) 2023 by zhangyang0207@bupt.edu.cn, All Rights Reserved. 
'''
import socket
import openai

# 在笔记本上运行，用于接收roban的socket并获得chatgpt回复
def get_chatgpt_respond(prompt):

    openai.proxy = "socks5h://127.0.0.1:20081"
    openai.api_key = ""

    model_engine = "gpt-3.5-turbo"

    completion = openai.ChatCompletion.create(
    model=model_engine, 
    messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content


# 创建 socket 对象
serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM) 

# 获取本地主机名
host = '192.168.3.17'

port = 20002

# 绑定端口
serversocket.bind((host, port))

# 设置最大连接数，超过后排队
serversocket.listen(5) 

while True:
    # 建立客户端连接
    clientsocket, addr = serversocket.accept()      

    print("连接地址: %s" % str(addr))
    
    msg = 'socket连接已经建立！' + "\r\n"
    clientsocket.send(msg.encode('utf-8'))
    
    while True:
        data = clientsocket.recv(1024).decode('utf-8')
        if data == 'q':
            break
        print("客户端发来消息： ", data)
        respond = get_chatgpt_respond(data)
        print("chatGPT回复： ", respond)
        clientsocket.send(respond.encode('utf-8'))
    
    clientsocket.close()



