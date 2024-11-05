from gpiozero import LED, Button, DigitalInputDevice
import time

# Assign pins-----------------------------------------
red = LED(11)
green = LED(13)
blue = LED(15)

button1 = Button(18, pull_up=True)
button2 = Button(16, pull_up=True)

lmPulley = DigitalInputDevice(32, pull_up=True)
lmMotor = DigitalInputDevice(31, pull_up=True)

pul = LED(36)
dir = LED(38)
ena = LED(40)

# Setup motor parameter-------------------------------
speed = 50
rotate = 90

# Setup functions to be used--------------------------

def led(rgb):
    r, g, b = [red.off if color == '0' else red.on for color in list(rgb)]
    red.value, green.value, blue.value = r, g, b

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
    dir.off()
    time.sleep(.0001)
    for _ in range(rotate):
        pul.on()
        time.sleep(.001/int(speed))
        pul.off()
        time.sleep(.001/int(speed))

def moveToPulley():
    dir.on()
    time.sleep(.0001)
    for _ in range(rotate):
        pul.on()
        time.sleep(.001/int(speed))
        pul.off()
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
    while not lmMotor.is_active:
        moveToMotor()
    stopMotor()
    ledOff()

def moveUntilPulley():
    ledBlue()
    while not lmPulley.is_active:
        moveToPulley()
    stopPulley()
    ledOff()

def moveHome():
    ledWhite()
    while not lmPulley.is_active:
        moveToPulley()
    stopPulley()
    ledOff()

# main--------------------------------------------------
# the status parameter is the start state of the curtain
def main_MaanNaai(init_status="close"):
    status = init_status
    while True:    
        ledGreen()

        if lmPulley.is_active:
            stopPulley()
            status = "close"
        if lmMotor.is_active:
            stopMotor()
            status = "open"
            
        if button1.is_pressed:
            if status == "close":
                ledCyan()
                moveToMotor()
                time.sleep(0.005)
            else:
                ledYellow()
                moveToPulley()
                time.sleep(0.005)

        if button2.is_pressed:
            if button1.is_pressed:
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
