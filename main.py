#!/usr/bin/env python3
"""Write the one-line office joke entry to the output path.

The joke is held in this repository as entry.txt. This program writes
that exact line, byte for byte, to the output path (default
$MAKEFUN_OUTPUT, or /output/entry.txt when the variable is unset).
No network, no randomness: running it twice writes the same bytes.

Options:
  --output PATH   write the joke to PATH instead of the default.
  --verify        after writing, check the output is one line of
                  1 to 200 characters and print a one-line summary.
"""
import argparse
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.txt"
DEFAULT_OUT = Path(os.environ.get("MAKEFUN_OUTPUT", "/output/entry.txt"))
MAX_CHARS = 200


def validate(text: str) -> None:
    """The competition gate: UTF-8 text of 1 to 200 characters, one line."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only white space")
    if "\n" in text.rstrip("\n") or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} characters, over the {MAX_CHARS} limit")


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write the one-line office joke to the output path."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="destination path (overrides MAKEFUN_OUTPUT, "
        "default /output/entry.txt)",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="verify the output against the competition gate and "
        "print a one-line summary",
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    out = args.output if args.output is not None else DEFAULT_OUT

    if not SRC.is_file():
        print(f"source joke missing: {SRC}", file=sys.stderr)
        return 1

    text = SRC.read_text(encoding="utf-8")
    try:
        validate(text)
    except ValueError as exc:
        print(f"entry fails the gate: {exc}", file=sys.stderr)
        return 1

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")

    if args.verify:
        written = out.read_text(encoding="utf-8")
        assert written == text, "output differs from source joke"
        validate(written)
        print(f"{out}: {len(written)} characters, one line, gate OK")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
