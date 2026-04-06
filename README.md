```
IPGrab v1.13 - IPv4 Grabber

Reads text or binary data from standard input, extracts valid IPv4 addresses
and networks, and outputs them in order of appearance.

By default, outputs both individual IPs and networks.

INPUT FORMAT:
  192.168.1.1                # Single IP address
  192.168.1.0/24             # Network with CIDR prefix
  192.168.1.0/255.255.255.0  # Network with subnet mask

OUTPUT FORMAT:
  192.168.1.1
  192.168.1.0/24
  192.168.1.0/24

USAGE:
  cat file | ipgrab [options]
  ipgrab [options] < file > file.lst

OPTIONS:
  -i|--ip-only     Output only individual IP addresses
  -n|--net-only    Output only networks
  -l|--lan-only    Output only private (LAN) addresses and networks
  -w|--wan-only    Output only public (WAN) addresses and networks
```
