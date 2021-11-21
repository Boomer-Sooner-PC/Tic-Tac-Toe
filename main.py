import serial
import time
import sys
import glob
from gcode import writeBoard, drawSymbol, gcode, drawWinLine
from ai import *
from camera import *


def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


print(serial_ports())

port = input("Which of these serial ports is the machine? \n > ")
cam = input("Which camera is connected to the machine? \n > ")
cam = int(cam)

ser = serial.Serial(port, 115200)
time.sleep(2)
writeBoard(ser)
time.sleep(1)
takePicture("1", cam)


player = 'O'
bot = 'X'
win = False
while not win:
    botMove = compMove()
    drawSymbol(botMove, "X", ser)
    takePicture("1", cam)
    devide("processed.jpg", 1)

    win = checkForWin()
    if win:
        drawWinLine(win, ser)
    if not win:
        input("done with move")
        takePicture(2, cam)
        devide("processed.jpg", "2")
        move = calculate()
        playerMove(move)
        print(move)


ser.close()
