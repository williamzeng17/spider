# coding: utf-8
"""
版权所有，保留所有权利，非书面许可，不得用于任何商业场景
版权事宜请联系：WilliamZeng2017@outlook.com
"""

import socket
import socks
import urllib2

socks.set_default_proxy(socks.SOCKS5, 'localhost', 9150)
socket.socket = socks.socksocket
print urllib2.urlopen('http://icanhazip.com').read()
