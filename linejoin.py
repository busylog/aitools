#!/usr/bin/env python3
import sys

# first keyword is the base. with others attached
def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} filename str1,str2,...")
        sys.exit(1)

    filename = sys.argv[1]
    keywords = sys.argv[2].split(",")
    first_keyword = keywords[0]

    collected = {k: [] for k in keywords}
    has_first = False

    def flush():
        nonlocal collected, has_first
        if has_first:
            for k in keywords:
                print("".join(collected[k]),end='')
            print()
        collected = {k: [] for k in keywords}
        has_first = False

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            for k in keywords:
                if k in line:
                    if k == first_keyword:
                        flush()
                        has_first = True
                    collected[k].append(line)
                    break  # stop after first matching keyword

        flush()

if __name__ == "__main__":
    main()
