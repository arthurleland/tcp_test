import socket
import sys


def main():
    CLIENT = "10.1.10.111"  # this specifies the network interface to use
    SERVER = "127.0.0.1"  # The server's hostname or IP address
    # SERVER = "67.169.190.38"  # The server's hostname or IP address
    PORT = 10000  # The port used by the server

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((CLIENT, 0))
    soc.connect((SERVER, PORT))
    soc.close()

    print("connect all done")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        soc.connect((HOST, PORT))


if __name__ == "__main__":
    main()
