import socket
import struct

from servo_control import SERVO_CONTROL

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

SERVO_CONTROL.initGpio()
print("GPIO initiated")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print("Listening for UDP connections on {}:{}".format(UDP_IP, UDP_PORT))

try:
    while 1:
        try:
            data, addr = sock.recvfrom(1024)
            channel, value = struct.unpack('bf', data)
            print("Received value {} for the channel {}".format(value, channel))
            SERVO_CONTROL.set(value)
        except:
            print("Failed to handle message")
finally:
    SERVO_CONTROL.shutdown()
