# coding=utf-8
# author: Lan_zhijiang
# description: File Player
# date: 2020/10/1

import os


def ding(): #开始录制指令提示音
        os.system('mplayer /home/pi/old_xiaolan/old_xiaolan/musiclib/ding.wav')


def dong(): #结束录制指令提示音
    
    os.system('mplayer /home/pi/old_xiaolan/old_xiaolan/musiclib/dong.wav')


def poweroff(): #关机提示音（太懒，mp3文件还没弄）
    
    os.system('omxplayer /home/pi/old_xiaolan/musiclib/old_xiaolan/poweroff.mp3')


def kacha(): #拍照声
    
    os.system('mplayer /home/pi/old_xiaolan/old_xiaolan/musiclib/kacha.mp3')


def speak(): #说出的回话
    
    os.system('mplayer /home/pi/old_xiaolan/old_xiaolan/musiclib/say.mp3')


def play(song_name): #音乐播放器
    
    print '正在播放:' + song_name
    os.system('omxplayer /home/pi/old_xiaolan/old_xiaolan/musiclib/music.mp3')


def speacilrecorder():

    os.system('mplayer /home/pi/old_xiaolan/old_xiaolan/musiclib/speacilrecorder.mp3')
