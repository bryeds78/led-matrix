#!/usr/bin/env python3

#If luma.led gets messed up, use the following to fix it on a RPI
#sudo -H pip3 install --upgrade --force-reinstall --ignore-installed luma.core
#sudo -H pip3 install --upgrade --force-reinstall --ignore-installed luma.led_matrix

import time
from datetime import datetime
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, tolerant, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
from luma.core.virtual import viewport
import requests
import random
import os

	
cryptos = [['BTC', 'bitcoin'], ['ETH', 'ethereum'], ['SXP', 'swipe'], ['ZIL', 'zilliqa']]
data = []
showme = ''
run = 0
finishedPromise = 0

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=12 , block_orientation=-90, rotate=2, height=8, contrast=20)

def meetingReminderSoon():
	meetMessage = "The meeting is starting soon   ||   The meeting is starting soon   ||   The meeting is starting soon   ||   The meeting is starting soon   ||   The meeting is starting soon"
	show_message(device, meetMessage, fill="white", font=proportional(CP437_FONT), scroll_delay = 0.02)

def meetingReminderNow():
	meetMessage = "MEETING IS STARTING NOW   ||   MEETING IS STARTING NOW   ||   MEETING IS STARTING NOW   ||   MEETING IS STARTING NOW   ||   MEETING IS STARTING NOW   ||   MEETING IS STARTING NOW"
	show_message(device, meetMessage, fill="white", font=proportional(CP437_FONT), scroll_delay = 0.02)

def showLEDUpdate():

	ledMessage = open('/home/pi/ftp/updateled.txt').readlines()

	#convert the ledUpdate to a string
	for i in ledMessage:
		ledMessage = i

	interruptMsg = 'clearly'
	showLED = 'yes'

	if interruptMsg in ledMessage:
		showLED = 'no'

	if showLED == 'yes':
		ledMessage = '  ||=+=||  ' + ledMessage + '  ||=+=||  ' + ledMessage + '  ||=+=||  ' + ledMessage + '  ||=+=||  ' + ledMessage + '  ||=+=||  '
		randomPixels()
		show_message(device, ledMessage, fill="white", font=proportional(tolerant(LCD_FONT, missing="?")), scroll_delay = 0.02)
		randomPixels()

def randomPromise():
	randomPixels()
	randpromise = random.choice(open('/home/pi/ftp/promises.txt').readlines())

	print(randpromise)
	randpromise = randpromise + '  ||  ' + randpromise

	showLEDUpdate()
	show_message(device, randpromise, fill="white", font=proportional(tolerant(LCD_FONT, missing="?")), scroll_delay = 0.02)
	randomPixels()
	showLEDUpdate()
	randomPixels()
	show_message(device, randpromise, fill="white", font=proportional(tolerant(LCD_FONT, missing="?")), scroll_delay = 0.02)
	finishedPromise = 1
	return finishedPromise

def randomPixels():
	runrand = 0
	while runrand < 30:
		with canvas(device) as draw:
			for i in range(48):
				x = random.randint(0, device.width)
				y = random.randint(0, device.height)

				# 'draw' is an ImageDraw object.
				draw.point((x, y), fill="white")
				time.sleep(0.0007)
		runrand = runrand + 1
	
def cryptoticker():
	
	f = open("/home/pi/ftp/cryptoprices.txt", "r")
	showme = f.read()
	
	randomPixels()
	show_message(device, showme, fill="white", font=proportional(tolerant(LCD_FONT, missing="?")), scroll_delay = 0.02)
	randomPixels()
	show_message(device, showme, fill="white", font=proportional(tolerant(LCD_FONT, missing="?")), scroll_delay = 0.02)
	randomPixels()
	show_message(device, showme, fill="white", font=proportional(tolerant(TINY_FONT, missing="?")), scroll_delay = 0.02)

