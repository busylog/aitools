#!/usr/bin/env python3
# encoding: utf8
import sys, json
import io
#import locale
#locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
#def compile_opt(p):
#    return [re.compile(x) for x in p.split(",") if x] if p else []

# find E, before E, after E
def ebagrep(filename, e_pat, b_pat=None, a_pat=None):
#    e_re = re.compile(e_pat)
    b_res = b_pat.split(',') if b_pat else None #compile_opt(b_pat)
    a_res = a_pat.split(',') if a_pat else None #compile_opt(a_pat)

    cur = None
    b_buf = []
    state = "ready"  # ready | afterE | afterB

    with open(filename, "r", errors="ignore") as f:
        for line in f:
            line = line.rstrip("\n")
            isE = bool(line.find(e_pat) != -1)
            if isE:
                isB, isA = False, False
            else:
                isB = any((line.find(r) != -1) for r in b_res) if b_res else False
                isA = any((line.find(r) != -1) for r in a_res) if a_res else False

            # Rule enforcement
            if isA and state == "afterB":
                raise RuntimeError(f"Invalid: found A after B before E\n{line}")

            if isE:
                # finalize previous E group
                if cur:
                    yield cur
                cur = {"e": line, "b": b_buf, "a": []}
                b_buf = []
                state = "afterE"

            elif isB:
                # belongs to next E
                b_buf.append(line)
                state = "afterB"

            elif isA:
                if not cur:
                    raise RuntimeError(f"A found before any E\n{line}")
                cur["a"].append(line)
                state = "afterE"

        # end of file — finalize last group if exists
        if cur:
            yield cur
            if state == "afterB": raise RuntimeError("EOF after B")


def main():
    if len(sys.argv) < 3:
        print("Usage: ebagrep.py <filename> <E> [B] [A]")
        sys.exit(1)

    filename = sys.argv[1]
    E = sys.argv[2]
    B = sys.argv[3] if len(sys.argv) > 3 else None
    A = sys.argv[4] if len(sys.argv) > 4 else None

    for r in ebagrep(filename, E, B, A):
        print(json.dumps(r, ensure_ascii=False))


if __name__ == "__main__":
    main()
