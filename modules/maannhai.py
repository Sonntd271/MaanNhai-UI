import time
from gpiozero import LED, Button, DigitalInputDevice
from utils.tts import speak, OPEN, CLOSE, OFF, ENA

class MaanNhai:
    """
    A class used to represent a MaanNhai device.

    ...

    Attributes
    ----------
    red : gpiozero.LED
        The red LED object - pin 17 by default.
    green : gpiozero.LED
        The green LED object - pin 27 by default.
    blue : gpiozero.LED
        The blue LED object - pin 22 by default.
    button1 : gpiozero.Button
        The button1 Button object - pin 24 by default.
    button2: gpiozero.Button
        The button2 Button object - pin 23 by default.
    lmPulley : gpiozero.DigitalInputDevice
        The lmPulley DigitalInputDevice object - pin 12 with 0.1 sec of bounce time by default.
    lmMotor : gpiozero.DigitalInputDevice
        The lmMotor DigitalInputDevice object - pin 6 with 0.1 sec of bounce time by default.
    pul : gpiozero.LED
        The pul LED object - pin 16 by default.
    dir : gpiozero.LED
        The dir LED object - pin 20 by default.
    ena : gpiozero.LED
        The ena LED object - pin 21 by default.
    speed : int
        The motor speed.
    rotate : int
        The motor rotation.
    status : str
        The curtain status.


    Methods
    -------
    led()
        Set all LED off.
    ledOff()
        Sets LED colour off.
    ledRed()
        Sets LED colour to red.
    ledGreen()
        Sets LED colour to green.
    ledBlue()
        Sets LED colour to blue.
    ledPurple()
        Sets LED colour to purple.
    ledCyan()
        Sets LED colour to cyan.
    ledYellow()
        Sets LED colour to yellow.
    ledWhite()
        Sets LED colour to white.
    moveToMotor()
        Moves to motor direction.
    moveToPulley()
        Moves to pulley direction.
    stopMotor()
        Stops the motor, calls moveToPulley.
    stopPulley()
        Stops at pulley, calls moveToMotor.
    moveUntilMotor()
        Moves until it hits the motor.
    moveUntilPulley()
        Moves until it hits the pulley.
    moveHome()
        Moves to pulley and stops.
    run()
        Runs the main control loop.
    open_curtain()
        Opens the curtain when it's closed, else do nothing.
    close_curtain()
        Closes the curtain when it's opened, else do nothing.
    handle_buttons()
        Handles button presses to control the curtains.
    """

    def __init__(self, init_status="close"):
        # Assign pins
        self.red = LED(17)
        self.green = LED(27)
        self.blue = LED(22)

        self.button1 = Button(24, pull_up=True)
        self.button2 = Button(23, pull_up=True)

        self.lmPulley = DigitalInputDevice(12, pull_up=True, bounce_time = 0.1)
        self.lmMotor = DigitalInputDevice(6, pull_up=True, bounce_time = 0.1)

        self.pul = LED(16)
        self.dir = LED(20)
        self.ena = LED(21)

        # Setup motor parameters
        self.speed = 50
        self.rotate = 90
        self.status = init_status

    # Setup functions to control LED colors
    def led(self, rgb):
        """Sets LED colour according to the inputs.

        Parameters
        ----------
        rgb : str
            The colour code, e.g. - '000'

        Returns
        -------
        None
        """

        r, g, b = [int(color) for color in rgb]
        self.red.value = r
        self.green.value = g
        self.blue.value = b

    def ledOff(self):
        """Sets LED colour off.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        self.led("000")

    def ledRed(self):
        """Sets LED colour to red.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
            
        self.led("100")

    def ledGreen(self):
        """Sets LED colour to green.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
                
        self.led("010")

    def ledBlue(self):
        """Sets LED colour to blue.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
            
        self.led("001")

    def ledPurple(self):
        """Sets LED colour to purple.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
            
        self.led("101")

    def ledCyan(self):
        """Sets LED colour to cyan.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
                
        self.led("011")

    def ledYellow(self):
        """Sets LED colour to yellow.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        self.led("110")

    def ledWhite(self):
        """Sets LED colour to white.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        self.led("111")

    # Motor control methods
    def moveToMotor(self):
        """Moves to motor direction.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
            
        self.dir.off()
        time.sleep(0.0001)
        for _ in range(self.rotate):
            self.pul.on()
            time.sleep(0.001 / self.speed)
            self.pul.off()
            time.sleep(0.001 / self.speed)

    def moveToPulley(self):
        """Moves to pulley direction.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        self.dir.on()
        time.sleep(0.0001)
        for _ in range(self.rotate):
            self.pul.on()
            time.sleep(0.001 / self.speed)
            self.pul.off()
            time.sleep(0.001 / self.speed)

    def stopMotor(self):
        """Stops at motor, calls moveToPulley.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        self.ledRed()
        time.sleep(0.01)
        self.moveToPulley()
        time.sleep(0.01)
        time.sleep(0.5)
        self.ledOff()

    def stopPulley(self):
        """Stops at pulley, calls moveToMotor.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        self.ledRed()
        time.sleep(0.01)
        self.moveToMotor()
        time.sleep(0.01)
        time.sleep(0.5)
        self.ledOff()

    # Movement control methods
    def moveUntilMotor(self):
        """Moves until it hits the motor.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        self.ledPurple()
        while self.lmMotor.is_active:
            self.moveToMotor()
        self.stopMotor()
        self.ledOff()

    def moveUntilPulley(self):
        """Moves until it hits the pulley.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        self.ledBlue()
        while self.lmPulley.is_active:
            self.moveToPulley()
        self.stopPulley()
        self.ledOff()

    def moveHome(self):
        """Moves to pulley and stops.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

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

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        if action == "OPEN":
            self.open_curtain()
        elif action == "CLOSE":
            self.close_curtain()
        else:
            self.handle_buttons()

    def open_curtain(self):
        """Opens the curtain when it's closed, else do nothing.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        if self.status == "close":
            print("[DEVICE] Openning")
            self.ledCyan()
            self.moveUntilMotor()
            self.status = "open"
            if ENA:
                speak("open")
            print("[DEVICE] Curtains are OPENED")
            self.ledGreen()

    def close_curtain(self):
        """Closes the curtain when it's opened, else do nothing.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        if self.status == "open":
            print("[DEVICE] Closing")
            self.ledYellow()
            self.moveUntilPulley()
            self.status = "close"
            if ENA:
                speak("close")
            print("[DEVICE] Curtains are CLOSED")
            self.ledGreen()


    def handle_buttons(self, queue):
        """
        Handles button presses to control the curtains.

        Parameters
        ----------
        queue: queue.Queue
            The message queue.

        Returns
        -------
        None
        """

        while True:
            self.ledGreen()

            if not self.lmPulley.is_active:
                print("lmPulley active")
                self.stopPulley()
                self.status = "close"
                if ENA:
                    speak(CLOSE)

            if not self.lmMotor.is_active:
                print("lmMotor active")
                self.stopMotor()
                self.status = "open"
                if ENA:
                    speak(OPEN)

            if self.button1.is_pressed:
                print("Button1 pressed")
                if self.status == "close":
                    self.ledCyan()
                    self.moveToMotor()
                    time.sleep(0.005)
                else:
                    self.ledYellow()
                    self.moveToPulley()
                    time.sleep(0.005)

            if self.button2.is_pressed:
                print("Button2 pressed")
                if self.button1.is_pressed:
                    self.moveHome()
                    print("Curtain Turning off")
                    if ENA:
                        speak(OFF)
                    return
                if self.status == "close":
                    self.moveUntilMotor()
                    time.sleep(0.01)
                    self.status = "open"
                    if ENA:
                        speak(OPEN)
                else:
                    self.moveUntilPulley()
                    time.sleep(0.01)
                    self.status = "close"
                    if ENA:
                        speak(CLOSE)

            time.sleep(0.1)


if __name__ == '__main__':
    curtain_control = MaanNhai(init_status="close")
    curtain_control.run()
