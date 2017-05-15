#!/usr/bin/env python3
import util
import unittest

class UtilTests(unittest.TestCase):
    def test_normalize(self):
        word = "?WoRD!"
        self.assertEqual(util.normalize(word), "word")
    def test_normalize_internal_punctuation(self):
        word = "shouldn't."
        self.assertEqual(util.normalize(word), "shouldn't")
    def test_normalize_whitespace(self):
        word = "   word\n"
        self.assertEqual(util.normalize(word), "word")
    def test_normalize_punctuation(self):
        word = "!WORD! "
        self.assertEqual(util.normalize(word), "word")
    def test_in_dict(self):
        self.assertTrue(util.in_dict("!WORD! "))
    def test_not_in_dict(self):
        self.assertFalse(util.in_dict("asdf"))
    def test_get_syllable_count(self):
        word = "Syllable."
        self.assertEqual(3, util.get_syllable_count(word))

def main():
    unittest.main()

if __name__ == '__main__':
    main()
