import RPi.GPIO as GPIO
import time
import numpy as np 
import matplotlib.pyplot as plt
import math

GPIO.setwarnings (False)

GPIO.setmode (GPIO.BCM)
LEDS = [21, 20, 16, 12, 7, 8, 25, 24]
bit_depth = 8

DAC = [26, 19, 13, 6, 5, 11, 9, 10]

GPIO.setup (DAC[0], GPIO.OUT)
GPIO.setup (DAC[1], GPIO.OUT)
GPIO.setup (DAC[2], GPIO.OUT)
GPIO.setup (DAC[3], GPIO.OUT)
GPIO.setup (DAC[4], GPIO.OUT)
GPIO.setup (DAC[5], GPIO.OUT)
GPIO.setup (DAC[6], GPIO.OUT)
GPIO.setup (DAC[7], GPIO.OUT)

GPIO.setup (21, GPIO.OUT)
GPIO.setup (20, GPIO.OUT)
GPIO.setup (16, GPIO.OUT)
GPIO.setup (12, GPIO.OUT)
GPIO.setup (7,  GPIO.OUT)
GPIO.setup (8,  GPIO.OUT)
GPIO.setup (25, GPIO.OUT)
GPIO.setup (24, GPIO.OUT)

def turnAllas (format):
    for led in LEDS:
        GPIO.output (led, format)

def lightUp (ledNumber, period):
    GPIO.output (LEDS [ledNumber], 1)
    time.sleep (period)
    GPIO.output (LEDS [ledNumber], 0)

def lightDown (ledNumber, period):
    GPIO.output (LEDS [ledNumber], 0)
    time.sleep (period)
    GPIO.output (LEDS [ledNumber], 1)

def blink (ledNumber, blinkCount, blinkPeriod):
    for i in range (0, blinkCount):
        lightUp (ledNumber, blinkPeriod)
        time.sleep (blinkPeriod)

def runningLight (count, period):
    turnAllas (0)
    for i in range (0, count):
        for j in range (0, bit_depth):
            lightUp (j, period)
    turnAllas (0)            

def runningDark (count, period):
    turnAllas (1)   
    for i in range (0, count):
        for j in range (0, bit_depth):
            lightDown (j, period)
    turnAllas (0)            

def decToBinList (number):
    N = bit_depth - 1
    p = 0
    X = []
    while N > 0:
        p = int (number/2**N)
        if p == 1:
            X.append (1)
            number -= 2**N
        else:
            X.append (0)
        N -= 1
    X.append (number)
    return X

def lightNumber (num):
    bnum = decToBinList (num)
    n = 0
    for byte in bnum:
        GPIO.output (LEDS [n], byte)
        n += 1

def runningPattern (pattern, direction):
    turnAllas (0)  
    bnum = decToBinList (pattern)
    if direction == 1:
        tmp = bnum [0]
        for i in range (0, bit_depth - 1):
            bnum [i] = bnum [i + 1]
        bnum [bit_depth - 1] = tmp
    n = 0
    for byte in bnum:
        GPIO.output (LEDS [n], byte)
        n += 1
    
        
def num2dac (value):
    #GPIO.cleanup()
    bnum = decToBinList (value)
    n = 0
    for byte in bnum:
        GPIO.output (DAC [n], byte)
        n += 1

def receptionNumber (num):
    while num > 0:
        for i in range (0, 255):
            num2dac (i)
            time.sleep (0.01)
        for i in range (0, 255):
            num2dac (255 - i)
            time.sleep (0.01)
        num = num - 1


def sunVoltage (run_time, frequency, samplingFrequency):
    oY = []
    oX = []
    alpha = 0.0
    for i in range (0, int (2*3.14 * frequency)):
        alpha = alpha + 1/samplingFrequency
        oY.append ( 128 + int ( 127 * math.sin (alpha)) )
        oX.append (alpha)
    fig, ax = plt.subplots()    
    ax.scatter (oX, oY)
    plt.show()
    for y in oY:
        num2dac (y)
        time.sleep (float (1/samplingFrequency))
    num2dac (0)

#sunVoltage (2, 50, 50)

#first script

#print ('Writa a number (-1 for out)')
#input_num = int (input())
#while input_num != -1:
#    num2dac (input_num)
#    print ('Writa a number (-1 for out)')
#    input_num = int (input())

num2dac (0)


#second script

#print ('Writa a repetition number (-1 for out)')
#repetition_num = int (input())
#receptionNumber (repetition_num)

#num2dac (0)

#zdef showSin (amplitude, sF):
#    for i in amplitude:
#        curr = int (round (i * 127) + 128)
#        out = num2dac (curr)
#        GPIO.output (Ds, out)
#        time.sleep ( float (1 / int (sF))
                    
#freq = int (input ('Set frequency'))
#sF   = int (input ('Set sampling frequency'))
#t    = int (input ('Set time'))
                    
#tim       = np.arange (0, t, float (1/sF))
#amplitude = np.sin (2*math.pi * tim*freq)
#plt.plot (tim, amplitude)
#plt.title ('sin')
#plt.xlabel ('time')
#plt.ylabel ('amplitude sin(time)')
#plt.show()
#show_sin (amplitude, sF)


GPIO.setup (24, GPIO.IN)

def dac_data (data):
    for i in range (0, bit_depth):
        GPIO.output (DAC[i], data[i])

GPIO.setup (17, GPIO.OUT)
GPIO.output (17, 1)


#print ("Введите число (-1 для выхода)")

#while True:
#    num = int (input())
#    if num == -1:
#        break
#    print (3.3 * float (num / 255))
#    num2dac (num)

num2dac (0)

cmpPin = 4
GPIO.setup (cmpPin, GPIO.IN)
voltage = 0

def linearSearch():
    for i in range (0, 255):
        num2dac (i)
        time.sleep (0.001)
        if GPIO.input (cmpPin) == 0:
            return i
            

def binSearch():
    valt = 0
    step = 128
    while step > 1:
        #print (int (valt))
        num2dac (int (valt))
        time.sleep (0.001)
        if GPIO.input (cmpPin) == 1:
            valt += step
        else: 
            valt -= step
        step /= 2
    if valt < 0:
        return 0
    return int (valt) 

#while True:
#    currValt = binSearch()
#    print (currValt, ':', float (3.3 * currValt / 255))



GPIO.setup (21, GPIO.OUT)
GPIO.setup (20, GPIO.OUT)
GPIO.setup (16, GPIO.OUT)
GPIO.setup (12, GPIO.OUT)
GPIO.setup (7,  GPIO.OUT)
GPIO.setup (8,  GPIO.OUT)
GPIO.setup (25, GPIO.OUT)
GPIO.setup (24, GPIO.OUT)

while True:
    currValt = binSearch() + 1
    #print (currValt)
    if currValt > 250:
        currValt = 256
    #print (currValt)
    valtPow = int (math.log2 (currValt)) 
    currValt = int (math.pow (2, valtPow)) - 1
    #print (currValt, ':', float (3.3 * currValt / 255), 'V')
    lightNumber (currValt)
