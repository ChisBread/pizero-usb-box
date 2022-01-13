import socket
import sys
from keycode import *
from functools import reduce
HIDT_KEY = bytearray([0x1])
HIDT_MMKEY = bytearray([0x2])
HIDT_SYSCTRL = bytearray([0x3])
HIDT_JOY = bytearray([0x4])
HIDT_MOUSE = bytearray([0x5])
HIDT_ABSMOUSE = bytearray([0x6])
HEAD_CODE = bytearray([0x2c])
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("192.168.1.178", 9000)
client_socket.sendto(b'AT+STAINFO', server_address)
data, addr = client_socket.recvfrom(1024)
if data:
    print("connected: "+data.decode())
def wifi_genkeycode(*keys):
    code = genkeycode(*keys)
    if len(code) < 8:
        code += bytearray([0x00]*(8-len(code)))
    if len(code) > 8:
        code = code[:8]
    vcbytes = bytearray([reduce(lambda x, y: x+y, code)+1])
    codelen = bytearray([len(code)%256])
    code = HEAD_CODE+codelen+vcbytes+HIDT_KEY+code
    return bytes(code)
def main():
    client_socket.sendto(wifi_genkeycode(*sys.argv[1:]), server_address)
    client_socket.sendto(wifi_genkeycode(), server_address)
if __name__ == '__main__':
    main()
    