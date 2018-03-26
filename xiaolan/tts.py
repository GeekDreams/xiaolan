# -*- coding: utf-8 -*-
# 百度TTS
import sys
import os
import logging
import requests
import wave
import xlpath
import json
import pyaudio
import time
import tempfile
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class baidu_tts(object):
    def __init__(self, stext, say, token, turl, AK, SK, url, per):
        self.stext = saytext
        self.say = say
        self.token = '24.b889fe13015f30355edcdd5343fc2ee9.2592000.1523371315.282335-10747354'
        self.turl = 'http://openapi.baidu.com/oauth/2.0/token'
        self.url = 'http://tsn.baidu.com/text2audio'
        self.AK = 'M9jz0511Yfbb15d1BshqtC5g'
        self.SK = 'Z73I2jvytEa8QydGnNlP3oOKfudIlvgE'
        self.per = '4'
        
    def get_token(self):
        try:
            pms = cache.readlines()
            if len(pms) > 0:
                time = pms[0]
                token = pms[1]
                time = dparser.parse(time)
                endtime = datetime.datetime.now()
                if (endtime - time).days <= 29:
                    return token
        finally:
            cache.close()
        URL = 'http://openapi.baidu.com/oauth/2.0/token'
        params = urllib.urlencode({'grant_type': 'client_credentials',
                                   'client_id': self.AK,
                                   'client_secret': self.SK})
        r = requests.get(URL, params=params)
        try:
            r.raise_for_status()
            token = r.json()['access_token']
            return token
        except requests.exceptions.HTTPError:
            self._logger.critical('Token request failed with response: %r',
                                  r.text,
                                  exc_info=True)
          
        
    def tts(self):
        if self.token == '':
            self.token = self.get_token()
        punctuations = ['.', '。', ';', '；', '\n']
        if self.token == '':
            self.token = self.get_token()
        query = {'tex': self.stext,
                 'lan': 'zh',
                 'tok': self.token,
                 'ctp': 1,
                 'cuid': str(get_mac())[:32],
                 'per': self.per
                 }
        r = requests.post('http://tsn.baidu.com/text2audio',
                          data=query,
                          headers={'content-type': 'application/json'})    
        try:
            r.raise_for_status()
            if r.json()['err_msg'] is not None:
                print ('Baidu TTS failed with response: %r',
                                      r.json()['err_msg'])
                return None
        except Exception:
            pass
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(r.content)
            say = f.name
            return say