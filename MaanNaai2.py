from gpiozero import LED, Button, DigitalInputDevice
import time

# Assign pins-----------------------------------------
red = LED(17)
green = LED(27)
blue = LED(22)

button1 = Button(24, pull_up=True)
button2 = Button(23, pull_up=True)

lmPulley = DigitalInputDevice(12, pull_up=True)
lmMotor = DigitalInputDevice(6, pull_up=True)

pul = LED(16)
dir = LED(20)
ena = LED(21)

# Setup motor parameter-------------------------------
speed = 50
rotate = 90

# Setup functions to be used--------------------------

def led(rgb):
    r,g,b = [int(color) for color in rgb]
    red.value = r
    green.value = g
    blue.value = b


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
    while lmMotor.is_active:
        moveToMotor()
    stopMotor()
    ledOff()

def moveUntilPulley():
    ledBlue()
    while lmPulley.is_active:
        moveToPulley()
    stopPulley()
    ledOff()

def moveHome():
    ledWhite()
    while lmPulley.is_active:
        moveToPulley()
    stopPulley()
    ledOff()

# main--------------------------------------------------
# the status parameter is the start state of the curtain
def main_MaanNaai(init_status="close"):
    status = init_status
    while True:    
        ledGreen()
        # print(status)

        if not lmPulley.is_active:
            print("lmpulley active")
            stopPulley()
            status = "close"
        if not lmMotor.is_active:
            print("lmmotor active")
            stopMotor()
            status = "open"
            
        if button1.is_pressed:
            print("b1 pressed")
            if status == "close":
                ledCyan()
                moveToMotor()
                time.sleep(0.005)
            else:
                ledYellow()
                moveToPulley()
                time.sleep(0.005)

        if button2.is_pressed:
            print("b2 pressed")
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

if __name__ == '__main__':
    main_MaanNaai()
