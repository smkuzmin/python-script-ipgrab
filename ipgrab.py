#!/usr/bin/env python3

r"""
IPGrab v1.9 - IPv4 Grabber

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
"""

import sys
import re
import ipaddress

def main():
    # Парсим аргументы командной строки
    mode = 'both'  # режим по умолчанию - и IP и сети
    args = sys.argv[1:]

    for arg in args:
        if arg in ('-i', '--ip-only'):
            mode = 'ip'
        elif arg in ('-n', '--net-only'):
            mode = 'net'
        elif arg in ('-h', '--help'):
            print(__doc__)
            sys.exit(0)

    try:
        input_data = sys.stdin.buffer.read()
    except Exception:
        return

    result = []
    pattern = rb'\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})?\b'
    matches = re.findall(pattern, input_data)

    for match in matches:
        try:
            decoded = match.decode('ascii')
            if '/' in decoded:
                # Это сеть с маской или префиксом
                net_obj = ipaddress.ip_network(decoded, strict=False)
                if isinstance(net_obj, ipaddress.IPv4Network):
                    if mode in ('both', 'net'):
                        result.append(str(net_obj))
            else:
                # Это одиночный IP
                ip_obj = ipaddress.ip_address(decoded)
                if isinstance(ip_obj, ipaddress.IPv4Address):
                    if mode in ('both', 'ip'):
                        result.append(str(ip_obj))
        except (ValueError, UnicodeDecodeError):
            continue

    if not result:
        return

    # Выводим в порядке появления в исходном файле
    for item in result:
        print(item)

if __name__ == '__main__':
    # Показываем справку при вызове с -h или --help, или если запущен без перенаправления ввода
    if sys.stdin.isatty() or '-h' in sys.argv or '--help' in sys.argv:
        print(__doc__, file=sys.stderr)
        sys.exit(0)

    # Обрабатываем прерывание без вывода ошибки
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
