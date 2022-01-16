def lexer(reader):
    buffer = []
    escape = False
    def tok():
        nonlocal buffer
        ret = ''.join(buffer)
        buffer = []
        return ret
    for ch in reader:
        if escape:
            buffer.append(ch)
            escape = False
        elif ch in ['\n', ' ']:
            if buffer:
                yield tok()
        elif ch == '\\':
            escape = True
        else:
            buffer.append(ch)
    if buffer:
        yield tok()
import sys
def stdin_iter():
    for line in sys.stdin:
        for c in line:
            yield c
def str_iter(s):
    for c in s:
        yield c
def file_iter(filename):
    with open(filename, 'r') as f:
        while True:
            # read next character
            char = f.read(1)
            # if not EOF, then at least 1 character was read, and 
            # this is not empty
            if char:
                yield char
            else:
                return
if __name__ == "__main__":
    for tok in lexer(stdin_iter()):
        print("'%s'"%tok)