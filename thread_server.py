import socket
import sys
import threading


def read_fun(conn):
    while True:
        stuff = conn.recv(1024)
        if not stuff:
            break
        print("*" + stuff.decode(), end="")


def write_fun(conn):
    for line in sys.stdin:
        conn.sendall(line.encode())


def main():
    HOST = "192.168.8.100"  # Standard loopback interface address (localhost)
    PORT = 10000  # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"connection on: {conn.getsockname()}")
            read_t = threading.Thread(target=read_fun, args=(conn,))
            write_t = threading.Thread(target=write_fun, args=(conn,))
            read_t.start()
            write_t.start()
            read_t.join()

    print("all done")


if __name__ == "__main__":
    main()
