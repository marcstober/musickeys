import unittest

from musickeycomputer import (
    compute_keys,
    compute_keys_with_flats,
    compute_keys_with_sharps,
    compute_order_of_flats,
    compute_order_of_sharps,
    get_note_in_key,
)


class TestMusicKeys(unittest.TestCase):

    def test_compute_order_of_sharps(self):
        oos = compute_order_of_sharps()
        self.assertEqual(oos, "FCGDAEB")

    def test_compute_order_of_flats(self):
        oof = compute_order_of_flats()
        self.assertEqual(oof, "BEADGCF")

    def test_get_note_in_key(self):
        nik = get_note_in_key("D", "F")
        self.assertEqual(nik, "F#")

    def test_get_note_in_key_invalid_note_raises_value_error(self):
        for invalid_note in ["f", "Eb"]:
            with self.subTest(note=invalid_note):
                with self.assertRaises(ValueError):
                    get_note_in_key("D", invalid_note)

    def test_compute_keys_6_6(self):
        # 7 flat keys (Gb through C) + 6 sharp keys (G through F#) = 13 total.
        keys = compute_keys(6, 6)
        self.assertEqual(len(keys), 13)
        self.assertEqual(keys[0].number_of_accidentals, 6)
        self.assertEqual(keys[-1].number_of_accidentals, 6)

    def test_compute_keys_6_5(self):
        # 7 flat keys + 5 sharp keys (G through B, max_sharps=6 gives [1:] = 5) = 12 total.
        keys = compute_keys(6, 5)
        self.assertEqual(len(keys), 12)
        self.assertEqual(keys[0].number_of_accidentals, 6)
        self.assertEqual(keys[-1].number_of_accidentals, 5)

    def test_compute_keys_5_6(self):
        # 6 flat keys (Db through C) + 6 sharp keys (G through F#) = 12 total.
        keys = compute_keys(5, 6)
        self.assertEqual(len(keys), 12)
        self.assertEqual(keys[0].number_of_accidentals, 5)
        self.assertEqual(keys[-1].number_of_accidentals, 6)

    def test_compute_keys_0_0(self):
        # No sharps or flats requested; result must be only the key of C major.
        keys = compute_keys(0, 0)
        print(keys)
        self.assertEqual(len(keys), 1)
        self.assertEqual(keys[0].key, "C")
        self.assertEqual(keys[0].number_of_accidentals, 0)

    def test_compute_keys_with_sharps(self):
        keys = compute_keys_with_sharps(6)
        keys_keys = [k.key for k in keys]
        self.assertEqual(keys_keys, ["G", "D", "A", "E", "B", "F#"])
        self.assertEqual(keys[5].number_of_accidentals, 6)

    def test_compute_keys_with_flats(self):
        keys = compute_keys_with_flats(7)
        self.assertEqual(keys[0].number_of_accidentals, 7)
        # IMPORTANT! The name of the key is spelled Cb, not B!
        self.assertEqual(keys[0].key, "Cb")

    def test_compute_keys_more_keys_than_possible(self):
        keys = compute_keys(10, 10)
        # maximum number of keys, can't compute more than 7 flats or sharps
        # (our algorithm would go into an infinite loop, but also such keys aren't really a thing)
        self.assertEqual(len(keys), 15)

    def test_compute_relative_minor(self):
        keys = compute_keys(0, 0)
        c_major = keys[0]
        self.assertEqual(c_major.relative_minor, "A")

    def test_compute_relative_minor_with_flats(self):
        keys = compute_keys(1, 0)
        f_major = keys[0]
        self.assertEqual(f_major.relative_minor, "D")


if __name__ == "__main__":
    unittest.main()
