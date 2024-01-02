import socket
import sys


def main():
    HOST = "192.168.0.124"  # The server's hostname or IP address
    PORT = 10000  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((HOST, PORT))
        print(f"connected via {s.getsockname()}")

        for line in sys.stdin:
            if line == "\n":
                break

            s.sendall(line.encode())
            data = s.recv(1024)
            print(f"Received {data!r}")

    print("all done")


if __name__ == "__main__":
    main()
