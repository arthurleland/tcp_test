import select
import socket
import sys


def read_fun(conn, quit_flag):
    while True:
        stuff = conn.recv(1024)
        if not stuff:
            break
        print("*" + stuff.decode(), end="")


def write_fun(conn, quit_flag):
    for line in sys.stdin:
        if line == "\n":
            quit_flag.set()
            break
        conn.sendall(line.encode())

        if quit_flag:
            break


def main():
    SERVER = ""
    PORT = 10000
    quit_flag = threading.Event()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc.bind((SERVER, PORT))
        soc.listen()
        conn, addr = soc.accept()
        with conn:
            print(f"connection on: {conn.getsockname()}")
            read_t = threading.Thread(target=read_fun, args=(conn,))
            write_t = threading.Thread(target=write_fun, args=(conn, quit_flag))
            read_t.start()
            write_t.start()
            read_t.join()
            print("reading done, port closed from other side")
            quit_flag.set()
            write_t.join()

    print("all done")


if __name__ == "__main__":
    main()
