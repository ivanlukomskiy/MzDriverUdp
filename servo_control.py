# This gives us control of the Raspberry Pi's pins.
# This is only used for time delays... standard Python stuff.

import RPi.GPIO as GPIO

pin_number = 35
frequency_hertz = 50
left_position = 0.40
right_position = 2.5
ms_per_cycle = 1000 / frequency_hertz


class ServoControl:
    pwm = None

    def initGpio(self):
        print('Initiating GPIO')
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin_number, GPIO.OUT)
        self.pwm = GPIO.PWM(pin_number, frequency_hertz)
        self.pwm.start(0)
        print('GPIO set')

    def set(self, value):
        print('setting to {}'.format(value))
        position = left_position + (right_position - left_position) * (value + 100) / 200
        self.pwm.start(position * 100 / ms_per_cycle)
        print('pwm set to {}'.format(value))

    def shutdown(self):
        self.pwm.stop()
        GPIO.cleanup()


SERVO_CONTROL = ServoControl()
