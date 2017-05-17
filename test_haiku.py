#!/usr/bin/env python3
import util
import markov
import haiku
import unittest

class HaikuTests(unittest.TestCase):

    def assert_syllable_count(self, expected_count, line):
        words = line.split()
        total_syllables = sum([util.get_syllable_count(w) for w in words])
        self.assertEqual(expected_count, total_syllables)
    def test_generate_first_line(self):
        text = "Just five syllables"
        chain = markov.MarkovChain(2)
        chain.update(text)
        line = haiku.generate_line(chain, 5)
        self.assertEqual(text, line)
    def test_generate_later_line(self):
        text = "Just five syllables in the first line of the text"
        chain = markov.MarkovChain(4)
        chain.update(text)
        line = haiku.generate_line(chain, 7, "Just five syllables")
        self.assertEqual("in the first line of the text", line)
    def test_generate_line_fail(self):
        text = "Can't make this line correctly"
        chain = markov.MarkovChain(2)
        chain.update(text)
        with self.assertRaises(RuntimeError):
            haiku.generate_line(chain, 5)
    def test_end_with_punctuation(self):
        text = ("This haiku would be"
        "perfect except that it has"
        "too many syllables on the last line.")
        chain = markov.MarkovChain(2)
        chain.update(text)
        with self.assertRaises(RuntimeError):
            haiku.generate_haiku_attempt(chain)
    def test_generate_haiku_attempt(self):
        chain = markov.MarkovChain.from_files(["test/test4.txt"], 4)
        poem = haiku.generate_haiku_attempt(chain)
        lines = poem.split("\n")
        #validate number of lines
        self.assertEqual(3, len(lines))
        #validate number of syllables: line one
        self.assert_syllable_count(5, lines[0])
        #line two
        self.assert_syllable_count(7, lines[1])
        #line three
        self.assert_syllable_count(5, lines[2])
        #make sure it ends with punctuation
        self.assertTrue(lines[2][-1] in "?.!")
    def test_generate_haiku(self):
        pass
        expected_haiku = ("Then you can create\n"
        "a perfect haiku using\n"
        "this example text.")
        chain = markov.MarkovChain.from_files(["test/test5.txt"], 4)
        actual_haiku = haiku.generate_haiku(chain)
        self.assertEqual(expected_haiku, actual_haiku)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
