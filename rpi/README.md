The Hackers of Catron
=====================

Raspberry Pi and Micro Communication
------------------------------------

This folder contains all of the non web-server code that communicates with the microcontroller. This code is run on the Pi, and made mostly in Python.

To facilitate communication via I2C, the Quick2Wire libraries are used. Because these libraries are under active development, it is recommended to not use them as a properly installed library, and instead update the python path to the downloaded directory. The libraries are included in this directory as their own git repo. If you update them, this code may no longer work.

In order to run the code in this directory and the web interface, you need to run the following series of commands:

	sudo apt-get upgrade
	gpg --list-keys
	curl http://dist.quick2wire.com/software@quick2wire.com.gpg.key | sudo apt-key add -
	sudo echo "deb http://dist.quick2wire.com/raspbian wheezy main" >> /etc/apt/sources.list
	sudo echo "deb-src http://dist.quick2wire.com/raspbian wheezy main" >> /etc/apt/sources.list
	sudo apt-get update
	sudo apt-get install quick2wire-gpio-admin python3 python-dev python-rpi.gpio
	sudo adduser $USER gpio
	sudo adduser $USER i2c
	sudo python3 [this repo's location]/rpi/quick2wire-python-api/setup.py install

Files in this Directory
-----------------------

This folder contains the following relevant files and folders:
* quick2wire-python-api/ is the quick2wire libraries, the version that we are using.
* catronBootup.py should run when the pi has booted (add it to /etc/rc.local). It generates a random board.
* testInterface.py and testInterface.py.bak are a test terminal to play with i2c reading, writing, and GPIO flags. It no longer works, and is mostly just a playground.
* timeTest.py can be ignored. It tests the difference in read time between i2c and gpio. i2c is faster.
* writeBytes.py writes a value to a register on a specific i2c device. It was used for debugging. It can be run like: `writeBytes.py [hex address] [register] [value]`.
