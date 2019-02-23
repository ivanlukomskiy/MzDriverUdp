import RPi.GPIO as GPIO

x_axis_pin = 35
frequency_hertz = 50
left_position = 0.40
right_position = 2.5
ms_per_cycle = 1000 / frequency_hertz

sensor_1_pin = 7


class ServoControl:
    pwm = None

    def sensor1(self, value):
        print("value is {}".format(value))
        print('Sensor value changed to {}'.format(GPIO.input(sensor_1_pin)))

    def initGpio(self):
        print('Initiating GPIO')
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(sensor_1_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(sensor_1_pin, GPIO.BOTH)
        GPIO.add_event_callback(sensor_1_pin, self.sensor1)

        GPIO.setup(x_axis_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(x_axis_pin, frequency_hertz)
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
