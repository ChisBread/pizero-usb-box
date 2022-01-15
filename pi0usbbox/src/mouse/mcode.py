def char(n):
	if n > 127:
		n = 127
	if n < -128:
		n = -128
	return n & 0xff
def mcode(keys):
	report_mod = 0x08
	x = y = r = 0
	for k in keys:
		if k in mmod:
			report_mod = report_mod | mmod[k]
		elif len(k) > 4 and "xyr=" == k[:4]:
			x, y, r = [ int(i) for i in k[4:].split(',')]
		else:
			raise Exception("unknown opt %s"%k)
	return bytearray([report_mod, char(x), char(y), char(r)])
mmod = {
	"MOUSE_LEFT":0x01,
	"MOUSE_RIGHT":0x02,
	"MOUSE_MIDDLE":0x04,
	"MOUSE_L":0x01,
	"MOUSE_R":0x02,
	"MOUSE_M":0x04,
}
if __name__ == "__main__":
	import sys
	keys = sys.argv[4:] if len(sys.argv) > 4 else []
	print(mcode(keys, int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])))