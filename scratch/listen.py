#!/usr/bin/env python3
import socket
import sys


def main():
    # SERVER = "192.168.106.100"
    SERVER = "127.0.0.1"
    PORT = 10000  # Port to listen on (non-privileged ports are > 1023)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((SERVER, PORT))
    s.listen()
    conn, addr = s.accept()
    data = conn.recv(1024)
    print("received: ", data.decode())
    conn.sendall(b"one")
    conn.sendall(b"more")
    conn.sendall(b"time")
    conn.close()
    s.close()
    print("server all done")


if __name__ == "__main__":
    main()
