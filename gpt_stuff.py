import selectors
import socket
import sys


def connect_to_server():
    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    try:
        print("attempting to connect)")
        client_socket.connect(("192.168.107.101", 10000))
        print("Connected to the server")
    except Exception as e:
        print(f"Error connecting to the server: {e}")
        sys.exit(1)


def main():
    # Create a selector
    sel = selectors.DefaultSelector()

    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Register the client socket for 'write' events (i.e., when it's ready to connect)
    sel.register(client_socket, selectors.EVENT_WRITE)

    print("Waiting for the server to be ready...")

    while True:
        # Wait for events
        events = sel.select()
        print("got event")

        for key, mask in events:
            if key.fileobj == client_socket:
                # Client socket is ready to connect
                connect_to_server()
                # Unregister the socket as it's no longer needed
                sel.unregister(client_socket)
                client_socket.close()
                sys.exit(0)


if __name__ == "__main__":
    main()
