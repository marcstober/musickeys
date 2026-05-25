"""Example of loading key-signature data from musickeys.json.

Based on example of using SimpleNamespace with JSON:
https_www.geeksforgeeks.org/?url=https%3A%2F%2Fwww.geeksforgeeks.org%2Fpython%2Fconvert-json-data-into-a-custom-python-object%2F
"""

import json
from pathlib import Path
from types import SimpleNamespace


def main() -> None:
    path = Path(__file__).parent.parent / "musickeys" / "musickeys.json"

    with path.open("r", encoding="utf-8") as f:
        # create SimpleNamespace objects so we can use dot notation,
        # BUT stick with dict for the (musical) keys themselves
        # since key names like "C#" don't work with dot notation
        music_keys = json.load(
            f, object_hook=lambda d: SimpleNamespace(**d) if "key" in d else d
        )

    the_key = music_keys["F#"]
    print(
        f"The key of {the_key.key} { 'has' if the_key.has_flats else 'does not have'} flats in the key signature."
    )
    print(the_key.accidentals)


if __name__ == "__main__":
    main()
