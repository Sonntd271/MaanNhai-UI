import time
from gpiozero import LED, Button, DigitalInputDevice
from utils.tts import speak

class MaanNhai:
    def __init__(self, init_status="close"):
        # Assign pins
        self.red = LED(17)
        self.green = LED(27)
        self.blue = LED(22)

        self.button1 = Button(24, pull_up=True)
        self.button2 = Button(23, pull_up=True)

        self.lmPulley = DigitalInputDevice(12, pull_up=True)
        self.lmMotor = DigitalInputDevice(6, pull_up=True)

        self.pul = LED(16)
        self.dir = LED(20)
        self.ena = LED(21)

        # Setup motor parameters
        self.speed = 50
        self.rotate = 90
        self.status = init_status

    # Setup functions to control LED colors
    def led(self, rgb):
        r, g, b = [int(color) for color in rgb]
        self.red.value = r
        self.green.value = g
        self.blue.value = b

    def ledOff(self):
        self.led("000")

    def ledRed(self):
        self.led("100")

    def ledGreen(self):
        self.led("010")

    def ledBlue(self):
        self.led("001")

    def ledPurple(self):
        self.led("101")

    def ledCyan(self):
        self.led("011")

    def ledYellow(self):
        self.led("110")

    def ledWhite(self):
        self.led("111")

    # Motor control methods
    def moveToMotor(self):
        self.dir.off()
        time.sleep(0.0001)
        for _ in range(self.rotate):
            self.pul.on()
            time.sleep(0.001 / self.speed)
            self.pul.off()
            time.sleep(0.001 / self.speed)

    def moveToPulley(self):
        self.dir.on()
        time.sleep(0.0001)
        for _ in range(self.rotate):
            self.pul.on()
            time.sleep(0.001 / self.speed)
            self.pul.off()
            time.sleep(0.001 / self.speed)

    def stopMotor(self):
        self.ledRed()
        time.sleep(0.01)
        self.moveToPulley()
        time.sleep(0.01)
        time.sleep(0.5)
        self.ledOff()

    def stopPulley(self):
        self.ledRed()
        time.sleep(0.01)
        self.moveToMotor()
        time.sleep(0.01)
        time.sleep(0.5)
        self.ledOff()

    # Movement control methods
    def moveUntilMotor(self):
        self.ledPurple()
        while self.lmMotor.is_active:
            self.moveToMotor()
        self.stopMotor()
        self.ledOff()

    def moveUntilPulley(self):
        self.ledBlue()
        while self.lmPulley.is_active:
            self.moveToPulley()
        self.stopPulley()
        self.ledOff()

    def moveHome(self):
        self.ledWhite()
        while self.lmPulley.is_active:
            self.moveToPulley()
        self.stopPulley()
        self.ledOff()

    # Main loop to run the curtain control system
    def run(self, action=None):
        """
        Runs the main control loop.
        If an action ("OPEN" or "CLOSE") is provided, it will execute that action.
        Otherwise, it will handle button presses.
        """
        if action == "OPEN":
            self.open_curtain()
        elif action == "CLOSE":
            self.close_curtain()
        else:
            self.handle_buttons()

    def open_curtain(self):
        if self.status == "close":
            self.led_cyan()
            self.move_to_motor()
            time.sleep(0.005)
            self.move_until_motor()
            self.status = "open"
            speak("open")
            print("[DEVICE] Curtains are OPENED")
            self.led_green()

    def close_curtain(self):
        if self.status == "open":
            self.led_yellow()
            self.move_to_pulley()
            time.sleep(0.005)
            self.move_until_pulley()
            self.status = "close"
            speak("close")
            print("[DEVICE] Curtains are CLOSED")
            self.led_green()

    def handle_buttons(self):
        """
        Handles button presses to control the curtains.
        """
        while True:
            self.led_green()

            if not self.lmPulley.is_active:
                print("lmPulley active")
                self.stop_pulley()
                self.status = "close"
                speak("close")

            if not self.lmMotor.is_active:
                print("lmMotor active")
                self.stop_motor()
                self.status = "open"
                speak("open")

            if self.button1.is_pressed:
                print("Button1 pressed")
                if self.status == "close":
                    self.led_cyan()
                    self.move_to_motor()
                    time.sleep(0.005)
                else:
                    self.led_yellow()
                    self.move_to_pulley()
                    time.sleep(0.005)

            if self.button2.is_pressed:
                print("Button2 pressed")
                if self.button1.is_pressed:
                    self.move_home()
                    print("Curtain Turning off")
                    speak("Curtain turning off")
                    break

                if self.status == "close":
                    self.move_until_motor()
                    time.sleep(0.01)
                    self.status = "open"
                    speak("open")
                    print("[DEVICE] Curtains are OPENED")
                else:
                    self.move_until_pulley()
                    time.sleep(0.01)
                    self.status = "close"
                    speak("close")
                    print("[DEVICE] Curtains are CLOSED")


if __name__ == '__main__':
    curtain_control = MaanNhai(init_status="close")
    curtain_control.run()
