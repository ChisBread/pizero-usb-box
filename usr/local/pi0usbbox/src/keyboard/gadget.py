import sys,re
from keycode import keycode

def report(keys, dev='/dev/hidg0'):
    with open(dev, 'rb+') as fd:
        fd.write(keycode(keys))
if __name__ == '__main__':
    print(report(['a']))
    print(report([]))

