import socket
import sys


def main():
    # SERVER = "192.168.12.102"
    SERVER = "10.1.10.100"
    CLIENT = "192.168.0.128"
    PORT = 10000

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            soc.bind((CLIENT, 0))
            soc.connect((SERVER, PORT))
            print(f"connected via {soc.getsockname()}")

            for line in sys.stdin:
                if line == "\n":
                    break

                soc.sendall(line.encode())
                data = soc.recv(1024)
                print(f"Received {data!r}")
    finally:
        pass

    print("all done")


if __name__ == "__main__":
    main()
