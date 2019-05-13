import RPi.GPIO as GPIO

frequency_hertz = 50
left_position = 0.40
right_position = 2.5
ms_per_cycle = 1000 / frequency_hertz


class AxisControl:
    v = 0
    pwm = None
    left_limit_reached = False
    right_limit_reached = False

    def __init__(self, name, pin, shift, multiplier, left_limit_pin, right_limit_pin):
        self.name = name
        self.pin = pin
        self.shift = shift
        self.multiplier = multiplier
        self.left_limit_pin = left_limit_pin
        self.right_limit_pin = right_limit_pin

        if left_limit_pin is not None:
            GPIO.setup(left_limit_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(left_limit_pin, GPIO.BOTH)
            GPIO.add_event_callback(left_limit_pin, self.limit_changed)
            self.limit_changed(left_limit_pin)

        if right_limit_pin is not None:
            GPIO.setup(right_limit_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(right_limit_pin, GPIO.BOTH)
            GPIO.add_event_callback(right_limit_pin, self.limit_changed)
            self.limit_changed(right_limit_pin)

        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, frequency_hertz)
        self.pwm.start(0)

    def set(self, value):
        print('setting {} to {}'.format(self.name, value))
        self.v = value
        self.apply()

    def apply(self):
        v = self.v
        if self.left_limit_reached and v < 0 or self.right_limit_reached and v > 0:
            v = 0

        position = left_position + (right_position - left_position) * (v * self.multiplier + self.shift + 100) / 200
        value = position * 100 / ms_per_cycle
        self.pwm.start(value)
        print('{} set to {}, value {}'.format(self.name, self.v, value))

    def limit_changed(self, value):
        if value == self.left_limit_pin:
            self.left_limit_reached = GPIO.input(self.left_limit_pin) == 0
        elif value == self.right_limit_pin:
            self.right_limit_reached = GPIO.input(self.right_limit_pin) == 0
        else:
            print('Unexpected pin interruption received {}'.format(value))
        print('New limits are left: {}, right: {}'.format(self.left_limit_reached, self.right_limit_reached))
        self.apply()

    def stop(self):
        self.pwm.stop()


class ServoControl:

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)

        self.x = AxisControl(
            name="x",
            pin=35,
            shift=-5.5,
            multiplier=0.3,
            left_limit_pin=None,
            right_limit_pin=None
            # left_limit_pin=7,
            # right_limit_pin=11
        )

        self.y = AxisControl(
            name="y",
            pin=37,
            shift=-4.5,
            multiplier=0.3,
            left_limit_pin=None,
            right_limit_pin=None
        )

    def shutdown(self):
        self.x.stop()
        self.y.stop()
        GPIO.cleanup()


SERVO_CONTROL = ServoControl()
