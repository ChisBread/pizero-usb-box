# pizero-usb-box hid-keyboard 使用说明

## 命令文档
### keyboard
- hid-keyboard
    - 交互式命令,执行后进入交互模式; 任何可被转发的键盘操作都会转发到USB-Host上
    - CTRL+P 进入Print模式, 适合一次输入大段文本
    - CTRL+R 进入Raw模式, 适合进行快捷键操作(如Win+R打开cmd等)
- hid-print ${string}
    - 向USB-Host输出一段文本
- hid-printfile ${file}
    - 向USB-Host输出一个文件
- hid-sendkeys ${keyname}
    - 向USB-Host输出一个键盘操作
## mouse
- hid-movepointer xyr=${x},${y},${r}
    - 移动光标位置