import socket
import sys
import time


def main():
    SERVER = "192.168.107.101"  # The server's hostname or IP address
    # CLIENT = "192.168.12.102"  # this specifies the network interface to use
    # SERVER = "67.169.190.38"  # The server's hostname or IP address
    PORT = 10000  # The port used by the server

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # soc.bind((CLIENT, 0))
    soc.connect((SERVER, PORT))
    soc.sendall(b"hi")
    soc.close()

    while True:
        data = soc.recv(1024)
        if not data:
            print("data empty")
            break
        print("received: ", data.decode())

    print("client all done")


if __name__ == "__main__":
    main()
