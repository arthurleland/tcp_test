import socket
import sys


def main():
    CLIENT = "192.168.12.101"  # this specifies the network interface to use
    SERVER = "192.168.12.100"  # The server's hostname or IP address
    # SERVER = "67.169.190.38"  # The server's hostname or IP address
    PORT = 10000  # The port used by the server

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((CLIENT, 0))
    soc.connect((SERVER, PORT))
    soc.close()

    print("client all done")


if __name__ == "__main__":
    main()
