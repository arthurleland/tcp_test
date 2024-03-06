#!/usr/bin/env python3
import os
import pathlib
import selectors
import socket
import sys
import time


class ChatClient:
    def __init__(
        self,
        conn=None,
        server_address=("127.0.0.1", 10000),
        client_address=None,
    ):
        self.sel = selectors.DefaultSelector()

        if conn is None:
            if isinstance(server_address, tuple):
                self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if client_address is not None:
                    self.conn.setsockopt(
                        socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
                    )
                    self.conn.bind(client_address)
            else:
                self.conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

            self.connect(server_address)
        else:
            self.conn = conn

    def connect(self, server_addr):
        while True:
            try:
                self.conn.connect(server_addr)
                print_connection_info(self.conn)
                break
            except Exception as e:
                time.sleep(0.1)

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


class ChatServer:
    def __init__(self, server_addr=("", 10000)):
        if isinstance(server_addr, tuple):
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(server_addr)

        else:
            self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            if os.path.exists(server_addr):
                os.remove(server_addr)
            self.sock.bind(server_addr)

        self.sock.listen()

    def accept(self):
        conn, _ = self.sock.accept()
        print_connection_info(conn)
        return ChatClient(conn)


def print_connection_info(conn):
    local_host = conn.getsockname()
    remote_host = conn.getpeername()
    if conn.family is socket.AF_UNIX:
        print(
            f"*** connected: (local) '{local_host}' : ",
            f"<==> (remote) '{remote_host}'",
        )
    else:
        print(
            f"*** connected: (local) {local_host[0]}:{local_host[1]} ",
            f"<==> (remote) {remote_host[0]}:{remote_host[1]}",
        )


def run_server(server_address):
    server = ChatServer(server_address)

    while True:
        print("*** listening for connection")
        conn = server.accept()
        conn.chat()

        uinput = input("continue Y/n: ")
        if uinput.lower() != "y" and uinput != "":
            if server.sock.family == socket.AF_UNIX:
                pathlib.Path(server.sock.getsockname()).unlink()
            break


def run_client(server_address, client_address=None):
    client = ChatClient(
        server_address=server_address, client_address=client_address
    )
    client.chat()


def main():

    error_message = """
    usage:
    ./als_chat.py <mode> <address_format> <server_address> [client_address]
    \tmode = server or client
    \taddress_format = inet or unix
    \tserver_address = x.x.x.x portnum or ~/sock
    """

    # breakpoint()
    try:
        mode, address_format = sys.argv[1:3]
        if mode not in ("server", "client") or address_format not in (
            "inet",
            "unix",
        ):
            raise Exception()

        if address_format == "inet":
            server_address = (sys.argv[3], eval(sys.argv[4]))
        elif address_format == "unix":
            server_address = os.path.expanduser(sys.argv[3])

        if mode == "server":
            run_server(server_address)
        elif mode == "client":
            try:
                if address_format == "inet":
                    client_address = (sys.argv[5], eval(sys.argv[6]))
                elif address_format == "unix":
                    client_address = os.path.expanduser(sys.argv[4])
            except Exception:
                client_address = None

            run_client(
                server_address=server_address,
                client_address=client_address,
            )
    except Exception as e:
        print(error_message)
        # raise


if __name__ == "__main__":
    print(f"pid: {os.getpid()}")
    main()
