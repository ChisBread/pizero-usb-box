def get_latest_tok(line):
    tok = ''
    for s in line.split(' '):
        s.strip(' ')
        if not s:
            continue
        tok = s
    return tok
def compile(line_reader):
    hold = False
    for line in line_reader:
        line = line.strip('\n')
        if line.startswith("REM"):
            continue
        if line.startswith("REPEAT "):
            yield 'r=%d'%int(get_latest_tok(line))
        elif hold:
            yield 'h=0'
        hold = True
        if line.startswith("DEFAULT_DELAY ") or line.startswith("DEFAULTDELAY "):
            yield 'dw=%d'%int(get_latest_tok(line))
            line = ''
        elif line.startswith("DELAY "):
            yield 'w=%d'%int(get_latest_tok(line))
            line = ''
            hold = False
        elif line.startswith("STRING "):
            yield 'p=%s'%line[len("STRING "):].replace(' ', '\\ ')
            line = ''
            hold = False
        elif line.startswith("GUI ") or line.startswith("WINDOWS "):
            yield 'meta'
            line = line[len(line.split(' ')[0]):]
        elif line.startswith("MENU ") or line.startswith("APP "):
            yield 'PROPS'
            line = line[len(line.split(' ')[0]):]
        
        if not line:
            continue
        for tok in line.split(' '):
            tok.strip(' ')
            if not tok:
                continue
            tok = tok.upper()
            if tok.endswith("ARROW"):
                tok = tok[:len(tok)-len("ARROW")]
            yield tok

        