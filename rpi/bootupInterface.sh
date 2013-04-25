#/bin/bash
#This is a quick script to hopefully fix some bootup problems
#we are getting with the wireless adapter.

ps -A | grep udhcpd
while [ $? -ne 0 ]
do
	ifdown wlan0
	sleep 1
	ifup wlan0
	sleep 1
	service hostapd restart
	sleep 1
	service udhcpd restart
	sleep 1
	service dnsmasq restart
	sleep 1
	ps -A | grep udhcpd
done
echo "Restart of interface complete!"
