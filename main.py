#!/usr/bin/python
import discum
from requests import get
from discord_webhook import DiscordWebhook
from os import system
import time
start_time = time.time()
from time import sleep, strftime, localtime
import random
import atexit
import json
try:
	from os import startfile
except:
	pass

#Data
class client:
	with open('config.json', "r") as file:
		data = json.load(file)
		token = data["token"]
		channel = data["channel"]
		grind = data["grind"]
		exp = data["exp"]
		coinflip = data["coinflip"]
		cfbet = int(data["cfbet"])
		cfrate = int(data["cfrate"])
		slot = data["slot"]
		sbet = int(data["sbet"])
		srate = int(data["srate"])
		command = data["command"]
		prefix = data["prefix"]
		allow = data["allow"]
		webhook = data["webhook"]
		link = data["link"]
		ping = data["ping"]
		side = ["h","t"]
		stopped = False
		run = True
		grind_amount = 0
		exp_amount = 0
		benefit_amount = 0
		current_cfbet = cfbet
		current_sbet = sbet
		OwOID = "408785106942164992"
		grind_status = '❌'
		exp_status = '❌'
		coinflip_status = '❌'
		slot_status = '❌'
		command_status = '❌'
		webhook_status = '❌'

#Color
class color:
	mark = "\033[104m"
	gray = "\033[90m"
	bold = "\033[1m"
	blue = "\033[94m"
	orange = "\033[33m"
	green = "\033[92m"
	yellow = "\033[93m"
	red = "\033[91m"
	purple = "\033[35m"
	reset = "\033[0m"

#Status
if client.grind:
	client.grind_status = '✅'
if client.exp:
	client.exp_status = '✅'
if client.coinflip:
	client.coinflip_status = '✅'
if client.slot:
	client.slot_status = '✅'
if client.command:
	client.command_status = '✅'
if client.webhook:
	client.webhook_status = '✅'

#Time
def timelog():
	return f'\033[104m{strftime("%H:%M:%S", localtime())}\033[0m'
def timerun():
	timerun = time.time() - start_time
	return f'{strftime("**__%H__h** **__%M__m** **__%S__s**",time.gmtime(timerun))}'

#Sign In
bot = discum.Client(token=client.token, log=False, build_num=0, x_fingerprint="None", user_agent=[
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36/PAsMWa7l-11',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 YaBrowser/20.8.3.115 Yowser/2.5 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.7.2) Gecko/20100101 / Firefox/60.7.2'])

#Log In
@bot.gateway.command
def on_ready(resp):
	if resp.event.ready_supplemental:
		user = bot.gateway.session.user
		print()
		print("""{}  █▀█ █ █ ▄▀█ █▄ █ █▀▄ ▄▀█ ▀█▀{}""".format(color.blue, color.reset))
		print("""{}  █▀▀ █▀█ █▀█ █ ▀█ █▄▀ █▀█  █{}""".format(color.blue, color.reset))
		print()
		print("{}     🎉 LOGIN SUCCESSFUL 🎉{}".format(color.green, color.reset))
		print("{}  ---------------------------{}".format(color.green, color.reset))
		print("    {}User: {}{}{}{}".format(color.orange, color.reset, color.bold, user['username'], color.reset))
		print("    {}Grind:    {} {}".format(color.orange, client.grind_status, color.reset))
		print("    {}Exp:      {} {}".format(color.orange, client.exp_status, color.reset))
		print("    {}Coinflip: {} {}".format(color.orange, client.coinflip_status, color.reset))
		print("    {}Slot:     {} {}".format(color.orange, client.slot_status, color.reset))
		print("    {}Command:  {} {}".format(color.orange, client.command_status, color.reset))
		print("    {}Webhook:  {} {}".format(color.orange, client.webhook_status, color.reset))
		print("{}  ---------------------------{}".format(color.green, color.reset))
		print()
		run()
		
#Webhook
def webhook(message):
	webhook = DiscordWebhook(url = client.link, content=message)
	webhook = webhook.execute()

#Captcha Bypass
@bot.gateway.command
def check(resp):
	if resp.event.message:
		m = resp.parsed.auto()
		if m['channel_id'] == client.channel and m['author']['id'] == client.OwOID:
			if '⚠' in m['content'] or 'https://owobot.com/captcha' in m['content'] or 'don\'t have enough cowoncy!' in m['content']:
				client.stopped = True

