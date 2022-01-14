import sys
import socket
from keycode import keycode
from functools import reduce
HIDT_KEY = bytearray([0x1])
HIDT_MMKEY = bytearray([0x2])
HIDT_SYSCTRL = bytearray([0x3])
HIDT_JOY = bytearray([0x4])
HIDT_MOUSE = bytearray([0x5])
HIDT_ABSMOUSE = bytearray([0x6])
HEAD_CODE = bytearray([0x2c])
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def report_code(keys):
    code = keycode(*keys, 8)
    vcbytes = bytearray([reduce(lambda x, y: x+y, code)+1])
    codelen = bytearray([len(code)%256])
    code = HEAD_CODE+codelen+vcbytes+HIDT_KEY+code
    return bytes(code)

def report(keys, dev='192.168.1.178:9000'):
    ip, port = dev.split(':')
    addr = (ip, int(port))
    client_socket.sendto(keys, addr)

def check(dev='192.168.1.178:9000'):
    ip, port = dev.split(':')
    addr = (ip, int(port))
    client_socket.sendto(b'AT+STAINFO', addr)
    data, addr = client_socket.recvfrom(1024)
    if data:
        print("connected: "+data.decode())
        return True
    return False

if __name__ == '__main__':
    print(check())

