import select
import sys
import time


def line_ready():
    read_ready, _, _ = select.select([sys.stdin], [], [], 0)
    return sys.stdin in read_ready


def var_args(arg1):
    print(arg1)
    print(args)


def main():
    a = (1, 2)
    var_args(1, *a[2:])

    while True:
        if line_ready():
            line = sys.stdin.readline()
            if line == "\n":
                break
            print("\nline is ready: ", line)
        else:
            print("*", end="")

        time.sleep(0.1)


if __name__ == "__main__":
    main()
