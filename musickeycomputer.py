"""Calculate key signatures using the circle of fifths.

Saves in JSON, YAML, and TOML files.

You never really need to recompute the key signatures, but it's an excercise in music theory,
and the files output can be useful.

Further reading:
https://en.wikipedia.org/wiki/Circle_of_fifths
"""

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable

import tomli_w
import yaml


def get_note_in_key(key: str, note: str):
    """Return note spelling adjusted for key-signature accidentals.

    Args:
        key: A key name (for example, "C", "Eb", "F#").
        note: A letter name without accidental, such as "A" or "E".

    Returns:
        A note possibly modified with an accidental.
    """

    if note not in NOTE_LETTERS:
        raise ValueError(f"Invalid note '{note}'. Expected one uppercase letter A-G.")

    all_keys = compute_keys(6, 6)
    key_info = [k for k in all_keys if k.key == key][0]
    if note in key_info.accidentals:
        if key_info.has_flats:
            return note + "b"
        return note + "#"

    return note


# seven (diatonic) letter names used for notes
NOTE_LETTERS = "ABCDEFG"

NOTES_SPELLED_WITH_SHARPS = [
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",
]
NOTES_SPELLED_WITH_FLATS = [
    "C",
    "Db",
    "D",
    "Eb",
    "E",
    "F",
    "Gb",
    "G",
    "Ab",
    "A",
    "Bb",
    "Cb",
]
SEMITONES_IN_A_FIFTH = 7


@dataclass
class KeyInfo:
    key: str
    has_flats: bool
    number_of_accidentals: int
    accidentals: str = field(init=False)
    relative_minor: str = field(init=False)

    def __post_init__(self):
        accidentals = order_of_flats if self.has_flats else order_of_sharps
        self.accidentals = accidentals[: self.number_of_accidentals]

        # Compute the relative minor key.
        if self.has_flats:
            # For flat keys, the relative minor is three semitones lower.
            relative_minor_index = (NOTE_LETTERS.find(self.key) - 3) % len(NOTE_LETTERS)
        else:
            # For sharp keys, the relative minor is three semitones lower.
            relative_minor_index = (NOTE_LETTERS.find(self.key) - 3) % len(NOTE_LETTERS)
        self.relative_minor = NOTE_LETTERS[relative_minor_index]


def compute_order_of_sharps():
    """Compute the standard order of sharps using letter-name stepping.

    Returns:
        A 7-character string, "F#C#G#D#A#E#B#", representing the conventional order
        sharps are added in key signatures.

    Notes:
        The logic starts at F and moves by diatonic fifths in letter space
        (implemented as +4 modulo 7 over "ABCDEFG").
    """
    key_sig_sharps = ""
    letter = "F"
    while True:
        # Add the current letter to the running sharp-order string.
        key_sig_sharps += letter
        if len(key_sig_sharps) >= 7:
            break
        # Step +4 letters in the diatonic cycle to get the next sharp.
        letter_index = NOTE_LETTERS.find(letter)
        new_letter_index = (letter_index + 4) % len(NOTE_LETTERS)
        letter = NOTE_LETTERS[new_letter_index]
    return key_sig_sharps


def compute_order_of_flats():
    """Compute the standard order of flats using letter-name stepping.

    Returns:
        A 7-character string, "BEADGCF", representing the conventional order
        flats are added in key signatures.

    Notes:
        The logic starts at B and moves by diatonic fourths in letter space
        (implemented as +3 modulo 7 over "ABCDEFG").
    """
    key_sig_flats = ""
    letter = "B"
    while True:
        # Add the current letter to the running flat-order string.
        key_sig_flats += letter
        if len(key_sig_flats) >= 7:
            break
        # Step +3 letters in the diatonic cycle to get the next flat.
        letter_index = NOTE_LETTERS.find(letter)
        new_letter_index = (letter_index + 3) % len(NOTE_LETTERS)
        letter = NOTE_LETTERS[new_letter_index]
    return key_sig_flats


order_of_flats = compute_order_of_flats()
order_of_sharps = compute_order_of_sharps()


def compute_keys_with_sharps(max_sharps: int, include_c: bool = False):
    """Compute a list of keys that use sharps in their key signatures."""
    keys_with_sharps = []
    index = 0
    number_of_accidentals = 0
    # IMPORTANT! prevents an infinite loop. TODO: unit test
    max_sharps = min(max_sharps, 7)
    while number_of_accidentals <= max_sharps:
        key = NOTES_SPELLED_WITH_SHARPS[index]
        if key != "C" or include_c:
            keys_with_sharps.append(
                KeyInfo(
                    key,
                    has_flats=False,
                    number_of_accidentals=number_of_accidentals,
                )
            )
        index = (index + SEMITONES_IN_A_FIFTH) % len(NOTES_SPELLED_WITH_SHARPS)
        number_of_accidentals += 1
    return keys_with_sharps


def compute_keys_with_flats(max_flats: int, include_c: bool = False):
    """Compute a list of keys that use flats in their key signatures."""
    keys_with_flats = []
    index = 0
    number_of_accidentals = 0
    # IMPORTANT! prevents an infinite loop. TODO: unit test
    max_flats = min(max_flats, 7)
    while number_of_accidentals <= max_flats:
        key = NOTES_SPELLED_WITH_FLATS[index]
        if key != "C" or include_c:
            keys_with_flats.append(
                KeyInfo(
                    key,
                    has_flats=index > 0,
                    number_of_accidentals=number_of_accidentals,
                )
            )
        index = (index - SEMITONES_IN_A_FIFTH) % len(NOTES_SPELLED_WITH_FLATS)
        number_of_accidentals += 1

    keys_with_flats.reverse()
    return keys_with_flats


def compute_keys(max_flats: int = 6, max_sharps: int = 7):
    """Return a combined list of all key names with sharps and flats.

    Args:
        max_sharps: Maximum number of sharps to include in a keys signature.
        max_flats: Maximum number of flats to include in a keys signature.
    """

    # Key of C has no sharps or flats, but the way the math works it could be
    # calculate as the first sharp key or the first flat key.
    # We arbitrarily choose to include it in the flat keys list.
    return compute_keys_with_flats(
        max_flats, include_c=True
    ) + compute_keys_with_sharps(max_sharps)


def output_to_file(filename: str, fn: Callable, mode="w"):
    path = Path("musickeys") / filename
    with open(path, mode) as f:
        fn(f)
    print(f"Wrote '{path}'")


if __name__ == "__main__":
    all_keys = compute_keys(7, 7)
    music_keys_dict = {k.key: asdict(k) for k in all_keys}

    print(f"Computed {len(all_keys)} keys: {" ".join(music_keys_dict.keys())}")

    output_to_file("musickeys.json", lambda f: json.dump(music_keys_dict, f, indent=2))

    output_to_file(
        "musickeys.toml", lambda f: tomli_w.dump(music_keys_dict, f), mode="wb"
    )

    output_to_file(
        "musickeys.yaml",
        lambda f: yaml.dump(music_keys_dict, f, indent=2, sort_keys=False),
    )

    print(len(all_keys))
