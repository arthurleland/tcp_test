import sys


def main():
    for line in sys.stdin:
        if len(line) == 1:
            break
        print(line, end="")

    print("all done")


if __name__ == "__main__":
    main()
