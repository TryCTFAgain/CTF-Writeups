from scapy.all import sniff

pcap = sniff(offline='capture.pcapng')

for packet in pcap:
	# Ping to 192.168.11.5 not error
	# Type of ICMP message:
	## 0: icmp echo-reply
	## 8: icmp echo-request
	## 11: icmp time exceeded

	if packet['IP'].dst=='192.168.11.5' and packet['ICMP'].type == 8:
		print(chr(len(packet.load)), end='')
	
