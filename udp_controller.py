import select
import socket
import struct

from servo_control import SERVO_CONTROL

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

SERVO_CONTROL.initGpio()
print("GPIO initiated")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(0)
sock.bind((UDP_IP, UDP_PORT))
print("Listening for UDP connections on {}:{}".format(UDP_IP, UDP_PORT))

greatest_timestamp = 0

try:
    while 1:
        ready = select.select([sock], [], [], 0.5)
        if ready[0]:
            try:
                data, addr = sock.recvfrom(1024)
                channel, value, timestamp = struct.unpack('bfl', data)
                if timestamp < greatest_timestamp:
                    print('Stale value received')
                    continue
                greatest_timestamp = timestamp
                print("Received value {} for the channel {}".format(value, channel))
                SERVO_CONTROL.set(value)
            except:
                print("Failed to handle message")
finally:
    SERVO_CONTROL.shutdown()
