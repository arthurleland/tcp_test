import selectors
import socket
import sys
import time


class ChatSocket:
    def __init__(self, sock=None):
        self.sel = selectors.DefaultSelector()
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def read(self):
        data = self.sock.recv(1024)

        if not data:
            print("*** recv done ***")
            self.sel.unregister(self.sock)
            return

        print("recv: ", data.decode(), end="")

    def write(self):
        line = sys.stdin.readline()

        if line == "\n":
            print("*** send done ***")
            self.sel.unregister(sys.stdin)
            self.sock.shutdown(socket.SHUT_WR)
            return

        print("send: ", line, end="")
        self.sock.sendall(line.encode())

    def chat(self):
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

        while True:
            if len(self.sel.get_map()) == 0:
                print("*** chat done ***")
                self.sock.close()
                break

            events = self.sel.select(timeout=0.1)
            for key, mask in events:
                key.data()


class ChatClient(ChatSocket):
    def connect(self, server_addr, port):
        while True:
            try:
                self.sock.connect((server_addr, port))
                print_connection_info(self.sock)
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
        sock, _ = self.server.accept()
        print_connection_info(sock)
        return ChatSocket(sock)


def print_connection_info(sock):
    local_host = sock.getsockname()
    remote_host = sock.getpeername()
    print(
        f"connecting: (local) {local_host[0]}:{local_host[1]}",
        f" <==> (remote) {remote_host[0]}:{remote_host[1]}",
    )


def run_server(server_addr="", port=10000):
    server = ChatServer(server_addr, port)
    while True:
        print("*** server listening for connection ***")
        conn = server.accept()
        conn.chat()


def run_client(server_addr="127.0.0.1", port=10000):
    client = ChatClient()
    client.connect(server_addr, port)
    client.chat()


def main():
    server_addr = "192.168.107.100"
    port_num = 10000

    run_server(port=port_num)
    # run_client(server_addr=server_addr, port=port_num)
    print("*** leaving main ***")


if __name__ == "__main__":
    main()
