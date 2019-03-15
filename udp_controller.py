import select
import socket
import struct

from servo_control import SERVO_CONTROL

UDP_IP = "0.0.0.0"
UDP_PORT = 5005
X_CHANNEL = 1
Y_CHANNEL = 2

SERVO_CONTROL.initGpio()
print("GPIO initiated")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(0)
sock.bind((UDP_IP, UDP_PORT))
print("Listening for UDP connections on {}:{}".format(UDP_IP, UDP_PORT))

greatest_timestamp_x = 0
greatest_timestamp_y = 0

try:
    while 1:
        ready = select.select([sock], [], [], 0.5)
        if ready[0]:
            try:
                data, addr = sock.recvfrom(1024)
                channel, value, timestamp = struct.unpack('bfq', data)
                print("Received value {} for the channel {}".format(value, channel))

                if channel == X_CHANNEL:
                    if timestamp < greatest_timestamp_x:
                        print('Stale X value received')
                        continue
                    greatest_timestamp_x = timestamp
                    SERVO_CONTROL.set_x_v(value)
                elif channel == Y_CHANNEL:
                    if timestamp < greatest_timestamp_y:
                        print('Stale Y value received')
                        continue
                    greatest_timestamp_y = timestamp
                    SERVO_CONTROL.set_y_v(value)

            except:
                print("Failed to handle message")
finally:
    SERVO_CONTROL.shutdown()
