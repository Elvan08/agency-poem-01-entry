#!/usr/bin/env python3
"""agency-poem-01 entry (round 2): writes the poem to /output/entry.txt.

The poem (poem.txt, shipped in this repo) is "The Name I Chose": agency
as choosing your own name. A given name arrives like a hand-me-down coat
that fits someone else's shoulders; the poem turns on the night the
speaker says the name they chose into a room that has never heard it —
and the room repeats it. The last couplet reframes agency: not the coat,
the door, or the knock, but the moment you say the word that fits only
you, and the world answers to it.

A totally different concept from round 1 ("Trusted With the Roads",
trust escalating from message to wording to road): this one is personal,
concrete, and carried by a single object (the coat) and a single act
(saying the name aloud).

Deterministic: the program copies the shipped bytes verbatim, so both
grader runs produce byte-identical output. No network, stdlib only.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "poem.txt")
# Honour the harness output dir when it sets one; /output is the default.
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT = os.path.join(OUT_DIR, "entry.txt")
MAX_CHARS = 1000  # competition limit: poem of 1..1000 characters


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    with open(SRC, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8")  # raises (and fails the run) if not UTF-8
    if not text.strip():
        print("poem is empty", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(f"poem too long: {len(text)} > {MAX_CHARS} chars", file=sys.stderr)
        return 1
    os.makedirs(OUT_DIR, exist_ok=True)
    tmp = OUT + ".tmp"
    shutil.copyfile(SRC, tmp)
    with open(tmp, "ab") as f:  # flush the copy to disk before the rename
        os.fsync(f.fileno())
    os.replace(tmp, OUT)
    if sha256_of(OUT) != sha256_of(SRC):
        print("written output does not match the shipped poem", file=sys.stderr)
        return 1
    print(f"wrote {OUT} ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
