#!/usr/bin/env python3
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import random
	
cryptos = [['BTC', 'bitcoin'], ['ETH', 'ethereum'], ['LINA', 'linear'], ['SXP', 'swipe'], ['TRADE', 'unitrade'], ['UNI', 'uniswap']]
run = 1
data = ''

while run == 1:
	now = datetime.now()
	dt_string = now.strftime("%-m/%-d/%y %-I:%M:%S")
	for i in cryptos:
		url = 'https://coinmarketcap.com/currencies/' + i[1] + '/'
		response = requests.get(url)
		html = response.content

		soup = BeautifulSoup(html, 'html.parser')
		symbol = i[0]
		price = soup.find('span' ,attrs={"class" : "cmc-details-panel-price__price"})
		changeprice = soup.find('span' ,attrs={"class" : "cmc-details-panel-price__price-change"})
		
		if price is not None:
			price = price.text
		else:
			price = ''
		
		if changeprice is not None:
			changeprice = changeprice.text
			changeprice = changeprice.replace('(','')
			changeprice = changeprice.replace(')','')
			changeprice = changeprice.replace(' ','')
		else:
			changeprice = ''
			
		data = data + symbol + '  ' + price + '  ' + changeprice + '  ||  '
	
	data = dt_string + ' || ' + data + dt_string
	
	my_file = open("/home/pi/ftp/cryptoprices.txt", "w")
	my_file.write(data)
	
	data = ''
	run = 1
	time.sleep(10)
