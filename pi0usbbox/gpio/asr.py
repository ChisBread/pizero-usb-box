import smbus
import time
# global
bus = smbus.SMBus(1)
i2c_addr = 0x0f   #语音识别模块地址
asr_add_word_addr  = 0x01   #词条添加地址
asr_mode_addr  = 0x02   #识别模式设置地址，值为0-2，0:循环识别模式 1:口令模式 ,2:按键模式，默认为循环检测
asr_rgb_addr = 0x03   			#RGB灯设置地址,需要发两位，第一个直接为灯号1：蓝 2:红 3：绿 ,
                                #第二个字节为亮度0-255，数值越大亮度越高
asr_rec_gain_addr  = 0x04    #识别灵敏度设置地址，灵敏度可设置为0x00-0x55，值越高越容易检测但是越容易误判，
                             #建议设置值为0x40-0x55,默认值为0x40                              
asr_clear_addr = 0x05   #清除掉电缓存操作地址，录入信息前均要清除下缓存区信息
asr_key_flag = 0x06  #用于按键模式下，设置启动识别模式
asr_voice_flag = 0x07   #用于设置是否开启识别结果提示音
asr_result = 0x08  #识别结果存放地址
asr_buzzer = 0x09  #蜂鸣器控制寄存器，1位开，0位关
asr_num_cleck = 0x0a #录入词条数目校验
asr_vession = 0x0b #固件版本号
asr_busy = 0x0c #忙闲标志

def add_words(idnum,str):
	global i2c_addr
	global asr_add_word_addr
	words = []
	words.append(asr_add_word_addr)
	words.append(len(str) + 2)
	words.append(idnum)
	for  alond_word in str:
		words.append(ord(alond_word))
	words.append(0)	
	print(words)
	for date in words:
		bus.write_byte (i2c_addr, date)
		time.sleep(0.03)

def set_rgb(R,G,B):
	global i2c_addr
	global asr_rgb_addr
	date = []
	date.append(R)
	date.append(G)
	date.append(B)

	print(date)
	bus.write_i2c_block_data (i2c_addr,asr_rgb_addr,date)

def i2c_read_byte(reg):
	global i2c_addr
	bus.write_byte (i2c_addr, reg)
	time.sleep(0.05)
	Read_result = bus.read_byte (i2c_addr)
	return Read_result

def busy_wait():
	busy = 255
	while busy != 0:
		busy = i2c_read_byte(asr_busy)
		print(asr_busy)	

'''
模式和词组具有掉电保存功能，第一次录入后续如果没有修改可以将1置位0不折行录入词条和模式
'''
def init_words(key, words, mod=1):
	words = [key,"hong deng","lv deng","lan deng","guan deng"]+words
	bus.write_byte_data(i2c_addr, asr_clear_addr, 0x40)#清除掉电缓存区
	busy_wait()				#等待模块空闲
	print("缓存区清除完毕")
	#mod=1 口令模式 0 循环模式
	bus.write_byte_data(i2c_addr, asr_mode_addr, mod)
	busy_wait()				#等待模块空闲	
	print("模式设置完毕完毕")
	for num, word in enumerate(words):
		add_words(num, word)
		busy_wait()				#等待模块空闲
	cleck = 0
	while cleck != len(words):
		cleck = i2c_read_byte(asr_num_cleck)
		print(cleck)	
	bus.write_byte_data(i2c_addr, asr_rec_gain_addr, 0x41)#设置灵敏度，建议值为0x40-0x55
	bus.write_byte_data(i2c_addr, asr_voice_flag, 1)#设置开关提示音
	bus.write_byte_data(i2c_addr, asr_buzzer, 1)#蜂鸣器
	set_rgb(255,255,255)
	time.sleep(1)
	set_rgb(0,0,0)
	bus.write_byte_data(i2c_addr, asr_buzzer, 0)#蜂鸣器

def read_byte():
	r = i2c_read_byte(asr_result)
	return r - 5 if r >= 5 else 255
if __name__ == "__main__":
	init_words('ke ji', ['kai ji'])
	while True:
		print(i2c_read_byte(asr_result))
		time.sleep(0.5)
