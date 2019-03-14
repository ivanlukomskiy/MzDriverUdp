import RPi.GPIO as GPIO

x_axis_pin = 35
frequency_hertz = 50
left_position = 0.40
right_position = 2.5
ms_per_cycle = 1000 / frequency_hertz
shift = -1.5
LOWERING_COEFFICIENT = 0.3
# LOWERING_COEFFICIENT = 0.05

left_limit_pin = 7
right_limit_pin = 11
use_limits = False

class ServoControl:
    pwm = None
    vx = 0
    left_limit_reached = False
    right_limit_reached = True

    def sensor_interruption(self, value):
        if value == left_limit_pin:
            self.left_limit_reached = GPIO.input(left_limit_pin) == 0
        elif value == right_limit_pin:
            self.right_limit_reached = GPIO.input(right_limit_pin) == 0
        else:
            print('Unexpected pin interruption received {}'.format(value))
        print('New limits are left: {}, right: {}'.format(self.left_limit_reached, self.right_limit_reached))
        self.apply_velocity()

    def initGpio(self):
        print('Initiating GPIO')
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(left_limit_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(right_limit_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(left_limit_pin, GPIO.BOTH)
        GPIO.add_event_detect(right_limit_pin, GPIO.BOTH)
        GPIO.add_event_callback(left_limit_pin, self.sensor_interruption)
        GPIO.add_event_callback(right_limit_pin, self.sensor_interruption)

        GPIO.setup(x_axis_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(x_axis_pin, frequency_hertz)
        self.pwm.start(0)

        self.sensor_interruption(left_limit_pin)
        self.sensor_interruption(right_limit_pin)
        print('GPIO set')

    def set(self, value):
        print('setting to {}'.format(value))
        self.vx = value
        self.apply_velocity()

    def apply_velocity(self):
        vx = self.vx
        if use_limits and (self.left_limit_reached and vx < 0 or self.right_limit_reached and vx > 0):
            vx = 0
        position = left_position + (right_position - left_position) * (vx * LOWERING_COEFFICIENT + shift + 100) / 200
        value = position * 100 / ms_per_cycle
        self.pwm.start(value)
        print('pwm set to {}, value {}'.format(self.vx, value))

    def shutdown(self):
        self.pwm.stop()
        GPIO.cleanup()


SERVO_CONTROL = ServoControl()
