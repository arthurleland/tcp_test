import socket
import sys
import threading


def read_fun(conn, quit_flag):
    while True:
        stuff = conn.recv(1024)
        if not stuff:
            quit_flag.set()
            break
        print("*" + stuff.decode(), end="")


def write_fun(conn, quit_flag):
    for line in sys.stdin:
        conn.sendall(line.encode())
        if quit_flag:
            break


def main():
    hostname = "arthurschiro.com"
    PORT = 10000

    if hostname is not None:
        SERVER = socket.gethostbyname(hostname)

    quit_flag = threading.Event()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        soc.connect((SERVER, PORT))
        print(f"connected on: {soc.getsockname()}")

        read_t = threading.Thread(target=read_fun, args=(soc, quit_flag))
        write_t = threading.Thread(target=write_fun, args=(soc, quit_flag))
        read_t.start()
        write_t.start()
        read_t.join()
        write_t.join()

    print("all done")


if __name__ == "__main__":
    main()
