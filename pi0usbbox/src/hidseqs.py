import sys
import time
import re
import keyboard.dev_gadget, keyboard.dev_udp
import mouse.dev_gadget
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
def seqs(args, report=general_report):
    dev = ''
    keys_buffer = []
    is_mouse = False
    def report_keys(holdms=0):
        nonlocal keys_buffer, dev, is_mouse
        if not dev:
            sys.stderr.write('has not device\n')
            return False
        sys.stderr.write('report %s to %s hold %sms\n'%(keys_buffer, dev, holdms))
        report(keys_buffer, dev, is_mouse)
        if holdms > 0:
            time.sleep(holdms/1000)
        report([], dev, is_mouse)
        keys_buffer = []
    for arg in args:
        if (len(arg) > 4 and 'xyr=' == arg[:4]) or ('MOUSE_' in arg):
            # 监测到鼠标操作, 将设备标记为鼠标
            is_mouse = True
        if len(arg) > 2 and 'd=' == arg[:2]:
            # 新设备,清空缓冲区
            if keys_buffer:
                report_keys()
            dev = arg[2:]
            is_mouse = False
        elif len(arg) > 2 and 'h=' == arg[:2]:
            # hold指令,清空缓冲区
            try:
                holdms = int(arg[2:])
            except:
                sys.stderr.write('h= int required\n')
            report_keys(holdms)
        elif len(arg) > 2 and 'w=' == arg[:2]:
            # delay
            try:
                waitms = int(arg[2:])
            except:
                sys.stderr.write('%s\n'%'wait= int required')
            sys.stderr.write('wait %sms\n'%waitms)
            time.sleep(waitms/1000)
        else:
            keys_buffer.append(arg)
    if keys_buffer:
        report_keys()

def stdin_iter():
    for line in sys.stdin:
        for tok in line.strip('\n').split(' '):
            yield tok
if __name__ == '__main__':
    seqs(stdin_iter())
