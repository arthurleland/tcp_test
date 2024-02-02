#!/usr/bin/env python3
import os
import socket
import sys


def main():
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    sock_addr = (
        "/home/arthur/projects/personal_projects/tcp_test/usocks/test.soc"
    )
    if os.path.exists(sock_addr):
        os.remove(sock_addr)
    s.bind(sock_addr)
    s.listen()
    conn, addr = s.accept()

    data = conn.recv(1024)
    print("received: ", data.decode())
    conn.sendall(b"one")
    conn.close()
    s.close()
    print("server all done")


if __name__ == "__main__":
    main()
