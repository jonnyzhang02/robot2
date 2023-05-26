'''
Author: jonnyzhang02 71881972+jonnyzhang02@users.noreply.github.com
Date: 2023-05-19 14:54:52
LastEditors: jonnyzhang02 71881972+jonnyzhang02@users.noreply.github.com
LastEditTime: 2023-05-26 13:41:44
FilePath: /robot2/185.py
Description: coded by ZhangYang@BUPT, my email is zhangynag0207@bupt.edu.cn

Copyright (c) 2023 by zhangyang0207@bupt.edu.cn, All Rights Reserved. 
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import String         # 导入消息类型
from ros_AIUI_node.srv import textToSpeakMultipleOptions
import socket

class S2T():
    def __init__(self):
        my_museum=museum()
        rospy.Subscriber("/aiui/nlp", String, my_museum.voice_guide)
        rospy.spin()                    # 控制 ROS 系统中的消息循环

    def nlp_callback(self, msg):
        rospy.loginfo(msg.data)         # 用 ros 的 log 输出结果

class T2S():
    def __init__(self):
        self.tts_param = {              # 定义待转文字及合成的参数
            'text': '你好，我是鲁班',
            'vcn': 'qige',
            'speed': 50,
            'pitch': 5,
            'volume': 20
        }

    def tts(self,text):
        self.tts_param["text"]=text
        rospy.wait_for_service("/aiui/text_to_speak_multiple_options", timeout=2)   # 等待服务可用。超时时间这里设置为 2s，默认会一直等待，超时会抛出 rospy.ROSException 异常
        tts_client = rospy.ServiceProxy("/aiui/text_to_speak_multiple_options", textToSpeakMultipleOptions)     # 创建 ros 服务客户端
        tts_client(self.tts_param['text'], self.tts_param['vcn'], self.tts_param['speed'], self.tts_param['pitch'], self.tts_param['volume'])       # 客户端发起请求，参数与该服务的类型定义一一对应

class museum():
    def __init__(self):
        # 0:待选择 1:导览和导游 2:chatGPT
        self.mode=0 

        # 解说词
        self.t1="第一件是《星夜》。梵高的经典之作，这幅画充满了梦幻般的色彩和运动感，描绘了一个星空下的风景，令人陶醉其中。"
        self.t2="第二件是《蓝色时期》。毕加索的代表作之一，这幅画以蓝色调为主，表达了艺术家内心深处的孤独和忧伤。"
        self.t3="第三件是《蒙克的呐喊》。爱德华·蒙克的标志性作品，表现了一个扭曲而恐怖的人物尖叫的场景，彰显了内心的痛苦和绝望"
        
        # 用于和chatGPT交互，初始化socket，连接到我的笔记本电脑
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_socket()
    
    def voice_guide(self,msg):
        # 接收数据
        rospy.loginfo("我听到你说:{}".format(msg.data))
        text=msg.data

        if self.mode==0:
            # 待选择模式
            if "智能" in text:
                # 进入chatGPT模式
                self.mode=2
                reply="好的，正在接入"

            elif "导览" not in text and "导游"not in text:
                # 未识别到导览和导游
                reply="抱歉，我不太理解，请再说一次"

            else:
                # 进入导览模式
                reply="好的，欢迎来到2020212185的展馆，这里有三幅精选艺术作品：《星夜》、《蓝色时期》和《蒙克的呐喊》。我们从哪个展品开始？"
                self.mode=1

        elif self.mode==1:
            # 导览模式
            reply="好的，我们开始导览，"
            s1=self.t1
            s2=self.t2
            s3=self.t3

            order=[] # 讲解顺序
            if "1" in text or "一"in text or "星夜" in text:
                order=[s1,s2,s3]
            elif "2" in text or "二"in text or "蓝色时期" in text:
                order=[s2,s1,s3]
            elif "3" in text or "三"in text or "蒙克的呐喊" in text:
                order=[s3,s1,s2]
            else:
                order=[s1,s2,s3] 

            for stuff in order:
                reply=reply+stuff

            reply=reply+",好的，导览完成，谢谢"
            self.mode=0

        else:
            # chatGPT模式
            reply=self.intell_reply(text)
            rospy.loginfo("GPT已回复！")
        
        t2s = T2S()
        t2s.tts(reply)
        rospy.loginfo(reply)

    def connect_socket(self):
        # 创建 socket 对象
        host = '192.168.3.17'
        port = 20055
        # 连接服务，指定主机和端口
        self.sock.connect((host, port))

        # 检测socket连接
        info=self.sock.recv(1024).decode('utf-8')
        rospy.loginfo(info)

    def intell_reply(self,text):
        # 发送数据
        self.sock.send(text.encode('utf-8'))
        # 接收数据
        gpt_reply=self.sock.recv(1024).decode('utf-8')
        
        return gpt_reply


if __name__ == '__main__':
    rospy.init_node("speak_to_text")
    s2t = S2T()