#Coinflip Check
@bot.gateway.command
def cfcheck(resp):
	if not client.stopped and client.coinflip and client.run:
		if resp.event.message_updated:
			m = resp.parsed.auto()
			try:
				if m['channel_id'] == client.channel and m['author']['id'] == client.OwOID:
					if 'you lost' in m['content']:
						print("{} {}[INFO] Coinflip Lost {} Cowoncy{}".format(timelog(), color.red, client.current_cfbet, color.reset))
						client.benefit_amount -= client.current_cfbet
						client.current_cfbet *= client.cfrate
					if 'you won' in m['content']:
						print("{} {}[INFO] Coinflip Won {} Cowoncy{}".format(timelog(), color.green, client.current_cfbet, color.reset))
						client.benefit_amount += client.current_cfbet
						client.current_cfbet = client.cfbet
			except KeyError:
				pass

#Slot Check
@bot.gateway.command
def scheck(resp):
	if not client.stopped and client.slot and client.run:
		if resp.event.message_updated:
			m = resp.parsed.auto()
			try:
				if m['channel_id'] == client.channel and m['author']['id'] == client.OwOID:
					if 'won nothing' in m['content']:
						print("{} {}[INFO] Slot Lost {} Cowoncy{}".format(timelog(), color.red, client.current_sbet, color.reset))
						client.benefit_amount -= client.current_sbet
						client.current_sbet *= client.srate
					if '<:eggplant:417475705719226369> <:eggplant:417475705719226369> <:eggplant:417475705719226369>' in m['content']:
						print("{} {}[INFO] Slot Draw{}".format(timelog(), color.bold, color.reset))
					if '<:heart:417475705899712522> <:heart:417475705899712522> <:heart:417475705899712522>' in m['content']:
						print("{} {}[INFO] Slot Won {} Cowoncy (x2){}".format(timelog(), color.green, client.current_sbet, color.reset))
						client.benefit_amount += client.current_sbet
						client.current_sbet = client.sbet
					if '<:cherry:417475705178161162> <:cherry:417475705178161162> <:cherry:417475705178161162>' in m['content']:
						print("{} {}[INFO] Slot Won {} Cowoncy (x3){}".format(timelog(), color.green, client.current_sbet * 2, color.reset))
						client.benefit_amount += client.current_sbet * 2
						client.current_sbet = client.sbet
					if '<:cowoncy:417475705912426496> <:cowoncy:417475705912426496> <:cowoncy:417475705912426496>' in m['content']:
						print("{} {}[INFO] Slot Won {} Cowoncy (x4){}".format(timelog(), color.green, client.current_sbet * 3, color.reset))
						client.benefit_amount += client.current_sbet * 3
						client.current_sbet = client.sbet
					if '<:o_:417475705899843604> <:w_:417475705920684053> <:o_:417475705899843604>' in m['content']:
						print("{} {}[INFO] Slot Won {} Cowoncy (x10){}".format(timelog(), color.green, client.current_sbet * 9, color.reset))
						client.benefit_amount += client.current_sbet * 9
						client.current_sbet = client.sbet
			except KeyError:
				pass

#Command
@bot.gateway.command
def command(resp):
	if client.command:
		prefix = client.prefix
		if resp.event.message:
			m = resp.parsed.auto()
			if m['author']['id'] == bot.gateway.session.user['id'] or m['author']['id'] == client.allow:
				#Help
				if m['content'].startswith(f"{prefix}help"):
					bot.sendMessage(str(m['channel_id']), """
I have **__5__ Commands**:

> **`send`** + **`text`**
> **`setting`**
> **`stat`**
> **`start`**
> **`stop`**
""")
					print("{} {}[SELF] Help List 📃{}".format(timelog(), color.gray, color.reset))
				#Send
				if m['content'].startswith(f"{prefix}send"):
					message = m['content'].replace(f'{prefix}send ', '')
					bot.sendMessage(str(m['channel_id']), message)
					print("{} {}[SELF] Send {}{}".format(timelog(), color.gray, message, color.reset))
				#Setting
				if m['content'].startswith(f"{prefix}setting"):
					bot.sendMessage(str(m['channel_id']),
					"""
> __**Grind**__・{}
> __**Exp**__・{}
> __**Coinflip**__・{}
> __**Slot**__・{}
> __**Command**__・{}
> __**Webhook**__・{}
""".format(client.grind_status, client.exp_status, client.coinflip_status, client.slot_status, client.command_status, client.webhook_status))
					print("{} {}[SELF] Setting ⚙️{}".format(timelog(), color.gray, color.reset))
				#Stat
				if m['content'].startswith(f"{prefix}stat"):
					bot.sendMessage(str(m['channel_id']),
					"""
I ran for {} with:
> Grinding __**{}**__ times 🎯
> Sending __**{}**__ quotes ✏️
> Gambling __**{}**__ cowoncys 💵
""".format(timerun(), client.grind_amount, client.exp_amount, client.benefit_amount))
					print("{} {}[SELF] Stat 📊{}".format(timelog(), color.gray, color.reset))
				#Start
				if m['content'].startswith(f"{prefix}start"):
					client.run = True
					bot.sendMessage(str(m['channel_id']), "> **Starting... 🔔**")
					print("{} {}[SELF] Start Selfbot 🔔{}".format(timelog(), color.gray, color.reset))
				#Stop
				if m['content'].startswith(f"{prefix}stop"):
					client.run = False
					bot.sendMessage(str(m['channel_id']), "> **Stopping... 🚨**")
					print("{} {}[SELF] Stop Selfbot 🚨{}".format(timelog(), color.gray, color.reset))

