# pizero-usb-box

- 使你的Raspberry Pi Zero 2 W成为便携多功能USB工具箱!
- 提供一些好玩的小功能, 快让你的朋友大吃一惊吧!

## 特性
同时模拟多种设备，未来会针对每种设备开发功能齐全（花里胡哨）的工具
1. HID设备支持, 可模拟键盘、鼠标，操作主机
2. Ethernet设备支持, 可共享主机与Raspberry Pi Zero 2 W之间的网络
3. Mass Storage设备支持, 可作为U盘, 并在主机与Raspberry Pi Zero 2 W之间进行数据交换
4. Serial支持，支持与Raspberry Pi Zero 2 W进行串口通信
5. 蓝牙近场识别, 支持macOS的自动锁屏和解锁
## 演示
浏览器操作
![mygithub](https://github.com/ChisBread/pizero-usb-box/raw/master/resource/mygithub.gif)
终端操作
![thisismine](https://github.com/ChisBread/pizero-usb-box/raw/master/resource/thisismine.gif)
## 安装和测试
1. 安装
```bash
## 支持自定义设置. 比如MAC地址等；部分设置需要在安装前修改完毕
# vim usr/local/pi0usbbox/confenv
## 蓝牙相关命令需要安装
# sudo apt install bluetooth bluez libbluetooth-dev
# sudo pip install pybluez
./install
```
## 使用说明
### HID 键鼠模拟工具
更多HID命令，查看[hid-tutorial](./docs/hid-tutorial.md)
```bash
# 交互式键鼠模拟
# 执行后自动转发终端操作
hid-keyboard
hid-mouse
```
### Network 自动设置工具
使用HID模拟操作设置网络，以访问Raspberry Pi Zero 2 W
```bash
# 暂时只支持 macOS
/usr/local/pi0usbbox/hostinit
```
### Mass Storage U盘重载
不知道是不是我操作有问题，需要重载才可以看到USB-Host写入的新数据
```bash
usbdisk-remount
```
### Blueguard 蓝牙近场锁屏/解锁
锁屏功能为防badusb专用(但防不了Pi直接被拔走)
```bash
# 填好手机蓝牙地址(密码注意保护, 不填密码为单锁屏模式)
# 注意: 不同环境的蓝牙测距效果不一, 请根据实际情况调整
nohup blueguard ${DEVICE_ADDR} ${PASSWORD} 2>&1 > /tmp/unlock.log
```
## Hacking Demo
提供一些实现好的注入demo
- [macos-hacking](./docs/macos-hacking.md)
## TODO
1. 基于pyautogui实现Host侧的daemon, 方便进行自动化操作
## 感谢
- [COMPOSITE USB GADGETS ON THE RASPBERRY Raspberry Pi Zero 2 W - isticktoit.net](http://www.isticktoit.net/?p=1383)
- [pizero-usb-hid-keyboard](https://github.com/raspberrypisig/pizero-usb-hid-keyboard)
- [usbarmory wiki](https://github.com/ckuethe/usbarmory/wiki/USB-Gadgets)
