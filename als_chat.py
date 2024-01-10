import selectors
import socket
import sys
import time


class SocketMixin:
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


class ChatClient(SocketMixin):
    def __init__(self, server_addr, port):
        self.sel = selectors.DefaultSelector()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        self.server_addr = server_addr
        self.port = port

    def connect(self):
        while True:
            try:
                self.sock.connect((self.server_addr, self.port))
                print(f"connected via {self.sock.getsockname()}")

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
                break
            except Exception as e:
                time.sleep(0.1)


class ChatServer(SocketMixin):
    def __init__(self, server_addr, port):
        self.sel = selectors.DefaultSelector()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((server_addr, port))
        self.server.listen()

    def accept(self):
        self.sock, addr = self.server.accept()
        print("accepted", self.sock, "from", addr)
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


def run_server(server_addr, port):
    server = ChatServer(server_addr, port)
    server.accept()
    server.chat()


def run_client(server_addr, port):
    server = ChatClient(server_addr, port)
    server.connect()
    server.chat()


def main():
    server_addr = "192.168.107.100"
    port = 10000

    run_server(server_addr, port)
    # run_client(server_addr,port)
    print("leaving main")


if __name__ == "__main__":
    main()
