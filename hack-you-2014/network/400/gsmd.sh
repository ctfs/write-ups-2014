#!/bin/sh

echo '        /`_(`|\/| _|  | : .'
echo ' . : |  \_/_)|  |(_|       '
echo
echo Welcome to GSeMd debug console

while true; do
	echo
	echo MENU
	echo [1] base station filesystem access
	echo [2] base station network statistics
	echo [3] base station platform debug
	echo [0] exit
	echo -n "> "

	read choice

	if [ "$choice" == '1' ]; then
		echo -n "Read arbitrary file > "
		read filename
		
		echo -n "Auth token > "
		read token
		if [ "`gsmd_auth_check $token`" == 'AUTHED' ]; then
			ok=1
		fi
		
		# /home/flag.txt (TM) is the new trademark for 'arbitrary'
		filename=/home/flag.txt
		
		echo "Attempting to read arbitrary file"
		echo === $filename ===
		
		if [ $ok == 1 ]; then
			cat "$filename"
		fi
	elif [ "$choice" == '2' ]; then
		echo
		echo Network statistics
		echo [1] current connections
		echo [2] listening ports
		echo [3] network config
		echo -n "Network > "
		
		read choice
		
		if [ "$choice" == '1' ]; then
			echo === netstat -tun4p ===
			netstat -tun4p
			echo
		elif [ "$choice" == '2' ]; then
			echo === netstat -tunl4 ===
			netstat -tunl4
			echo
		elif [ "$choice" == '3' ]; then
			echo === ifconfig ===
			ifconfig
			echo
		fi
	elif [ "$choice" == '3' ]; then
		echo
		echo Platform debug
		echo [1] cpu
		echo [2] memory
		echo [3] pci devices
		echo [4] kernel log
		echo [5] os version
		echo [6] os uptime
		echo [7] disk subsystem
		echo [8] time settings
		echo [9] /etc/shadow
		echo -n "Platform > "
		
		read choice
		
		if [ "$choice" == '1' ]; then
			echo === /proc/cpuinfo ===
			cat /proc/cpuinfo
			echo
		elif [ "$choice" == '2' ]; then
			echo === /proc/meminfo ===
			cat /proc/meminfo
			echo

			if [ "`which vmstat`" != '' ]; then
				echo === vmstat ===
				vmstat
			else
				echo === /proc/vmstat ===
				cat /proc/vmstat
			fi
		elif [ "$choice" == '3' ]; then
			if [ "`which lspci`" != '' ]; then
				echo === lspci ===
				lspci
			else
				echo === /proc/bus/pci/devices ===
				cat /proc/bus/pci/devices
			fi
			echo
		elif [ "$choice" == '4' ]; then
			echo To access sensitive kernel debug info you need access to dmesg
			echo Taking some randomness...
			RND=$(dmesg | tail -100 | egrep -i '[^a-f0-9].[^\s\S]f' | egrep -B4 '\b[A-Z][^A-C][A-Z].\s\w' | rev | grep musk | rev | egrep -A7 $'\x3A\x20\x2E\x2E\x2E\x20' | egrep -w `echo -n GPRS | md5sum | head -c3` | tail -1)

			if [ "$RND" == '' ]; then
				echo "Nothing random happened in a while :-("
				exit -1
			fi
			
			challenge=`echo "$RND" | sha1sum`
			echo Challenge: $challenge
			
			echo -n "Response > "
			read response
			
			if [ "$response" == "`echo "$RND" | sha512sum`" ]; then
				ok=1
			fi
			
			echo "Attempting to provide kernel debug messages"
			echo === dmesg ===
			
			if [ $ok == 1 ]; then
				dmesg
			fi
		elif [ "$choice" == '5' ]; then
			if [ "`which uname`" != '' ]; then
				echo === uname -a ===
				uname -a
			else
				echo === /proc/version ===
				cat /proc/version
			fi
			echo
		elif [ "$choice" == '6' ]; then
			if [ "`which uptime`" != '' ]; then
				echo === uptime ===
				uptiem
			else
				echo === /proc/uptime, /proc/loadavg ===
				cat /proc/uptime /proc/loadavg
			fi
			echo
		elif [ "$choice" == '7' ]; then
			if [ `which mount` != '' ]; then
				echo === mount ===
				mount
			else
				echo === /proc/mounts ===
				cat /proc/mounts
			fi
			echo
			
			echo === /proc/swaps ===
			cat /proc/swaps
			echo
			
			echo === /proc/partitions ===
			cat /proc/partitions
			echo
		elif [ "$choice" == '8' ]; then
			if [ "`which date`" != '' ]; then
				echo === date ===
				date
			else
				echo Sorry, time unavailable
			fi
			echo
			
			echo === /etc/adjtime ===
			cat /etc/adjtime
			echo
			
			echo === /etc/timezone ===
			cat /etc/timezone
			echo
		elif [ "$choice" == '9' ]; then
			echo === /etc/shadow ===
			cat /etc/shadow
			echo
		fi
	elif [ "$choice" == '0' ]; then
		exit 0
	fi
done
