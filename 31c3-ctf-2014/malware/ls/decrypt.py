from salsa20 import XSalsa20_xor, Salsa20_xor
from evdev import uinput, ecodes as e
import string
import struct

def split(line, n):
	return [line[i:i+n] for i in range(0, len(line), n)]

# First packet after the tcp handshake in the pcap contains the key:
key = "4fca2a2f553b08362466bd8589a0d7d92307ccb6500e6ed07d95bf95b40bff36".decode("hex")

# the file data contains the event data extracted from the pcap
# I extracted this data using tshark:
# tshark -r ls_dec.pcap -T fields -e data -Y "ip.dst==188.40.18.94&&ip.len>70" > data
data = open("data").read().strip()
data = string.replace(data, "\n", "")
data = split(data, 24*2)

events = []

# Decrypt each event with the key and increasing nonce (iv)
for i in range(0, len(data)):
	d = data[i].decode("hex")
	iv = struct.pack("l", i)
	#print iv
	event = Salsa20_xor(d, iv, key)
	#event = event.encode("hex")
	events.append(event)

#struct input_event {
#struct timeval time; 2*8 bytes
#__u16 type;  2 byte
#__u16 code;  2 byte
#__s32 value; 4 byte
#};

# Parse struct and replay it
# Note: in order to make the replaying work the script might have to be ran as root
with uinput.UInput() as ui:
	for l in events:
		event = struct.unpack("qqHHi", l) # parse struct
		event_type = event[2]
		event_code = event[3]
		event_value = event[4]
		if event_type == e.EV_KEY:
			ui.write(event_type, event_code, event_value)
	ui.syn()
