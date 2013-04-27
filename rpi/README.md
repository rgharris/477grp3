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

Additionally, in order to replicate the functionality of the raspberry pi in the board, you will need to install and configure hostapd for an access point (and have a compatible USB Wireless adapter attached to the pi), udhcpd for DHCP, and dnsmasq for DNS services, to give the pi a domain so that you can access it easily. Additionally, dnsmasq can be used instead of udhcpd for DHCP serving, though we did not do this. Instructions for setting up all of these can be easily found online. Some quick, possibly helpful links, include:

* [The Raspberry Pi Blog](http://www.rpiblog.com/2012/12/turn-raspberry-pi-into-wireless-access.html)'s post on making an access point of a raspberry pi, which contains useful info on udhcpd and hostapd.
* The wireless adapter we used to run the access point on the Raspberry Pi was the [Tenda W311MI 150Mbps Wireless PICO USB Adapter] (http://www.amazon.com/gp/product/B006GCYAOI). 
* [Andrew Oberstar](http://www.andrewoberstar.com/blog/2012/12/30/raspberry-pi-as-server-dns-and-dhcp)'s blog post on using the Raspberry Pi as a server for DNS and DHCP, which explains configuring dnsmasq.

Finally, we added catronBootup.py and bootupInterface.sh to `/etc/rc.local` so that they would start on boot. bootupInterface.sh should come before catronBootup.py in the file.

Files in this Directory
-----------------------

This folder contains the following relevant files and folders:
* quick2wire-python-api/ is the quick2wire libraries, the version that we are using.
* catronBootup.py should run when the pi has booted (add it to /etc/rc.local). It generates a random board.
* bootupInterface.sh is a quick, hacky solution to an issue we were having with bringing up the wireless interface on boot - it was inconsistant, so this script will continously try to bring it up until it is actually up.
* writeBytes.py writes a value to a register on a specific i2c device. It was used for debugging. It can be run like: `writeBytes.py [hex address] [register] [value]`.
