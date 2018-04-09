# -*- coding: utf-8 -*-
import sys
import os
import json
import requests
import pygame
import demjson
import time
from recorder import recorder
import snowboy
from tts import baidu_tts
from stt import baidu_stt


def get_intent(text):
        ak = 'cd3c2238c7348d28363a1aad0b93d474'
        url = 'https://ai.aixxz.com'
        path = '/api?'

        data = {
                "city" = "中山"
                "nickname" = "tb"
                "text" = text
                "user" = "123456"
               }
        r = requests.post(url + path + data,
                          headers={'Authorization', 'APPCODE ' + appcode})
        json = r.json()
        domian = json['intent']
        return domain
        
        
def do_intent(text): #自制的语义理解系统,欢迎大家补充
        if '闹钟' in text:
                intent = 'clock'
                return intent
        elif '打开' in text:
                intent = 'smarthome'
                return intent
        elif '翻译' in text:
                intent = 'ts'
                return intent
        elif '搜索' in text:
                intent = 'ser'
                return intent
        elif '闲聊' in text:
                intent = 'tuling'
                return intent
        elif '关机' in text:
                print ('SHUTDOWING...')
                os.system('sudo poweroff')
        elif '重启' in text:
                print ('REBOOTING...')
                os.system('sudo reboot')
        elif '怎么走' in text:
                intent = 'map'
                return intent
        elif '酒店' in text:
                intent = 'hotel'
                return intent
        elif '旅游' in text:
                intent = 'travel'
                return intent
        elif '做游戏' in text:
                intent = 'minigame'
                return intent
        elif '新闻' in text:
                intent = 'news'
                return intent
        elif '傻逼' in text:
                speaker.falu()
        else:
                intent = 'tuling'
                return intent