import time

import board
import busio
import digitalio
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket

# Name address for wifitest.adafruit.com
SERVER_ADDRESS = (('104.236.193.178'), 80)

cs = digitalio.DigitalInOut(board.D10)
spi_bus = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialize ethernet interface with DHCP
eth = WIZNET5K(spi_bus, cs)

print("DHCP Assigned IP: ", eth.pretty_ip(eth.ip_address))

socket.set_interface(eth)

# Create a new socket
sock = socket.socket()

print("Connecting to: ", SERVER_ADDRESS[0])
sock.connect(SERVER_ADDRESS)

print("Connected to ", sock.getpeername())

# Make a HTTP Request
sock.send(b"GET /testwifi/index.html HTTP/1.1\n")
sock.send(b"Host: 104.236.193.178\n")
sock.send(b"Connection: close\n\n")

# Start transmission timer
start = time.monotonic()

bytes_avail = 0
while not bytes_avail:
    bytes_avail = sock.available()
    if bytes_avail > 0:
        data = sock.recv(bytes_avail)
        print(data[0])
        break
    time.sleep(0.05)

end = time.monotonic()
print("Received: %d bytes"%bytes_avail)
end = end - start / 1000000.0
rate = bytes_avail / end / 1000.0
print("Rate = %0.5f kbytes/second"%rate)