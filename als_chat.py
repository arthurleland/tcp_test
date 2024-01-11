import selectors
import socket
import sys
import time


class ChatConnection:
    def __init__(self, conn=None):
        self.sel = selectors.DefaultSelector()
        if conn is None:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.conn = conn

    def read(self):
        data = self.conn.recv(1024)

        if not data:
            print("*** recv done")
            self.sel.unregister(self.conn)
            return

        print("recv: ", data.decode(), end="")

    def write(self):
        line = sys.stdin.readline()

        if line == "\n":
            print("*** send done")
            self.sel.unregister(sys.stdin)
            self.conn.shutdown(socket.SHUT_WR)
            return

        # print("send: ", line, end="")
        self.conn.sendall(line.encode())

    def chat(self):
        self.conn.setblocking(False)

        self.sel.register(
            self.conn,
            selectors.EVENT_READ,
            data=self.read,
        )
        self.sel.register(
            sys.stdin,
            selectors.EVENT_READ,
            data=self.write,
        )

        while True:
            if len(self.sel.get_map()) == 0:
                print("*** chat done")
                self.conn.close()
                break

            events = self.sel.select(timeout=0.1)
            for key, mask in events:
                key.data()


class ChatClient(ChatConnection):
    def connect(self, server_addr, port):
        while True:
            try:
                self.conn.connect((server_addr, port))
                print_connection_info(self.conn)
            except Exception as e:
                time.sleep(0.1)


class ChatServer:
    def __init__(self, server_addr, port):
        self.sel = selectors.DefaultSelector()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((server_addr, port))
        self.sock.listen()
        self.sock.setblocking(False)

        self.sel.register(
            self.sock,
            selectors.EVENT_READ,
        )

    def accept(self, timeout=0.1):
        events = self.sel.select(timeout=timeout)
        if len(events) > 0:
            conn, _ = events[0][0].fileobj.accept()
            print_connection_info(conn)
            return ChatConnection(conn)
        return None


def print_connection_info(conn):
    local_host = conn.getsockname()
    remote_host = conn.getpeername()
    print(
        f"*** connected: (local) {local_host[0]}:{local_host[1]}",
        f" <==> (remote) {remote_host[0]}:{remote_host[1]}",
    )


def run_server(server_addr="", port=10000):
    server = ChatServer(server_addr, port)
    # sel = selectors.DefaultSelector()
    # sel.register(sys.stdin, selectors.EVENT_READ)

    count = 0
    while True:
        if count == 0:
            print("*** listening for connection")
            print("*** press enter to quit")
            count += 1

        conn = server.accept(timeout=0.1)
        if conn is not None:
            conn.chat()
            count = 0

        # events = sel.select(timeout=0.1)
        # if len(events) > 0:
        #     return


def run_client(server_addr="127.0.0.1", port=10000):
    client = ChatClient()
    client.connect(server_addr, port)
    client.chat()


def main():
    server_addr = "192.168.107.100"
    port_num = 10000

    run_server(port=port_num)
    # run_client(server_addr=server_addr, port=port_num)
    print("*** leaving main")


if __name__ == "__main__":
    main()
