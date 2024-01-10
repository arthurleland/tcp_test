import socket


def main():
    # SERVER = ""  # all interfaces
    # SERVER = "10.1.10.111"
    SERVER = "192.168.107.100"
    PORT = 10000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((SERVER, PORT))
    s.listen()
    conn, addr = s.accept()
    try:
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"received {data!r}")
                conn.sendall(data.upper())
        print("connection closed")
    finally:
        pass


if __name__ == "__main__":
    main()
