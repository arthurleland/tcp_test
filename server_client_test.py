import sys


def main():
    while True:
        line = sys.stdin.readline()

        if len(line) == 1:
            break
        print(line, end="")

    print("all done")


if __name__ == "__main__":
    main()
