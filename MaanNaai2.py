from gpiozero import LED, Button
from time import sleep

# Define pins using BCM numbering system (from original BOARD pin mapping)
red = 17      # BCM 17 (was BOARD 11)
green = 27    # BCM 27 (was BOARD 13)
blue = 22     # BCM 22 (was BOARD 15)

button1 = 24  # BCM 24 (was BOARD 18)
button2 = 23  # BCM 23 (was BOARD 16)

lmPulley = 12  # BCM 12 (was BOARD 32)
lmMotor = 6    # BCM 6 (was BOARD 31)

pul = 16       # BCM 16 (was BOARD 36)
dir = 20       # BCM 20 (was BOARD 38)
ena = 21       # BCM 21 (was BOARD 40)

# Setup GPIO------------------------------------------

# LEDs
red_led = LED(red)
green_led = LED(green)
blue_led = LED(blue)

# Buttons
button1 = Button(button1)
button2 = Button(button2)

# Motors (inputs for the pulley and motor sensors)
lm_pulley = Button(lmPulley)
lm_motor = Button(lmMotor)

# Motor control (outputs for stepper motor)
pul_motor = LED(pul)
dir_motor = LED(dir)
ena_motor = LED(ena)

# Setup motor parameters-------------------------------
speed = 50
rotate = 90

# Setup functions to be used--------------------------

def led(rgb):
    r, g, b = [False if color == '0' else True for color in list(rgb)]
    red_led.value = r
    green_led.value = g
    blue_led.value = b

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
    dir_motor.off()
    sleep(0.0001)
    for _ in range(rotate):
        pul_motor.on()
        sleep(0.001 / speed)
        pul_motor.off()
        sleep(0.001 / speed)

def moveToPulley():
    dir_motor.on()
    sleep(0.0001)
    for _ in range(rotate):
        pul_motor.on()
        sleep(0.001 / speed)
        pul_motor.off()
        sleep(0.001 / speed)

def stopMotor():
    ledRed()
    sleep(0.01)
    moveToPulley()
    sleep(0.01)
    sleep(0.5)
    ledOff()

def stopPulley():
    ledRed()
    sleep(0.01)
    moveToMotor()
    sleep(0.01)
    sleep(0.5)
    ledOff()

def moveUntilMotor():
    ledPurple()
    while not lm_motor.is_pressed:
        moveToMotor()
    stopMotor()
    ledOff()

def moveUntilPulley():
    ledBlue()
    while not lm_pulley.is_pressed:
        moveToPulley()
    stopPulley()
    ledOff()

def moveHome():
    ledWhite()
    while not lm_pulley.is_pressed:
        moveToPulley()
    stopPulley()
    ledOff()

# main--------------------------------------------------

# the status parameter is the start state of the curtain
def main_MaanNaai(init_status="close"):
    status = init_status
    while True:
        ledGreen()

        if lm_pulley.is_pressed:
            stopPulley()
            status = "close"
        if lm_motor.is_pressed:
            stopMotor()
            status = "open"

        if not button1.is_pressed:
            if status == "close":
                ledCyan()
                moveToMotor()
                sleep(0.005)

            else:
                ledYellow()
                moveToPulley()
                sleep(0.005)

        if not button2.is_pressed:
            if not button1.is_pressed:
                moveHome()
                break

            if status == "close":
                moveUntilMotor()
                sleep(0.01)
                status = "open"
            else:
                moveUntilPulley()
                sleep(0.01)
                status = "close"

if __name__ == "__main__":
    main_MaanNaai()
