import sys
import time
import re
import wifi,gadget
def general_report(keys, dev):
    if '/dev/hidg' in dev:
        gadget.report(keys, dev)
    elif re.match(r'[\d\.]+:\d+', dev):
        wifi.report(keys, dev)
    elif dev == 'std':
        print(keys)
    else:
        sys.stderr.write('error device\n')
def seqs(args, report):
    keys = []
    dev = ''
    for arg in args:
        if len(arg) > 2 and 'd=' == arg[:2]:
            dev = arg[2:]
        elif len(arg) > 2 and 'h=' == arg[:2]:
            try:
                holdms = int(arg[2:])
            except:
                sys.stderr.write('%s\n'%'h= int required')

            if not dev:
                sys.stderr.write('%s\n'%'has not device')
                return False
            sys.stderr.write('report %s to %s hold %sms\n'%(keys, dev, holdms))
            report(keys, dev)
            if holdms > 0:
                time.sleep(holdms/1000)
            report([], dev)
            keys = []
        else:
            keys.append(arg)
    if keys:
        if not dev:
            sys.stderr.write('%s\n'%'has not device')
            return False
        sys.stderr.write('report %s to %s hold %sms\n'%(keys, dev, 0))

        report(keys, dev)
        report([], dev)

if __name__ == '__main__':
    seqs(sys.argv[1:], general_report)
