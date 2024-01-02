import socket
import sys
import threading


def read_fun(conn):
    while True:
        stuff = conn.recv(1024)
        print("*" + stuff.decode(), end="")


def write_fun(conn):
    for line in sys.stdin:
        conn.sendall(line.encode())


def main():
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 10000  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        soc.connect((HOST, PORT))
        print(f"connected on: {soc.getsockname()}")

        read_t = threading.Thread(target=read_fun, args=(soc,))
        write_t = threading.Thread(target=write_fun, args=(soc,))
        read_t.start()
        write_t.start()

        read_t.join()
        write_t.join()

    print("all done")


if __name__ == "__main__":
    main()
