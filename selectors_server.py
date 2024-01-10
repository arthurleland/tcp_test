import selectors
import socket
import sys


def read(conn, sel):
    data = conn.recv(1024)

    if not data:
        print("recv close", conn)
        sel.unregister(conn)
        sel.unregister(sys.stdin)
        conn.close()
        return

    print("recv: ", data.decode(), end="")


def write(conn, sel):
    line = sys.stdin.readline()

    if line == "\n":
        print("send close")
        sel.unregister(conn)
        sel.unregister(sys.stdin)
        conn.close()
        return

    print("send: ", line, end="")
    conn.sendall(line.encode())


def main():
    sel = selectors.DefaultSelector()

    SERVER = "192.168.107.100"
    PORT = 10000
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.bind((SERVER, PORT))
    soc.listen()

    conn, addr = soc.accept()
    print("accepted", conn, "from", addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, (read, conn, sel))
    sel.register(sys.stdin, selectors.EVENT_READ, (write, conn, sel))

    while True:
        if len(sel.get_map()) == 0:
            break

        events = sel.select(timeout=0.1)
        for key, mask in events:
            callback = key.data[0]
            callback(*key.data[1:])

    print("all done")


if __name__ == "__main__":
    main()
