# -*- coding: utf-8 -*-
''' 智能家居技能（尚未完善，大家一起加油，用函数哦)  '''
import json
import sys
import os
import requests
import time
sys.path.append('/home/pi/xiaolan/xiaolan/')
from stt import baidu_stt
from tts import baidu_tts
from recorder import recorder
import speaker

def start(tok):
	
	h = hass()
	h.start(tok)

class hass(object):
	def __init__(self):
		
		pass
	
	def start(self, tok): #判断
		 
		bt = baidu_tts()
		bs = baidu_stt(1, 2, 3, 4)
		r = recorder()
		h = hass()
		welcome = '欢迎使用小蓝专用智能家居控制系统！请在，滴，一声之后说出指令'
		
		bt.tts(welcome, tok)
		speaker.speak()
		speaker.ding()
		r.record()
		speaker.dong()
		text = bs.stt('./voice.wav', tok)
		
		while text == None:
			sorry = '对不起，我没有听清楚，请重复一遍'
			bt.tts(sorry, tok)
			speaker.speak()
			speaker.ding()
			r.record()
			speaker.speak()
			text = bs.stt('./voice.wav', tok)
			if text != None:
				break
		texts = str.encode(encoding='UTF-8',errors='strict')
		if '打开' in text:
			cortolthings = texts[6:-2]
			cortolmode = 'turn_on'
			h.cortol(cortolthings, cortolmode, tok)
		elif '关闭' in text:
			cortolthings = texts[6:-2]
			cortolmode = 'turn_off'
			h.cortol(cortolthings, cortolmode, tok)
		elif '查看' in text:
			if '传感器' in text:
				getstatethings = texts[6:-5]
				getmode = 'sensor'
				h.sensor(getstatethings, tok)
		if '红外' in text:
			if '学习' in text:
				h.study(tok)

		else:
			h.usuallycortol(text, tok)
	
	def chosecolor(self, text):
	
		if '红色' in text:
			c = 'red'
			return c
		elif '黄色' in text:
			c = 'yellow'
			return c
		elif '橙色' in text:
			c = 'orange'
			return c
		elif '绿色' in text:
			c = 'green'
			return c
		elif '蓝色' in text:
			c = 'blue'
			return c
		elif '紫色' in text:
			c = 'purple'
			return c
		elif '白色' in text:
			c = 'white'
			return c
		else:
			c = 'a'
			return c
	
	def service(self): #获取各个领域的服务
		
		url = 'http://hassio.local'
		port = '8123'
		passwd = 'y20050801'
		service = '/api/services'
		headers = {'x-ha-access': passwd,
          		   'content-type': 'application/json'}
		
		r = requests.get(url + ':' + port + service,
				 headers=headers)
		
		json = r.json()
		domains = {}
		
		try:
			for jsons in json:
				domain = jsons['domain']
				services = jsons['services']
				domains[domain] = services
		except KeyError:
			return domains
		else:
			return domains
				 
	
	def e_id(self):
		
		url = 'http://hassio.local'
		port = '8123'
		passwd = 'y20050801'
		service = '/api/states'
		headers = {'x-ha-access': passwd,
          		   'content-type': 'application/json'}
		
		r = requests.get(url + ':' + port + service,
				 headers=headers)
		
		r_json = r.json()
		e_id = {}
		friendly_name_e = unicode('friendly_name', "utf-8", "ignore")
		attributes_e = unicode('attributes', "utf-8", "ignore")
		try:
                    for r_jsons in r_json:
                        entity_id = r_jsons['entity_id']
                        friendly_name = r_jsons['attributes']['friendly_name']
                        domain = entity_id.split(".")[0]
                        e_id[friendly_name] = entity_id
                except KeyError:
                    return e_id
		else:
		    return e_id
			
	
	def cortol(self, cortolthings, cortolmode, tok): #智能家居中的灯、开关控制于此（支持一句话插件）
		 	
		bt = baidu_tts()
		bs = baidu_stt(1, 2, 3, 4)
		r = recorder()
		h = hass()
		url = 'http://hassio.local'
		port = '8123'
		passwd = 'y20050801'
		headers = {'x-ha-access': passwd,
          		   'content-type': 'application/json'}
		
		domains = h.service()
		e_id = h.e_id()
		cortolthings = unicode(cortolthings, "utf-8", "ignore")
		
		try:
			if cortolmode == 'turn_on':
				if e_id[cortolthings] != None:
					if 'switch' in e_id[cortolthings]:
						color_name = 'a'
						service = '/api/services/switch/turn_on'
					elif 'light' in e_id[cortolthings]:
						ask = '请问要设置什么颜色，可以忽略'
                                                bt.tts(ask, tok)
                                                speaker.speak()
                                                speaker.ding()
                                                r.record()
                                                speaker.dong()
                                                color_name_f = bs.stt('./voice.wav', tok)
                                                if color_name_f != None:
                                                        color_name = h.chosecolor(color_name_f)
                                                else:
                                                        color_name = 'a'
						service = '/api/services/light/turn_on'
					elif 'automation' in e_id[cortolthings]:
						color_name = 'a'
						service = '/api/services/automation/turn_on'
			elif cortolmode == 'turn_off':
				if e_id[cortolthings] != None:
					if 'switch' in e_id[cortolthings]:
						color_name = 'a'
						service = '/api/services/switch/turn_off'
					elif 'light' in e_id[cortolthings]:
						color_name = 'a'
						service = '/api/services/light/turn_off'
					elif 'automation' in e_id[cortolthings]:
						color_name = 'a'
						service = '/api/services/automation/turn_off'
		except KeyError:
			sorry = '对不起，控制设备不存在，请注意！控制设备的名称得跟在homeassistant上设置的friendly，name一样'
			bt.tts(sorry, tok)
			speaker.speak()
		except TypeError:
			sorry = '对不起，控制设备不存在，请注意！控制设备的名称得跟在homeassistant上设置的friendly，name一样'
			bt.tts(sorry, tok)
			speaker.speak()
		except ValueError:
			sorry = '对不起，控制设备不存在，请注意！控制设备的名称得跟在homeassistant上设置的friendly，name一样'
			bt.tts(sorry, tok)
			speaker.speak()
		else:
			pass
		
		try:
			
			cortole_id = e_id[cortolthings]
			if color_name == 'a':
				dataf = {"entity_id": cortole_id.encode('utf-8')}
				data = json.dumps(dataf)
			else:
				dataf = {"color_name": color_name,
				 	"entity_id": cortole_id.encode('utf-8')}
				data = json.dumps(dataf)
		except KeyError:
			sorry = '对不起，控制设备不存在，请注意！控制设备的名称得跟在homeassistant上设置的friendly，name一样'
			bt.tts(sorry, tok)
			speaker.speak()
		except TypeError:
			sorry = '对不起，控制设备不存在，请注意！控制设备的名称得跟在homeassistant上设置的friendly，name一样'
			bt.tts(sorry, tok)
			speaker.speak()
		except ValueError:
			sorry = '对不起，控制设备不存在，请注意！控制设备的名称得跟在homeassistant上设置的friendly，name一样'
			bt.tts(sorry, tok)
			speaker.speak()
		else:
			print data
			cortolback  = requests.post(url + ':' + port + service,
						    headers=headers,
						    data=data)
			if cortolback.status_code == 200 or cortolback.status_code == 201:
				sayback = '执行成功'
				bt.tts(sayback, tok)
				speaker.speak()
			else:
				sayback = '执行错误'
				bt.tts(sayback, tok)
				speaker.speak()
	
	def sensor(self, getstatethings, tok):
		
		bt = baidu_tts()
		bs = baidu_stt(1, 2, 3, 4)
		r = recorder()
		h = hass()
		url = 'http://hassio.local'
		port = '8123'
		passwd = 'y20050801'
		headers = {'x-ha-access': passwd,
          		   'content-type': 'application/json'}

		e_id = e_id()
		getstatesthings = unicode(getstatethings, "utf-8", "ignore")
		getstatesthings_eid = e_id[getstatesthings]
		getstatesthings_l = getstatesthings_eid.encode('utf-8')
		service = '/api/states' + getstatesthings_l
		r = requests.get(url +':' + port + service,
			         headers=headers)
			
		json = r.json()
		
		if cortolback.status_code == 200 or cortolback.status_code == 201:
			
			state = json['state']
			if state == 'on':
				say = '此设备为开启状态'
				bt.tts(say, tok)
				speaker.speak()
			elif state == 'off':
				say = '此设备为关闭状态'
				bt.tts(say, tok)
				speaker.speak()
			elif state == 'below_horizon':
				say = '太阳已经下山了'
				bt.tts(say, tok)
				speaker.speak()
			else:
				if state.isdigit() == True:
					say = '数据是' + state
					bt.tts(say, tok)
					speaker.speak()
		else:
			sayback = '执行错误'
			bt.tts(sayback, tok)
			speaker.speak()		
	def study(self, tok):
		
		bt = baidu_tts()
		bs = baidu_stt(1, 2, 3, 4)
		r = recorder()
		h = hass()
		url = 'http://hassio.local'
		port = '8123'
		passwd = 'y20050801'
		headers = {'x-ha-access': passwd,
          		   'content-type': 'application/json'}
		
		say = '该功能暂未开发完毕，sorry'
		bt.tts(say, tok)
		speaker.speak()
 	
	
	
	
	
	
	
	
