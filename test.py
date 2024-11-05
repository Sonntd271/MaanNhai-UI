# from gpiozero import LED, Button

# red = 17      # BCM 17 (was BOARD 11)
# green = 27    # BCM 27 (was BOARD 13)
# blue = 22     # BCM 22 (was BOARD 15)

# button1 = 24  # BCM 24 (was BOARD 18)
# button2 = 23  # BCM 23 (was BOARD 16)

# # LEDs
# red_led = LED(red)
# green_led = LED(green)
# blue_led = LED(blue)

# # Buttons
# button1 = Button(button1)
# button2 = Button(button2)

# button1.when_pressed(red_led.on)
# button2.when_pressed(green_led.on)

from gpiozero import LED, Button
from signal import pause

led = LED(17)
button = Button(24)

button.when_pressed = led.on
button.when_released = led.off

pause()