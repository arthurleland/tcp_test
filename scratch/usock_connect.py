#!/usr/bin/env python3
import socket
import sys
import time


def main():
    soc = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    sock_addr = (
        "/home/arthur/projects/personal_projects/tcp_test/usocks/test.soc"
    )
    soc.connect(sock_addr)
    soc.sendall(b"hi")
    soc.shutdown(socket.SHUT_WR)

    while True:
        data = soc.recv(1024)
        if not data:
            print("data empty")
            soc.close()
            break
        print("received: ", data.decode())

    print("client all done")


if __name__ == "__main__":
    main()
