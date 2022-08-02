# -*- coding: utf-8 -*-
import glob
import time
import os
import sys
import ftplib
import urllib
import pathlib
from ftplib import FTP
from datetime import datetime


#  An Example Reading from /sys/bus/w1/devices/<ds18b20-id>/w1_slave
#  a6 01 4b 46 7f ff 0c 10 5c : crc=5c YES
#  a6 01 4b 46 7f ff 0c 10 5c t=26375

import RPi.GPIO as GPIO

#  Set Pullup mode on GPIO14 first.
GPIO_PIN_NUMBER=14
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN_NUMBER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#  set ftp creds
host = "ftp host"
username = "ftp username"
password = "ftp pw"


def ds18b20_read_sensors():
  rtn = {}
  w1_devices = []
  w1_devices = os.listdir("/sys/bus/w1/devices/")
  for deviceid in w1_devices:
    rtn[deviceid] = {}
    rtn[deviceid]['temp_c'] = None
    device_data_file = "/sys/bus/w1/devices/" + deviceid + "/w1_slave"
    if os.path.isfile(device_data_file):
      try:
         f = open(device_data_file, "r")
         data = f.read()
         f.close()
         if "YES" in data:
           (discard, sep, reading) = data.partition(' t=')
           rtn[deviceid]['temp_c'] = float(reading) / float(1000.0)
         else:
           rtn[deviceid]['error'] = 'No YES flag: bad data.'
      except Exception as e:
         rtn[deviceid]['error'] = 'Exception during file parsing: ' + str(e)
    else:
      rtn[deviceid]['error'] = 'w1_slave file not found.'
  return rtn;


temp_readings = ds18b20_read_sensors()
for t in temp_readings:
  if not 'error' in temp_readings[t]:
    temptemp = (temp_readings[t]['temp_c']) + 1.2185
    ftemp = round(((temptemp *1.8) + 32), 2)
    print (ftemp)
    
    # Write the temp to the monitoring file
    my_file = open("/var/www/html/temp.txt", "w")
    my_file.write(str(ftemp))
    my_file.close()
      
    # Work with the temp history
      
    # add the timestamp and save it to the file every 5 minutes

# Set the time zone to Denver
time.strftime('%X %x %Z')
os.environ['TZ'] = 'America/Denver'
time.tzset()
time.strftime('%X %x %Z')
min = time.strftime('%M')
# Set upload to no, will switch to yes if the time ends with 5 or 0
# if min.endswith('0') or min.endswith('5')
fulltime = time.strftime("%-I:%M:%S%p %-m/%d/%y")
fulltime = fulltime.lower()
temphistory = str(ftemp) + ' :: ' + str(fulltime)
filehistory = open('/var/www/html/temphistory.txt', 'a')
filehistory.write(temphistory + '\n')
filehistory.close()

#count the lines in the file and remove the newest lines if over 72
count = len(open('/var/www/html/temphistory.txt').readlines())      
if count > 3600:
  with open('/var/www/html/temphistory.txt', 'r') as fin:
    data = fin.read().splitlines(True)
  with open('/var/www/html/temphistory.txt', 'w') as fout:
    fout.writelines(data[1:])

# connect to host on default port i.e 21
ftp = FTP(host=host, user=username, passwd=password)
# print the content of directory
#print(ftp.dir())
fp = open("/var/www/html/temp.txt", 'rb')
# upload file
ftp.cwd('path to folder for temperature recording')
ftp.storbinary('STOR %s' % os.path.basename("temp.txt"), fp, 1024)

#upload the history
fp = open("/var/www/html/temphistory.txt", 'rb')
# upload file
ftp.storbinary('STOR %s' % os.path.basename("temphistory.txt"), fp, 1024)

fp.close()
#print(ftp.dir())

# before quitting download the updateled file to update the promises

# change the directory to where the file lives
ftp.cwd('ftp path to the file')

try:
  FILENAME = "updateled.txt"
  filelist = ftp.nlst()
  destination = '/home/pi/ftp/'
  fullfile = destination + FILENAME
  path = 'path to the directory the txt file will be in'

  # Check current working directory.
  os.chdir(destination)
  retval = os.getcwd()
  print("Current working directory is: " + retval)

  if FILENAME in filelist:
    print('file in file list')
    # pathFile = retval + FILENAME
    try:
      print('Deleting Local File')
      os.unlink('updateled.txt')
    except:
      print('File Does Not Exist Locally')

    try:
      ftp.cwd('path to the file on the ftp server')
      fhandle=open(FILENAME, 'wb')
      print('Getting ' + FILENAME)
      ftp.retrbinary('RETR '+ FILENAME, fhandle.write)
      fhandle.close()
    except:
      something = 'somethingelse'

    #Delete the downloaded file
    print('Deleting Existing FTP File')
    ftp.delete(FILENAME)

except:
  filename = 'none'

ftp.quit()
sys.exit()

	
  #time.sleep(60.0)
