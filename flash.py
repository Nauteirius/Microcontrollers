from machine import Pin, SPI
from time import sleep
import os
import time



from micropython import const
import framebuf


din = Pin(3, Pin.OUT)
cs = Pin(5, Pin.OUT)
clk = Pin(2, Pin.OUT)

spi = SPI(0, mosi=din, sck=clk, baudrate=10000000)


_NOOP = const(0)
_DIGIT0 = const(1)
_DECODEMODE = const(9)
_INTENSITY = const(10)
_SCANLIMIT = const(11)
_SHUTDOWN = const(12)
_DISPLAYTEST = const(15)
class Matrix8x8:
    def __init__(self, spi, cs, num):
        """
        Driver for cascading MAX7219 8x8 LED matrices.
        >>> import max7219
        >>> from machine import Pin, SPI
        >>> spi = SPI(1)
        >>> display = max7219.Matrix8x8(spi, Pin('X5'), 4)
        >>> display.text('1234',0,0,1)
        >>> display.show()
        """
        self.spi = spi
        self.cs = cs
        self.cs.init(cs.OUT, True)
        self.buffer = bytearray(8 * num)
        self.num = num
        fb = framebuf.FrameBuffer(self.buffer, 8 * num, 8, framebuf.MONO_HLSB)
        self.framebuf = fb
        # Provide methods for accessing FrameBuffer graphics primitives. This is a workround
        # because inheritance from a native class is currently unsupported.
        # http://docs.micropython.org/en/latest/pyboard/library/framebuf.html
        self.fill = fb.fill  # (col)
        self.pixel = fb.pixel # (x, y[, c])
        self.hline = fb.hline  # (x, y, w, col)
        self.vline = fb.vline  # (x, y, h, col)
        self.line = fb.line  # (x1, y1, x2, y2, col)
        self.rect = fb.rect  # (x, y, w, h, col)
        self.fill_rect = fb.fill_rect  # (x, y, w, h, col)
        self.text = fb.text  # (string, x, y, col=1)
        self.scroll = fb.scroll  # (dx, dy)
        self.blit = fb.blit  # (fbuf, x, y[, key])
        self.init()

    def _write(self, command, data):
        self.cs(0)
        for m in range(self.num):
            self.spi.write(bytearray([command, data]))
        self.cs(1)

    def init(self):
        for command, data in (
            (_SHUTDOWN, 0),
            (_DISPLAYTEST, 0),
            (_SCANLIMIT, 7),
            (_DECODEMODE, 0),
            (_SHUTDOWN, 1),
        ):
            self._write(command, data)

    def brightness(self, value):
        if not 0 <= value <= 15:
            raise ValueError("Brightness out of range")
        self._write(_INTENSITY, value)

    def show(self):
        for y in range(8):
            self.cs(0)
            for m in range(self.num):
                self.spi.write(bytearray([_DIGIT0 + y, self.buffer[(y * self.num) + m]]))
            self.cs(1)



pin = Pin("LED", Pin.OUT)
dioda = Pin(0, Pin.OUT)
button=Pin(28,Pin.IN,Pin.PULL_DOWN)
mov=Pin(16,Pin.IN,Pin.PULL_DOWN)
beep=Pin(4,Pin.OUT)
dioda.toggle()

def lever(initial_state):
    '''Pressing button will turn on/off dioda'''
    while(1):
        if(initial_state!=button.value()):
            temp=dioda.value()
            dioda.toggle()
            print("stan diody: ",temp," -> ",dioda.value())
            break
        sleep(1)
        
def movement_detection():
    '''Detect movement and turn on sound while it's see something'''
    current_state=0
    wykryto=0
    print("ok")
    start_time=time.time()*100
    while(1):
        if(time.time() - start_time>0.03):
            print("koniec dzilania beepa")
            start_time=time.time()*100
            beep.value(0)

        if mov.value()==1: 
            if(current_state==0):
                wykryto=wykryto+1
                print("wykryto ",wykryto," ruchów")
                start_time = time.time()
                beep.value(1)
                # pid=os.fork()
                # if(pid>0):
                #     beeper(pid)
                current_state=1      
        else: 
            current_state=0
            beep.value(0)

#def beeper():
    #beep.value(1)
#     sleep(1)
#     os.kill(pid)


dioda.value(0)
beep.value(0)
display = Matrix8x8(spi, cs, 1)


try:

    while True:
        display.brightness(1)
        display.fill(0)
        display.show()
        time.sleep(1)
        display.text('1',0,0,1)
        display.show()
        time.sleep(2)
        display.text('+',0,0,1)
        display.show()
        time.sleep(2)
        display.text('7',0,0,1)
        display.show()
        time.sleep(2)
        display.text('=',0,0,1)
        display.show()
        time.sleep(2)
        display.text('8',0,0,1)
        display.show()
        time.sleep(2)
        #pass
        #state = button.value()   
        #movement_detection()

        #lever(state)
        #sleep(0.5)
   
        
        # dioda.toggle()
        # pin.toggle()
        # sleep(1)

except InterruptedError:
        print("interrupted")

    
finally:
    print("end")