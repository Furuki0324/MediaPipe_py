import socket
import struct

M_SIZE = 1024

host = "127.0.0.1"
port = 50001

locaddr = (host, port)

sock = socket.socket(socket.AF_INET,type = socket.SOCK_DGRAM)
print("Create socket.")

sock.bind(locaddr)

while True:
    try:
        print("Waiting message.")
        message, cli_addr = sock.recvfrom(M_SIZE)
        message = struct.unpack('i', message)

        print(f"Received message is {message[0]}.")

    except KeyboardInterrupt:
        sock.close()
        break