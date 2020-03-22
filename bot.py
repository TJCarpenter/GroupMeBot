import os
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request
import random

app = Flask(__name__)
bot_id = "9dde9cf2c705a02b106bb079a1"

# Called whenever the app's callback URL receives a POST request
# That'll happen every time a message is sent in the group
@app.route('/', methods=['POST'])
def webhook():
	# 'message' is an object that represents a single GroupMe message.
	message = request.get_json()

	if wake(message):
		command(message)
		reply(random.choice(['(╥﹏╥)', '(っ◕‿◕)っ', '(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧', '(╯°□°）╯︵ ┻━┻','(☞ﾟ∀ﾟ)☞','(⋟﹏⋞)', '┻━┻︵ \(°□°)/ ︵ ┻━┻', '┏━┓ ︵ /(^.^/)','(╭ರ_•́)', '( ͡° ͜ʖ ͡°)', 'ಠ_ಠ', 'ლ(ಠ益ಠ)ლ', 'ʕつ•ᴥ•ʔつ','┬─┬ ノʕ•ᴥ•ノʔ', 'ʕつಠᴥಠʔつ ︵ ┻━┻', '(つ◉益◉)つ', ' ლ(ಠ_ಠლ)', '(╯°□°)╯︵ ɹoɹɹƎ']))
		
	return "ok", 200

################################################################################

# Check message to see if there is a wake character
def wake(message):
	if message['text'][0] == "!":
		return True
	else:
		return False

# Determine command to be run
def command(message):
	# Commands:
	#	help (h)
	#	times (t)

	command_text = message['text'].replace('!', '')

	if command_text in ['h', 'help']:
		reply('!h !help\nDisplays all available commands.\n\n!t !times\nDisplays times for chow.\n\n!f !fact\nGives an interesting fact.\n\n!c !coin\nFlip a coin.\n\n!d20\nRoll a 20 sided die.')

	if command_text in ['t', 'times']:
		reply('WEEKDAYS | MON-FRI\nBreakfast\t0730 - 0830\nLunch\t1100 - 1300\nDinner\t1630 - 1830\n\nWEEKENDS | SAT-SUN\nBreakfast\t0730 - 0900\nLunch\t 1130 - 1330\nDinner\t1630 - 1800')

	if command_text in ['f', 'fact']:
		reply_with_fact()

	if command_text in ['c', 'coin']:
		reply(random.choice(['Heads', 'Tails']))

	if command_text == 'd20':
		reply('You rolled a {}'.format(random.randint(1, 20)))


# Send a message in the groupchat
def reply(msg):
	url = 'https://api.groupme.com/v3/bots/post'
	data = {
		'bot_id'		: bot_id,
		'text'			: msg
	}
	request = Request(url, urlencode(data).encode())
	json = urlopen(request).read().decode()

# Send a random fact in the groupchat
def reply_with_fact():
	reply(random.choice(open('facts.txt').read().splitlines()))

# Send a message with an image attached in the groupchat
def reply_with_image(msg, imgURL):
	url = 'https://api.groupme.com/v3/bots/post'
	urlOnGroupMeService = upload_image_to_groupme(imgURL)
	data = {
		'bot_id'		: bot_id,
		'text'			: msg,
		'picture_url'		: urlOnGroupMeService
	}
	request = Request(url, urlencode(data).encode())
	json = urlopen(request).read().decode()
	
# Uploads image to GroupMe's services and returns the new URL
def upload_image_to_groupme(imgURL):
	imgRequest = requests.get(imgURL, stream=True)
	filename = 'temp.png'
	postImage = None
	if imgRequest.status_code == 200:
		# Save Image
		with open(filename, 'wb') as image:
			for chunk in imgRequest:
				image.write(chunk)
		# Send Image
		headers = {'content-type': 'application/json'}
		url = 'https://image.groupme.com/pictures'
		files = {'file': open(filename, 'rb')}
		payload = {'access_token': 'eo7JS8SGD49rKodcvUHPyFRnSWH1IVeZyOqUMrxU'}
		r = requests.post(url, files=files, params=payload)
		imageurl = r.json()['payload']['url']
		os.remove(filename)
		return imageurl

# Checks whether the message sender is a bot
def sender_is_bot(message):
	return message['sender_type'] == "bot"