#Grind
def grind():
	if not client.stopped and client.grind and client.run:
		bot.typingAction(client.channel)
		bot.sendMessage(str(client.channel), "owo")
		print("{} {}[SEND] owo{}".format(timelog(), color.yellow, color.reset))
	if not client.stopped and client.grind and client.run:
		sleep(random.randint(1, 2))
		bot.typingAction(client.channel)
		bot.sendMessage(str(client.channel), "owoh")
		print("{} {}[SEND] owoh{}".format(timelog(), color.yellow, color.reset))
	if not client.stopped and client.grind and client.run:
		sleep(random.randint(1, 2))
		bot.typingAction(client.channel)
		bot.sendMessage(str(client.channel), "owob")
		print("{} {}[SEND] owob{}".format(timelog(), color.yellow, color.reset))
		client.grind_amount += 1

#Exp
def exp():
	if not client.stopped and client.exp and client.run:
		try:	
			response = get("http://api.quotable.io/random")
			if response.status_code == 200:
				json_data = response.json()
				data = json_data["content"]
				bot.sendMessage(client.channel, data)
				print("{} {}[SEND] Quote{}".format(timelog(), color.yellow, color.reset))
				client.exp_amount += 1
				sleep(random.randint(1, 2))
		except:
			pass

#Coinflip
def cf():
	if client.current_cfbet  > 250000:
		client.current_cfbet = client.cfbet
	if not client.stopped and client.coinflip and client.run:
		side = random.choice(client.side)
		bot.typingAction(client.channel)
		bot.sendMessage(str(client.channel), "owo cf {} {}".format(client.current_cfbet, side))
		print("{} {}[SEND] owo cf {} {}{}".format(timelog(), color.yellow, client.current_cfbet, side, color.reset))
		sleep(random.randint(1, 2))

#Slot
def s():
	if client.current_sbet  > 250000:
		client.current_sbet = client.sbet
	if not client.stopped and client.slot and client.run:
		bot.typingAction(client.channel)
		bot.sendMessage(str(client.channel), "owo s {}".format(client.current_sbet))
		print("{} {}[SEND] owo s {}{}".format(timelog(), color.yellow,client.current_sbet, color.reset))
		sleep(random.randint(1, 2))

#Run
def run():
	farm = 0
	text = 0
	coinflip = 0
	slot = 0
	while True:
		if client.stopped:
			bot.gateway.close()
		if not client.stopped and client.run:
			grind()
			if time.time() - text > random.randint(50, 200):
				exp()
				text = time.time()
			sleep(random.randint(3, 5))
			cf()
			s()
			sleep(random.randint(10, 15))
bot.gateway.run()

#Exit
@atexit.register
def exit():
	client.stopped = True
	try:
		startfile('music.mp3')
	except:
		pass
	if client.webhook:
		webhook(f"**<a:pepeintelligent:964835071595008000> chà có sự cố ở <#{client.channel}> <@{client.ping}>**")
		webhook(f"**<a:1096324489022808094:1098237958324236388> chà có sự cố ở <#{client.channel}> <@{client.ping}>**")
		webhook(f"**<a:quay:1086553810220089374> chà có sự cố ở <#{client.channel}> <@{client.ping}>**")
	bot.switchAccount(client.token[:-4] + 'FvBw')
	print("{} {}[INFO] I found a captcha 💀".format(timelog(), color.red, color.reset))
	print()
	print("{}          📊 STAT 📊{}".format(color.orange, color.reset))
	print("{}  --------------------------{}".format(color.orange, color.reset))
	print("    {}Grind:{}  {}{} Times 🎯{}".format(color.green, color.reset, color.bold, client.grind_amount, color.reset))
	print("    {}Exp:{}    {}{} Quotes ✏️{}".format(color.green, color.reset, color.bold, client.exp_amount, color.reset))
	print("    {}Gamble:{} {}{} Cowoncys 💵{}".format(color.green, color.reset, color.bold, client.benefit_amount, color.reset))
	print("{}  --------------------------{}".format(color.orange, color.reset))
	exit = input("{}Enter 'OK' to Reset: {}".format(color.blue, color.reset))
	if exit == 'OK':
		system('python "main.py"')