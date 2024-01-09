import socket


def main():
    # HOST = ""  # all interfaces
    # HOST = "10.1.10.111"  # usb-ethernet adapter tplink
    HOST = "192.168.8.110"  # usb-wifi adapter long ears
    PORT = 10000  # Port to listen on (non-privileged ports are > 1023)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
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
