import select
import socket
import struct
import time
import traceback
from threading import Thread

from servo_control import SERVO_CONTROL

current_milli_time = lambda: int(round(time.time() * 1000))

UDP_IP = "0.0.0.0"
UDP_PORT = 5005
X_CHANNEL = 1
Y_CHANNEL = 2
EXPIRATION_TIME = 100


class AxisController:
    greatest_timestamp = 0
    expire_time = 0

    def __init__(self, name, controller):
        self.name = name
        self.controller = controller

    def set(self, value, timestamp):
        if timestamp < self.greatest_timestamp:
            print('Stale value received for {}'.format(self.name))
            return
        self.greatest_timestamp = timestamp
        self.expire_time = current_milli_time() + EXPIRATION_TIME
        self.controller.set(value)

    def check_expiration(self):
        if current_milli_time() > self.expire_time:
            print('Got disconnection on {}'.format(self.name))
            self.controller.set(0)


class UdpController:
    sock = None

    def __init__(self):
        self.controllers = {
            1: AxisController(name='x', controller=SERVO_CONTROL.x),
            2: AxisController(name='y', controller=SERVO_CONTROL.y)
        }
        print("Listening for UDP connections on {}:{}".format(UDP_IP, UDP_PORT))

    def udp_loop(self):
        try:
            while 1:
                ready = select.select([self.sock], [], [], 0.5)
                if ready[0]:
                    try:
                        data, addr = self.sock.recvfrom(1024)
                        channel, value, timestamp = struct.unpack('bfq', data)
                        print("Received value {} for the channel {}".format(value, channel))

                        self.controllers[channel].set(value, timestamp)

                    except:
                        print("Failed to handle message", traceback.format_exc())
        finally:
            SERVO_CONTROL.shutdown()

    def connection_check_control(self):
        while 1:
            time.sleep(0.01)
            for controller in self.controllers.values():
                controller.check_expiration()

    def startup(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(0)
        self.sock.bind((UDP_IP, UDP_PORT))
        Thread(target=self.udp_loop()).start()
        Thread(target=self.connection_check_control()).start()


control = UdpController()
control.startup()
