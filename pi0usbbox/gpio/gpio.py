#coding:utf-8
import os
import sys
sys.path.append('/usr/local/pi0usbbox/pi0hid')
import pi0hid
import asr, ssd1306
import time
tasks = [
    ('la ji','lock',['d=/dev/hidg0', 'ctrl', 'meta', 'q']),
    ('li hai','unlock',['d=/dev/hidg0', 'p=chisbread', 'enter']),
    ('zuo hua','left',['d=/dev/hidg0', 'ctrl', 'left']),
    ('you hua','right',['d=/dev/hidg0', 'ctrl', 'right']),
]
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'init':
        asr.init_words('da gong', [ w for w,d,c in tasks], 0)
    disp_cnt = 0
    disp_desc = disp_cmd = ''
    while True:
        idx = asr.read_byte()
        print(idx)
        word, desc, cmd = tasks[idx] if idx < len(tasks) else ('','','')
        if word:
            pi0hid.seqs(cmd)
            disp_cnt = 10
            disp_desc = desc
            disp_cmd = ' '.join(cmd[1:])
        if disp_cnt > 0:
            disp_cnt -= 1
        else:
            disp_desc = disp_cmd = ''
        ssd1306.display_all(disp_desc, disp_cmd)
        time.sleep(0.05)