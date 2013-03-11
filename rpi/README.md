The Hackers of Catron
=====================

Raspberry Pi and Micro Communication
------------------------------------

This folder contains all of the non web-server code that communicates with the microcontroller. This code is run on the Pi, and made mostly in Python.

To facilitate communication via I2C, the Quick2Wire libraries are used. Because these libraries are under active development, it is recommended to not use them as a properly installed library, and instead update the python path to the downloaded directory. The libraries are included in this directory as their own git repo, so I have no idea what will happen if you run a git pull in that directory. Weird things, probably.

In any case, in order to use the libraries (and subsequently, the code in this directory), you need to add the quick2wire directory to the python path. Here's how to do that:

	export QUICK2WIRE_API_HOME=[cloned 477grp3 directory]/rpi/quick2wire-python-api
	export PYTHONPATH=$PYTHONPATH:$QUICK2WIRE_API_HOME

Additionally, the libraries use python 3, and the quick2wire-gpio-admin pacakges. In order to use those, you will need to install them. Here's how to do it on a pi:

	sudo apt-get upgrade
	gpg --list-keys
	curl http://dist.quick2wire.com/software@quick2wire.com.gpg.key | sudo apt-key add -
	sudo echo "deb http://dist.quick2wire.com/raspbian wheezy main" >> /etc/apt/sources.list
	sudo echo "deb-src http://dist.quick2wire.com/raspbian wheezy main" >> /etc/apt/sources.list
	sudo apt-get update
	sudo apt-get install quick2wire-gpio-admin python3 python-dev python-rpi.gpio
	sudo adduser $USER gpio

Currently, this directory only contains a test python script for communicating over I2C. It should use the same system as the final product (1 GPIO as a flag, with all communication over the TWI), but it works like an I2C serial terminal. All commands typed into it should be in the same format that we're expecting to send to the micro, and the micro should reply back appropriately.
