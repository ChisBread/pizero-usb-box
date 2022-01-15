import sys,re
from mouse.mcode import mcode

def report(keys, dev='/dev/hidg1'):
    with open(dev, 'rb+') as fd:
        fd.write(mcode(keys))
if __name__ == '__main__':
    keys = sys.argv[4:] if len(sys.argv) > 4 else []
    print(report(sys.argv[1:]))

