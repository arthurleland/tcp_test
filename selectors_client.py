import selectors
import socket
import sys


def accept(soc):
    conn, addr = soc.accept()
    print("accepted", conn, "from", addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)


def read(conn):
    data = conn.recv(1024)

    if not data:
        print("recv close", conn)
        sel.unregister(conn)
        sel.unregister(sys.stdin)
        conn.close()
        return

    print("recv: ", data.decode(), end="")


def write(conn):
    line = sys.stdin.readline()

    if line == "\n":
        print("send close")
        sel.unregister(conn)
        sel.unregister(sys.stdin)
        conn.close()
        return

    print("snd: ", line, end="")
    conn.sendall(line.encode())


def main():
    sel = selectors.DefaultSelector()

    SERVER = "192.168.107.100"
    PORT = 10000
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    soc.connect((SERVER, PORT))
    print(f"connected via {soc.getsockname()}")

    soc.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, (read, soc))
    sel.register(sys.stdin, selectors.EVENT_READ, (write, soc))

    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data[0]
            callback(key.data[1])

    print("all done")


if __name__ == "__main__":
    main()