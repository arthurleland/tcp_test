import socket
import sys


def main()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            # soc.bind((CLIENT, 0))
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
