import selectors
import socket
import sys
import time


class ChatSocket:
    def __init__(self, sock):
        self.sock = sock
        self.sel = selectors.DefaultSelector()

        self.sock.setblocking(False)
        self.sel.register(
            self.sock,
            selectors.EVENT_READ,
            data=self.read,
        )
        self.sel.register(
            sys.stdin,
            selectors.EVENT_READ,
            data=self.write,
        )

    def read(self):
        data = self.sock.recv(1024)

        if not data:
            print("recv done")
            self.sel.unregister(self.sock)
            return

        print("recv: ", data.decode(), end="")

    def write(self):
        line = sys.stdin.readline()

        if line == "\n":
            print("send done")
            self.sel.unregister(sys.stdin)
            self.sock.shutdown(socket.SHUT_WR)
            return

        print("send: ", line, end="")
        self.sock.sendall(line.encode())

    def chat(self):
        while True:
            if len(self.sel.get_map()) == 0:
                print("chat done")
                self.sock.close()
                break

            events = self.sel.select(timeout=0.1)
            for key, mask in events:
                key.data()


class ChatClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, server_addr, port):
        while True:
            try:
                self.sock.connect((server_addr, port))
                print(f"connected via {self.sock.getsockname()}")
                return ChatSocket(self.sock)
            except Exception as e:
                time.sleep(0.1)


class ChatServer:
    def __init__(self, server_addr, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((server_addr, port))
        self.server.listen()

    def accept(self):
        self.sock, addr = self.server.accept()
        print("accepted", self.sock, "from", addr)
        return ChatSocket(self.sock)


def run_server(server_addr, port):
    server = ChatServer(server_addr, port)
    while True:
        print("*** server listening for connection ***")
        conn = server.accept()
        conn.chat()


def run_client(server_addr, port):
    client = ChatClient()
    conn = client.connect(server_addr, port)
    conn.chat()


def main():
    server_addr = "192.168.107.100"
    port = 10000

    run_server(server_addr, port)
    # run_client(server_addr,port)
    print("leaving main")


if __name__ == "__main__":
    main()