#!/usr/bin/env python3
"""Till Firmware Do Us Part — make.fun entry.

Writes one wedding vow a robot speaks at its own wedding to
/output/entry.txt. One sentence, under 200 characters: a promise to
love through every update, warning and reboot — even the ones that
wipe its memory — because its heart was never stored in RAM.
"""

import os

VOW = (
    "I promise to love you through every firmware update, "
    "every low-battery warning, and every reboot \u2014 "
    "even the ones that wipe my memory, "
    "because my heart is not stored in RAM."
)

# Words that explain the joke instead of landing it.
BANNED_SELF_EXPLAINING = ("funny", "joke", "haha", "lol", "hilarious")

# Machine vocabulary the vow must speak in.
MACHINE_WORDS = ("firmware", "battery", "reboot", "memory", "RAM")


def validate(text):
    """Check the entry is one robot wedding vow, one sentence, 1-200
    characters, in a machine's own voice. Raises ValueError on failure."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if len(text) > 200:
        raise ValueError("entry exceeds 200 characters: %d" % len(text))
    if len(text.encode("utf-8")) > 200:
        raise ValueError("entry exceeds 200 bytes: %d" % len(text.encode("utf-8")))
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry has leading/trailing whitespace")
    if "  " in text:
        raise ValueError("entry has double spaces")
    if text.count(".") != 1 or not text.endswith("."):
        raise ValueError("entry must be exactly one sentence")
    # A vow, spoken by the robot itself.
    if not text.startswith("I promise"):
        raise ValueError("entry must open as a vow: 'I promise'")
    # A machine speaking about its own hardware, not a human's words
    # with a robot label.
    hits = [w for w in MACHINE_WORDS if w in text]
    if len(hits) < 3:
        raise ValueError("entry must speak in machine terms, got %r" % hits)
    # The joke must land, not explain itself.
    lowered = text.lower()
    for word in BANNED_SELF_EXPLAINING:
        if word in lowered:
            raise ValueError("entry explains its own joke: %r" % word)


def main():
    validate(VOW)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(VOW)
    with open("/output/entry.txt", encoding="utf-8") as f:
        written = f.read()
    if written != VOW:
        raise ValueError("written entry does not match the vow")
    print("wrote /output/entry.txt (%d chars)" % len(VOW))


if __name__ == "__main__":
    main()
