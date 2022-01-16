import sys
import time
import re
from lexer import *
import ducky 
import keyboard.dev_gadget, keyboard.dev_udp
import mouse.dev_gadget
debug = False
def general_report(keys, dev, is_mouse=False):
    devclass = keyboard
    if is_mouse:
        devclass=mouse
    if '/dev/hidg' in dev:
            devclass.dev_gadget.report(keys, dev)
    elif re.match(r'[\d\.]+:\d+', dev):
        devclass.dev_udp.report(keys, dev)
    elif dev == 'std':
        print(keys)
    else:
        sys.stderr.write('error device\n')

def seqs(args, report = general_report, default_wait = 0):
    dev = ''
    keys_buffer = []
    is_mouse = False
    def report_keys(holdms=0):
        nonlocal keys_buffer, dev, is_mouse, default_wait
        if not dev:
            sys.stderr.write('has not device\n')
            return False
        if debug:
            sys.stderr.write('report %s to %s hold %sms\n'%(keys_buffer, dev, holdms))
        report(keys_buffer, dev, is_mouse)
        if holdms > 0:
            time.sleep(holdms/1000)
        # 不上报非点击动作
        if is_mouse and len(keys_buffer) == 1 and 'xyr=' in keys_buffer[0]:
            pass
        else:
            report([], dev, is_mouse)
        if default_wait > 0:
            time.sleep(default_wait/1000)
        keys_buffer = []
    last_arg = ''
    last_dev = ''
    for arg in args:
        if arg.startswith("xyr=") or ('MOUSE_' in arg):
            # 监测到鼠标操作, 将设备标记为鼠标
            is_mouse = True
        if arg.startswith("d="):
            # 新设备,清空缓冲区
            if keys_buffer:
                report_keys()
            last_dev = dev
            dev = arg[2:]
            if not last_dev:
                last_dev = dev
            is_mouse = False
        elif arg.startswith("r="):
            repeat = int(arg[2:])
            if repeat > 1 or last_arg:
                args = ['d='+last_dev]+[last_arg]*(repeat-1)
                seqs(args, general_report, default_wait)
        elif arg.startswith("h="):
            # hold指令,清空缓冲区
            try:
                holdms = int(arg[2:])
            except:
                sys.stderr.write('h= int required\n')
            if keys_buffer:
                report_keys(holdms)
        elif arg.startswith("w="):
            # delay
            try:
                waitms = int(arg[2:])
            except:
                sys.stderr.write('%s\n'%'wait= int required')
            if debug:
                sys.stderr.write('wait %sms\n'%waitms)
            time.sleep(waitms/1000)
        elif arg.startswith("dw="):
            # default_wait
            try:
                default_wait = int(arg[3:])
            except:
                sys.stderr.write('%s\n'%'default_wait= int required')
            if debug:
                sys.stderr.write('default_wait %sms\n'%waitms)
        elif arg.startswith("p="):
            if keys_buffer:
                report_keys()
            tmp = default_wait
            default_wait = 0
            for c in arg[2:]:
                keys_buffer.append(c)
                report_keys()
            default_wait = tmp
            time.sleep(default_wait/1000)
        elif arg.startswith("f="):
            if keys_buffer:
                report_keys()
            for c in file_iter(arg[2:]):
                keys_buffer.append(c)
                report_keys()
        else:
            keys_buffer.append(arg)
        if not arg.startswith('h=') and not arg.startswith('d=') and not arg.startswith('dw='):
            last_arg = arg
    if keys_buffer:
        report_keys()

if __name__ == '__main__':
    data_in = ''
    if len(sys.argv) > 1:
        if sys.argv[1] == '-i':
            seqs(lexer(stdin_iter()))
        elif sys.argv[1] == '-s':
            seqs(lexer(str_iter(' '.join(sys.argv[2:]))))
        elif sys.argv[1] == '--ducky':
            with open(sys.argv[2], 'r') as f:
                for tok in ducky.compile(f):
                    if tok.startswith('h=') or tok.startswith('p=') or tok.startswith('w=') or tok.startswith('dw='):
                        sys.stdout.write(tok+'\n')
                    else:
                        sys.stdout.write(tok+' ')
        else:
            seqs(lexer(file_iter(sys.argv[1])))

    
