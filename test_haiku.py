#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import util
import markov
import haiku
import unittest


class HaikuTests(unittest.TestCase):

    def _assert_syllable_count(self, expected_count, line):
        words = line.split()
        total_syllables = sum([util.get_syllable_count(w) for w in words])
        self.assertEqual(expected_count, total_syllables)

    def test_get_next_word_success(self):
        text = "The next word is dog."
        chain = markov.MarkovChain.from_string(text)
        word = haiku.get_next_word(chain, "The next word is", 2)
        self.assertEqual("dog.", word)

    def test_get_next_word_failure(self):
        text = "The next word is multisyllabic."
        chain = markov.MarkovChain.from_string(text)
        with self.assertRaises(RuntimeError):
            haiku.get_next_word(chain, "The next word is", 2)

    def test_generate_first_line(self):
        text = "Just five syllables"
        chain = markov.MarkovChain.from_string(text)
        line = haiku.generate_line(chain, 5)
        # only valid line is original text
        self.assertEqual(text, line)

    def test_generate_later_line(self):
        text = "Just five syllables in the first line of the text"
        chain = markov.MarkovChain.from_string(text)
        line = haiku.generate_line(chain, 7, "Just five syllables")
        # only valid line is original text
        self.assertEqual("in the first line of the text", line)

    def test_generate_line_fail(self):
        # can't generate 5 syllable line from this
        text = "Can't make this line correctly"
        chain = markov.MarkovChain.from_string(text)
        with self.assertRaises(RuntimeError):
            haiku.generate_line(chain, 5)

    def test_generate_haiku_attempt_fail(self):
        text = ("This haiku would be"
                "perfect except that it has"
                "too many syllables on the last line.")
        chain = markov.MarkovChain.from_string(text)
        with self.assertRaises(RuntimeError):
            haiku.generate_haiku_attempt(chain)

    def test_generate_haiku_attempt_success(self):
        # Test input allows for multiple possible haiku
        text = ("This is already\n"
                "a perfectly fine haiku\n"
                "so just repeat it!\n"
                "This is already\n"
                "an acceptable haiku\n"
                "so just use this one.")
        chain = markov.MarkovChain.from_string(text)
        poem = haiku.generate_haiku_attempt(chain)
        lines = poem.split("\n")
        # validate number of lines and syllable counts
        self.assertEqual(3, len(lines))
        self._assert_syllable_count(5, lines[0])
        self._assert_syllable_count(7, lines[1])
        self._assert_syllable_count(5, lines[2])
        # make sure it ends with punctuation
        self.assertTrue(lines[2][-1] in "?.!")

    def test_generate_haiku(self):
        input_lines = ["You have to skip the first sentence.",
                       "Then you can create",
                       "a perfect haiku using",
                       "this example text."]
        expected_haiku = "\n".join(input_lines[1:])
        chain = markov.MarkovChain.from_string(" ".join(input_lines))
        actual_haiku = haiku.generate_haiku(chain)
        self.assertEqual(expected_haiku, actual_haiku)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
