import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

on = GPIO.HIGH
off = GPIO.LOW

# Assign pins-----------------------------------------
red = 11
green = 13
blue = 15

button1 = 18
button2 = 16

lmPulley = 32
lmMotor = 31

pul = 36
dir = 38
ena = 40

# Setup GPIO------------------------------------------

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(lmPulley, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(lmMotor, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

GPIO.setup(pul,GPIO.OUT)
GPIO.setup(dir,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)

# Setup motor parameter-------------------------------

speed = 50
rotate = 90 


# Setup functions to be used--------------------------

def led(rgb):
    r, g, b = [off if color == '0' else on for color in list(rgb)]
    GPIO.output(red, r)
    GPIO.output(green, g)
    GPIO.output(blue, b)

def ledOff():
    led("000")

def ledRed():
    led("100")
    
def ledGreen():
    led("010")
    
def ledBlue():
    led("001")

def ledPurple():
    led("101")

def ledCyan():
    led("011")

def ledYellow():
    led("110")

def ledWhite():
    led("111")

def moveToMotor():
    GPIO.output(dir,off)
    time.sleep(.0001)
    for _ in range(rotate):
      GPIO.output(pul,on)
      time.sleep(.001/int(speed))
      GPIO.output(pul,off)
      time.sleep(.001/int(speed))

def moveToPulley():
    GPIO.output(dir,on)
    time.sleep(.0001)
    for _ in range(rotate):
      GPIO.output(pul,on)
      time.sleep(.001/int(speed))
      GPIO.output(pul,off)
      time.sleep(.001/int(speed))

def stopMotor():
    ledRed()
    time.sleep(0.01)
    moveToPulley()
    time.sleep(0.01)
    time.sleep(0.5)
    ledOff()
            
def stopPulley():
    ledRed()
    time.sleep(0.01)
    moveToMotor()
    time.sleep(0.01)
    time.sleep(0.5)
    ledOff()
        
def moveUntilMotor():
    ledPurple()
    while (not GPIO.input(lmMotor)):
        moveToMotor()
    stopMotor()
    ledOff()

def moveUntilPulley():
    ledBlue()
    # start = time.time()
    while (not GPIO.input(lmPulley)):
        moveToPulley()
    # end = time.time()
    stopPulley()
    # start = time.time()
    # print(f"Time taken {1000*(end-start)}")
    ledOff()

def moveHome():
    ledWhite()
    while (not GPIO.input(lmPulley)):
        moveToPulley()
    stopPulley()
    ledOff()

# main--------------------------------------------------
# the status parameter is the start state of the curtain
def main_MaanNaai(init_status = "close"):
    status = init_status
    while True:    
        ledGreen()
        
        if (GPIO.input(lmPulley)):
            stopPulley()
            status = "close"
        if (GPIO.input(lmMotor)):
            stopMotor()
            status = "open"
            
        if not GPIO.input(button1):
            if status == "close":
                ledCyan()
                #time.sleep(0.01)
                moveToMotor()
                time.sleep(0.005)
        
            else:
                ledYellow()
                #time.sleep(0.01)
                moveToPulley()
                time.sleep(0.005)

        if not GPIO.input(button2):
            if not GPIO.input(button1):
                moveHome()
                break

            if status == "close":
                moveUntilMotor()
                time.sleep(0.01)
                status = "open"
            else:
                moveUntilPulley()
                time.sleep(0.01)
                status = "close"
           
main_MaanNaai()
