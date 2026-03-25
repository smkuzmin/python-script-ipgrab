IPGrab v1.7 - IPv4 Grabber

Reads any file (text or binary) from STDIN, grabs valid IPv4 addresses
and networks, and outputs the list to STDOUT in order of appearance.

By default, grabs both IP addresses and networks.

INPUT FORMAT:
  192.168.1.1                # Single IP address
  192.168.1.0/24             # Network with CIDR prefix
  192.168.1.0/255.255.255.0  # Network with subnet mask

OUTPUT FORMAT:
  192.168.1.1
  192.168.1.0/24
  192.168.1.0/24

USAGE:
  cat file | ipgrab
  cat file | ipgrab --ip-only
  cat file | ipgrab --net-only
  cat file | ipgrab -i
  cat file | ipgrab -n
  ipgrab < file > file.lst
