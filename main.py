#! /usr/bin/env python
# -*- coding: utf-8 -*-

import amino
import secmail
import random
import string 
from hashlib import sha1
import base64
import time
from bs4 import BeautifulSoup
import webbrowser
from nickname_generator import generate
import json

def device_gen():
	st = 69
	ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = st))
	MetaSpecial = sha1(ran.encode("utf-8"))
	thedevice = '01' + (MetaSpecial).hexdigest() + sha1(bytes.fromhex('01') + MetaSpecial.digest() + base64.b64decode("6a8tf0Meh6T4x7b0XvwEt+Xw6k8=")).hexdigest()

	return thedevice.upper()

def create():
	with open('accounts.json', 'r') as f:
		data = json.load(f)

	global password

	exceptions = amino.lib.util.exceptions

	device = device_gen()

	mail = secmail.SecMail()
	email = mail.generate_email()
	client = amino.Client(deviceId = device)

	nickname = generate('ru')
	

	client.request_verify_code(email = email)
	time.sleep(4)
	message = mail.get_messages(email=email).id
	message = message[0]

	readmsg = mail.read_message(email = email, id = message).htmlBody
	silka = BeautifulSoup(readmsg, 'lxml')
	ssylka = silka.find_all('a')
	ssylka = ssylka[0].get('href')

	webbrowser.open_new_tab(ssylka)

	verifycode = input('Введите, пожалуйста, код: ')

	try:
		client.register(nickname = nickname, email = email, password = password, verificationCode = verifycode, deviceId = device)
		data[email] = {}
		data[email]['device'] = device
		data[email]['password'] = password
		print(f'Аккаунт зарегестрирован под ником {nickname}')
	except exceptions.UnsupportedEmail:
		print('Эта почта не поддерживается')
		return
	except exceptions.AccountLimitReached:
		print('Достигнут лимит аккаунтов, попробуйте ещё раз.')
		return
	except exceptions.IncorrectVerificationCode:
		print('Код верификации неправильный.')
		return
	except exceptions.CommandCooldown:
		print('Куллдаун.')
		return
	except exceptions.VerificationRequired as e:
		link = e.args[0]["url"]
		print(link)
		input('Нажмите <Enter> для продолжения.')
		try:
			client.register(nickname = nickname, email = email, password = password, verificationCode = verifycode, deviceId = device)
			data[email] = {}
			data[email]['device'] = device
			data[email]['password'] = password
			print(f'Аккаунт зарегестрирован под ником {nickname}')
		except:
			print('Не удалось создать')
			return
	except Exception as e:
		print(str(e))
		return

	with open('accounts.json', 'w') as f:
		json.dump(data, f, indent=4)

password = '12345678'

while True:
	create()



