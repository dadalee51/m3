'''
version 2.2a
The plan is to use esp m3 as a master to control the
two ATtiny 1616 mc, where:
at1 slave address: 0x12 (decimal value 18)
at2 slave address 0x14 (decimal value 20)
acccelerometer address is 0x19 LIS2DH12TR
multiplexor 0x70
color sensor: 0x
AT1 -
    Motor A/B
    RLED1, WLED1
    ENCODER_A/B/C
    TXD2/RXD2 (connected to m3 but no use) - this is improved by 2.25b
    RGB led.
AT2 -
    IRSensor SEN1/2/3
    LDR - SEN13/14
    Motor C/D
    RLED1, WLED1
    encoder:C/D
    Multiplexor
i2c address:
    Decimal address:  16  | Hexa address:  0x10 - color sensors
    Decimal address:  18  | Hexa address:  0x12 -AT1
    Decimal address:  20  | Hexa address:  0x14 -AT2
    Decimal address:  25  | Hexa address:  0x19 -accelerotmeter 
    Decimal address:  112  | Hexa address:  0x70 - multiplexor

'''
from machine import Pin, SoftI2C as I2C
from time import sleep, sleep_ms
import struct
from VEML6040 import VEML6040

#use a at2 as a bridge to read from LIS2DH12 sensor.
AT1 = 0x12
AT2 = 0x14
MUX = 0x70
ir1 = Pin(12, Pin.OUT)
ir2 = Pin(16, Pin.OUT)
ir1.off()
ir2.off()

i2c = I2C(scl=Pin(14), sda=Pin(4), freq=100000)

blueLED = Pin(2, Pin.OUT)
def startColorS1():
    i2c.writeto(MUX, b'\x01')
    return VEML6040()
def startColorS2():
    i2c.writeto(MUX, b'\x02')
    return VEML6040()
def readColorS1():
    i2c.writeto(MUX, b'\x01')
    return vsens1.readRGB()
def readColorS2():
    i2c.writeto(MUX, b'\x02')
    return vsens2.readRGB()
def getByteFromDecList(v1,v2,v3):
    return bytes([v1,v2,v3])

def amp(r,g,b):
    if r>g and r>b:
        return r,0,0
    elif g>r and g>b:
        return 0,g,0
    elif b>r and b>g:
        return 0,0,b
    else:
        return 0,0,0
#toMotor('MA', -1, 120)
#toMotor('MD',  1, 120)
'''
    motorNmae is either in MA/MB/MC/MD
    direction: 1-pos/-1=neg/0=coast/2=break/10 full/11 neg full.
'''
def toMotor(motorName, direction, power):
    inp = struct.pack('>2sbB', motorName.encode(), direction, power)
    print(inp)
    if motorName in ['MA','MB']:
        i2c.writeto(AT1, inp)
    elif motorName in ['MC','MD']:
        i2c.writeto(AT2, inp)

i2c.writeto(AT1, b'WL1A') #turn on WLED1 with A, off with B
i2c.writeto(AT2, b'WL2A') #turn on WLED2


vsens1 = startColorS1()
vsens2 = startColorS2()
ran = 4096
sml = 255

toMotor('MA', -1, 80)
toMotor('MD',  1, 100)
sleep(1)
toMotor('MA', 2, 0)
toMotor('MD', 2, 0)
sleep(1)
toMotor('MA', 1, 80)
toMotor('MD', -1, 100)
sleep(1)
toMotor('MA', 0, 0)
toMotor('MD', 0, 0)
while True:
    #use this line to send RGB value to AT1.
    #i2c.writeto(AT1, b'RGB\x00\xFF\xFF')
    argb1 = readColorS1()
    r1 = argb1['red'] *sml//ran
    g1 = argb1['green'] *sml//ran
    b1 = argb1['blue'] *sml//ran
    w1 = argb1['white'] *sml//ran
    argb2 = readColorS2()
    r2 = argb2['red'] *sml//ran
    g2 = argb2['green'] *sml//ran
    b2 = argb2['blue'] *sml//ran
    w2 = argb2['white'] *sml//ran
    r2,g2,b2=amp(r2,g2,b2)
    theList = getByteFromDecList(255-r2//20,255-g2//20,255-b2//20)
    i2c.writeto(AT1, b'RGB'+theList)
    #print(w1, w2)
    
    #print(theList)
    #blueLED.value(not blueLED.value())
    #data = i2c.readfrom(DEVICE_ADDR, 4)  # Read 4 bytes from the device
    #z_acceleration = struct.unpack('<f', data)[0]
    #print("Z Acceleration:", z_acceleration)
    #sleep(0.1)
    #then read from 0x14,
    #data = i2c.readfrom(0x12, 6)
    
    #print(data[0], data[1])
    #print('Num = {:08b} {:08b}'.format(data[0], data[1] ))
    #ans = struct.unpack('>hhh', data)
    
    #read from AT1, tof data
    #tofRaw = i2c.readfrom(AT1, 2)
    #tofData = struct.unpack('<h', tofRaw)[0]
    #print(tofData)
    
    #print(f"ans:{ans}")
    #wled.value(not wled.value())
    sleep(0.2)