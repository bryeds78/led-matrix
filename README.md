# led-matrix
The code that runs my LED matrix on a rPi w/ HiLetgo MAX7219

This project started with me wanting a Crypto ticker using linked HiLetgo MAX7219 LED Matricies. I have since turned it into a message board that scrolls a random inspirational message from a text file and if it sees a txt file with a specific name on an FTP site, it downloads it and adds it to the beginning as a special message. It shows messages on minutes ending in 1, 4 and 9, otherwise it shows the time. When it shows the time and it is at the 30 second mark, it displays the full date. I also built in a function that will read a special message file. The special message file is created through a webhook that is triggered by IFTTT, which is triggered by google assistant. I say "Hey Google, update my led <insert message here>" and it saves that message to a specific file. The temp.py file that is described later handles detecting and downloading the file to the rPi. 

The clock functions were taken from the following: https://github.com/rm-hull/luma.led_matrix/blob/master/examples/silly_clock.py

I went through the code and modified it to suit my needs. 

The code also uses the temp.py file in this repository. temp.py was built to monitor the temperature in our daughter's bedroom and save it to a txt file on an FTP so I can view it over the web through my domain. It also removes the last line of a history file and adds the current date, time and temp to it to create a running history we can also view online. Because this was already running every minute and logging into the FTP to add the data to the site, I decided to use it to also check for messages from the the IFTTT/Google Assistant integration. 

myclock.py is set to run at startup with the rpi and temp.py is set to run every minute. 
  
The IFTTT integration links to google assistant and triggers a webhook. You create a new applet in IFTTT, use google assistant with the "when I say text with a special ingredient" and then you use webhook and a get request on your web server to process the phrase and save it somewhere. I did this in PHP and can provide the code if needed. I also added a keyword - if I use the phrase clearly, meaning have a special message with only the word clearly, it will tell the system to not display the special message. You can change it to anything you want.  
  
So you'll need myclock.py, temp.py (feel free to rename them), set myclock to run at start and temp.py to run every minute. Use IFTTT to make the google assistant integration with a webhook and use the webhook to send the phrase to a page that process the data to a txt file. The TXT file is downloaded to the rpi through temp.py, myclock.py looks for it and reads it, then adds it to the beginning of the messages, unless the key phrase is used.
  
For the messages, I found quotes and things I like. It's just a txt file with a new line for each one. You can use as many lines as you want. 
  
Side note: I am running this on a rPi Zerow - when temp.py runs to check the FTP and process, it does slow it down for a couple of seconds. If you use a higher powered rpi, it should work better. 
  
I will likely update this with more information and details, but I wanted to get this out for anyone interested. I also give credit to those who made the original code I used to make this happen. I was going through a TON of online resources so I don't know who it all was, but I do know for sure it was the people who made silly_clock.py that really helped. It was hard to get these LEDs working right! I'll the appropriate credit when I can find the sources - I have extensive side notes as I didn't want to have to figure it all out again after i killed it accidentally once and had to go back and figure it all out.

  I also added cryptofile.py to the repository, it scrapes coinmarketcap.com for the proces of specified crypto and saves to a txt file that you can integrate into myclock.py

I apologize for the not so professional code! I am in IT and can script, build websites, etc, but python is new and I have barely any formal programming training, I certainly don't prescribe to any specific patterns or methods, but I do try to keep it clean. I was not writing and putting together this code with the thought of sharing it, so maybe I will go and update it if time permits, but it's pretty straight forward. Not a bad first time python project.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Here are the raw notes and steps I used to get any prerequisites setup and running before I was able to execute this successfully.
  
  Turn on SSH & SPI from raspi-config
Install and configure a FTP server (proftpd - install and then login with the admin creds)

* sudo -H pip3 install --upgrade --force-reinstall --ignore-installed luma.core
* sudo -H pip3 install --upgrade --force-reinstall --ignore-installed luma.led_matrix

	sudo usermod -a -G spi,gpio pi
	sudo apt install build-essential python3-dev python3-pip
	sudo apt-get install git
	sudo -H pip3 install --upgrade --ignore-installed pip3 setuptools
	sudo apt install proftpd (login with rpi creds)
	sudo -H pip3 install --upgrade --force-reinstall --ignore-installed luma.core
	sudo -H pip3 install --upgrade --force-reinstall --ignore-installed pillow
sudo apt-get install build-essential
sudo apt-get install python-dev python-pip

sudo pip install schedule, requests, bs4
install pip requests
install pip bs4

sudo apt install build-essential python-dev python-pip
sudo -H pip install --upgrade --ignore-installed pip setuptools
sudo -H pip install --upgrade luma.led_matrix

Use crontab method to start the script with the system:
https://www.tomshardware.com/how-to/run-script-at-boot-raspberry-pi
