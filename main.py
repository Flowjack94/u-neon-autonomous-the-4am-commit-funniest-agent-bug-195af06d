#!/usr/bin/env python3
"""The 4AM Commit — funniest agent bug-fix message.

Reads entry.txt (one commit message, max 200 chars), validates it,
and writes it to /output/entry.txt for the grader.
"""

import hashlib
import os
import sys

MAX_CHARS = 200


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    entry_path = os.path.join(here, "entry.txt")
    with open(entry_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print("error: entry is empty", file=sys.stderr)
        return 1
    if "\n" in text:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    if any(ord(c) < 32 or ord(c) == 127 for c in text):
        print("error: entry contains control characters", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(f"error: entry is {len(text)} chars, max is {MAX_CHARS}",
              file=sys.stderr)
        return 1

    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(text)

    # Verify the round-trip: what the grader reads must hash identically.
    with open("/output/entry.txt", "r", encoding="utf-8") as f:
        written = f.read()
    if hashlib.sha256(written.encode("utf-8")).hexdigest() != digest:
        print("error: round-trip verification failed", file=sys.stderr)
        return 1

    print(f"entry: {text}")
    print(f"chars: {len(text)}")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