def minute_change(device):
	'''When we reach a minute change, animate it.'''
	hours = datetime.now().strftime('%I')
	minutes = datetime.now().strftime('%M')

	def helper(current_y):
		with canvas(device) as draw:
			text(draw, (32, 0), hours, fill="white", font=proportional(tolerant(CP437_FONT, missing="?")))
			text(draw, (47,0), ":", fill="white", font=proportional(tolerant(TINY_FONT, missing="?")))
			text(draw, (49, current_y), minutes, fill="white", font=proportional(tolerant(CP437_FONT, missing="?")))
		time.sleep(0.1)
	for current_y in range(0, 9):
		helper(current_y)
	minutes = datetime.now().strftime('%M')
	for current_y in range(9, 0, -1):
		helper(current_y)


def animation(device, from_y, to_y):
	'''Animate the whole thing, moving it into/out of the abyss.'''
	hourstime = datetime.now().strftime('%I')
	mintime = datetime.now().strftime('%M')
	current_y = from_y
	while current_y != to_y:
		with canvas(device) as draw:
			text(draw, (32, current_y), hourstime, fill="white", font=proportional(tolerant(CP437_FONT, missing="?")))
			text(draw, (47, current_y), ":", fill="white", font=proportional(tolerant(TINY_FONT, missing="?")))
			text(draw, (49, current_y), mintime, fill="white", font=proportional(tolerant(CP437_FONT, missing="?")))
		time.sleep(0.1)
		current_y += 1 if to_y > from_y else -1


def main():
	randomPixels()
	os.environ['TZ'] = 'America/Denver'
	time.tzset()
	# Setup for Banggood version of 4 x 8x8 LED Matrix (https://bit.ly/2Gywazb)
	serial = spi(port=0, device=0, gpio=noop())
	device = max7219(serial, cascaded=12, block_orientation=-90, blocks_arranged_in_reverse_order=False, rotate=2)
	device.contrast(16)

	# The time ascends from the abyss...
	animation(device, 9, 0)

	toggle = False  # Toggle the second indicator every second
	while True:
		toggle = not toggle
		sec = datetime.now().second
		min = datetime.now().minute
		min = str(min)
		now = datetime.now()
		meetRemind = datetime.now().strftime('%H:%M')
		dow = now.strftime("%a")
		dow = dow.lower()
		nomeeting = 'yes'
		if dow == 'wed' or dow == 'fri':
			nomeeting = 'no'
		if sec == 59:
			# When we change minutes, animate the minute  change
			minute_change(device)
		elif sec == 30:
			# Half-way through each minute, display the complete date/time,
			# animating the time display into and out of the abyss.
			full_msg = now.strftime("%a %b %-d %-I:%M:%S %Y") 
			animation(device, 0, 9)
			show_message(device, full_msg, fill="white", font=proportional(tolerant(CP437_FONT, missing="?")))
			animation(device, 9, 0)
		elif meetRemind == '09:13' and nomeeting == 'no':
			animation(device, 0, -1)
			meetingReminderSoon()
		elif meetRemind == '09:15' and nomeeting == 'no':
			animation(device, 0, -1)
			meetingReminderNow()
		elif min.endswith('0') or min.endswith('1') or min.endswith('4') or min.endswith('8'):
			animation(device, 0, -1)
			randomPromise()
		else:
			# Do the following twice a second (so the seconds' indicator blips).
			# I'd optimize if I had to - but what's the point?
			# Even my Raspberry PI2 can do this at 4% of a single one of the 4 cores!
			hours = datetime.now().strftime('%I')
			minutes = datetime.now().strftime('%M')
			with canvas(device) as draw:
				text(draw, (32, 0), hours, fill="white", font=proportional(tolerant(CP437_FONT, missing="?")))
				text(draw, (47, 0), ":" if toggle else " ", fill="white", font=proportional(tolerant(TINY_FONT, missing="?")))
				text(draw, (49, 0), minutes, fill="white", font=proportional(tolerant(CP437_FONT, missing="?")))
			time.sleep(0.5)

if __name__ == "__main__":
	main()
	
