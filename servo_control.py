import RPi.GPIO as GPIO

x_axis_pin = 35
x_shift = -1.5
x_input_multiplier = 0.3

y_axis_pin = 37
y_shift = -2.5
y_input_multiplier = 0.3

frequency_hertz = 50
left_position = 0.40
right_position = 2.5
ms_per_cycle = 1000 / frequency_hertz
# LOWERING_COEFFICIENT = 0.05

x_left_limit_pin = 7
x_right_limit_pin = 11
use_limits = False

class ServoControl:
    x_pwm = None
    y_pwm = None
    x_v = 0
    y_v = 0
    x_left_limit_reached = False
    x_right_limit_reached = True

    def sensor_interruption(self, value):
        if value == x_left_limit_pin:
            self.x_left_limit_reached = GPIO.input(x_left_limit_pin) == 0
        elif value == x_right_limit_pin:
            self.x_right_limit_reached = GPIO.input(x_right_limit_pin) == 0
        else:
            print('Unexpected pin interruption received {}'.format(value))
        print('New limits are left: {}, right: {}'.format(self.x_left_limit_reached, self.x_right_limit_reached))
        self.apply_x_velocity()

    def initGpio(self):
        print('Initiating GPIO')
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(x_left_limit_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(x_right_limit_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(x_left_limit_pin, GPIO.BOTH)
        GPIO.add_event_detect(x_right_limit_pin, GPIO.BOTH)
        GPIO.add_event_callback(x_left_limit_pin, self.sensor_interruption)
        GPIO.add_event_callback(x_right_limit_pin, self.sensor_interruption)

        GPIO.setup(x_axis_pin, GPIO.OUT)
        GPIO.setup(y_axis_pin, GPIO.OUT)

        self.x_pwm = GPIO.PWM(x_axis_pin, frequency_hertz)
        self.y_pwm = GPIO.PWM(y_axis_pin, frequency_hertz)
        self.x_pwm.start(0)
        self.y_pwm.start(0)

        self.sensor_interruption(x_left_limit_pin)
        self.sensor_interruption(x_right_limit_pin)
        print('GPIO set')

    def set_x_v(self, value):
        print('setting x_v to {}'.format(value))
        self.x_v = value
        self.apply_x_velocity()

    def set_y_v(self, value):
        print('setting y_v to {}'.format(value))
        self.y_v = value
        self.apply_y_velocity()

    def apply_x_velocity(self):
        x_v = self.x_v
        if use_limits and (self.x_left_limit_reached and x_v < 0 or self.x_right_limit_reached and x_v > 0):
            x_v = 0
        position = left_position + (right_position - left_position) * (x_v * x_input_multiplier + x_shift + 100) / 200
        value = position * 100 / ms_per_cycle
        self.x_pwm.start(value)
        print('x pwm set to {}, value {}'.format(self.x_v, value))

    def apply_y_velocity(self):
        y_v = self.y_v
        position = left_position + (right_position - left_position) * (y_v * y_input_multiplier + y_shift + 100) / 200
        value = position * 100 / ms_per_cycle
        self.y_pwm.start(value)
        print('y pwm set to {}, value {}'.format(self.y_v, value))

    def shutdown(self):
        self.x_pwm.stop()
        self.y_pwm.stop()
        GPIO.cleanup()


SERVO_CONTROL = ServoControl()
