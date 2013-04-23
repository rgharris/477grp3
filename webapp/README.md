The Hackers of Catron
=====================

Web Interface: Setup
--------------------
This folder contains the web interface for the Hackers of Catron. The web interface is designed for mobile devices, but looks decent enough on a non-mobile device as well. Additionally, the interface does make use of i2c, so it must be run on a raspberry pi or modified to run on something else with i2c access. Alternatively the code could just be used as a starting point for a port to a different device.

The code is written as WSGI in python 3. In order to run the code, you will need to set up your web server appropriately. For apache on the raspberry pi, this is what we did:

* `sudo apt-get install libapache2-mod-wsgi-py3`
* `sudo ln -s [location of cloned repository]/webapp /var/www`
* Edit /etc/apache2/sites-available/default and add `WSGIScriptAlias / /var/www/test.py` above the `ScriptAlias /cgi/ /var/www/cgi` line

That should be it, assuming everything is set up correctly. Additionally, you will need to install bottle from easy_install for python 3:
```
$ sudo easy_install3 bottle
```
You will also need to install the quick2wire libraries, which you can do using the install script in the rpi/quick2wire-python-api folder of this repository.

Web Interface: Files
--------------------
The web interface contains the following files and folders of interest:
* index.py, dialogs/, and chkRefresh/ can all be ignored, as they're hold overs from the previous version of the web interface.
* test.py is the main file, where most of the processing happens and where everything is served from.
* js/ is the javascript file, where all of our javascript functions are.
* styles/ is the CSS file, which contains our styles and our fonts
* images/ is the images file, which contains the images that are displayed on the devices.
* layouts/ contains the templates, which is most of the actual HTML that is sent to the device. They use bottle's template language, which is a slight variation of generic python.
* quick2wire-python-api/ can be ignored, it's the version in the rpi/ directory that's important.
* giveAllResources.py writes 100 resources to everybody for debugging.
* getPlayerInfo.py reads and prints a specific player's info to the terminal.

Web Interface: TODO
-------------------
* Knight handling is about 50% complete
* 7 rolls still need to be handled.
* Ports have not yet been considered. Neither has bank trading. These can be done in the trading interface.

Web Interface: DISCLAIMER
-------------------------
This web interface is a senior design project, and as such is not in a complete form, it's basically a beta. It will likely not be worked on after the semester is over, either. We hold no liability to anything that may happen to you or your device as a result of using this web application, or anything relating to the Hackers of Catron, for that matter.

*Insert license here, assuming it is to be licensed.*
