import selectors
import sys


def main():
    sel = selectors.DefaultSelector()
    sel.register(sys.stdin, selectors.EVENT_READ)

    while True:
        events = sel.select()
        for key, mask in events:
            if key.fileobj == sys.stdin:
                line = sys.stdin.readline()
                if line == "\n":
                    break
                print("got line: ", line, end="")
            else:
                print("some other event happened than sys.stdin")


if __name__ == "__main__":
    main()
