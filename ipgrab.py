#!/usr/bin/env python3

r"""
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
"""

import sys
import re
import ipaddress

def main():
    # Парсим аргументы командной строки
    ip_only = False
    net_only = False
    lan_only = False
    wan_only = False
    args = sys.argv[1:]

    for arg in args:
        if arg in ('-i', '--ip-only'):
            ip_only = True
        elif arg in ('-n', '--net-only'):
            net_only = True
        elif arg in ('-l', '--lan-only'):
            lan_only = True
        elif arg in ('-w', '--wan-only'):
            wan_only = True
        elif arg in ('-h', '--help'):
            print(__doc__, file=sys.stderr)
            sys.exit(0)
        else:
            print(f"Error: Invalid option: {arg}", file=sys.stderr)
            sys.exit(1)

    # Проверка на взаимоисключающие флаги
    if ip_only and net_only:
        print("Error: Options -i and -n are mutually exclusive", file=sys.stderr)
        sys.exit(1)
    if lan_only and wan_only:
        print("Error: Options -l and -w are mutually exclusive", file=sys.stderr)
        sys.exit(1)

    try:
        input_data = sys.stdin.buffer.read()
    except Exception:
        return

    result = []
    pattern = rb'\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2}|/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})?\b'
    matches = re.findall(pattern, input_data)

    for match in matches:
        try:
            decoded = match.decode('ascii')
            if '/' in decoded:
                # Это сеть с маской или префиксом
                # strict=True отклоняет сети с ненулевыми битами хоста (например, 8.8.8.5/24)
                net_obj = ipaddress.ip_network(decoded, strict=True)
                if isinstance(net_obj, ipaddress.IPv4Network):
                    if ip_only:
                        continue
                    if wan_only:
                        if not net_obj.is_global:
                            continue
                    if lan_only:
                        if net_obj.is_global:
                            continue
                    result.append(str(net_obj))
            else:
                # Это одиночный IP
                ip_obj = ipaddress.ip_address(decoded)
                if isinstance(ip_obj, ipaddress.IPv4Address):
                    if net_only:
                        continue
                    if wan_only:
                        if not ip_obj.is_global:
                            continue
                    if lan_only:
                        if ip_obj.is_global:
                            continue
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
