# led-matrix
The code that runs my LED matrix on a rPi w/ HiLetgo MAX7219

This project started with me wanting a Crypto ticker using linked HiLetgo MAX7219 LED Matricies. I have since turned it into a message board that scrolls a random inspirational message from a text file and if it sees a txt file with a specific name on an FTP site, it downloads it and adds it to the beginning as a special message. It shows messages on minutes ending in 1, 4 and 9, otherwise it shows the time. When it shows the time and it is at the 30 second mark, it displays the full date. 

The clock functions were taken from the following: https://github.com/rm-hull/luma.led_matrix/blob/master/examples/silly_clock.py

I went through the code and modified it to suit my needs. 
