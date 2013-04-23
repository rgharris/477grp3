The Hackers of Catron
=====================

* Author:			Team Hex Me, Baby! ([group webpage](https://engineering.purdue.edu/477grp3/))
* Date:				Spring Semester, 2013
* Version:			0.1.0
* Github:			<https://github.com/rgharris/477grp3>

The Hackers of Catron is an electronic version of the popular board game, [The Settlers of Catan](http://www.catan.com). The Settlers of Catan is a resource trading game, with the object of having the largest settlement on the island of catan. This repository contains all the code for Purdue University's ECE 477 Senior Design Spring 2013 Team 3's project.

You can see the status and development on our team webpage. We developed the entire project from scratch, starting with sourcing parts and designing a (fairly large) Printed Circuit Board. The board contains the microcontroller, RGB LEDs to show resources, 7 Segment Displays to show the rarity of each resource, and hall effect sensors to read magnets that are attached to the bottom of each piece, along with various drivers, multiplexers, and the like to make it all work together nicely. Additionally, the microcontroller is attached to a Raspberry Pi via I2C. The Raspberry Pi has a USB Wifi adapter attached to it and runs an access point. When connected to the access point, you are able to access a web interface.

Repository Structure
--------------------

The repository is designed to seperate out the sections so that it's easier for us to work concurrently instead of stepping over each other with commits. To assist with that goal, the repository was seperated into three distinct folders:

* webapp
  * This folder contains the web application that runs on the Raspberry Pi.
* rpi
  * This folder contains the Raspberry Pi's bootup script, a debugging function, and the quick2wire libraries.
* micro
  * This folder contains the code that runs on the microcontroller on the main game board.

Each folder has it's own README that we recommend you read to get the full idea of what's going on. Particularly for the Raspberry Pi, as it has some installation steps that need to be handled before it can be used.

TODO
----

At this point the main project has been completed and we're squashing bugs as we come across them. Additionally we're doing some things required by the Senior Design class - final reports, a user manual, a video, etc., all of which will be available on the website.

DISCLAIMER
----------

As has been mentioned several times, this is a senior design project, and as such is never going to leave an early beta state, practically an alpha state. After the 2013 spring semester is over, it will probably not be worked on by Team Hex Me Baby again. We hold no liability to anything that may happen to you or anything you own as a result of using the Hackers of Catron or any part in any way. 
