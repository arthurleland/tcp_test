import socket
import sys


def main():
    SERVER = "192.168.12.100"  # Standard loopback interface address (localhost)
    PORT = 10000  # Port to listen on (non-privileged ports are > 1023)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((SERVER, PORT))
    s.listen()
    conn, addr = s.accept()
    conn.close()
    s.close()
    print("server all done")


if __name__ == "__main__":
    main()
