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

    def test_strip_punctuation(self):
        """Strip out unclosed quotation mark"""
        text = "\"Quote"
        self.assertEqual("Quote", util.strip_straight_quotes(text))

    def test_strip_balanced_punctuation(self):
        """Don't modify balanced quotation marks"""
        text = "\"Quote\""
        self.assertEqual(text, util.strip_straight_quotes(text))

    def test_strip_third_quote(self):
        """Remove extra, unclosed quote, but not first closed quotes"""
        text = "She said \"foo.\" Then he said \"Bar "
        self.assertEqual("She said \"foo.\" Then he said Bar ",
                         util.strip_straight_quotes(text))

    def test_strip_parentheses(self):
        """Remove unclosed parenthesis"""
        text = "(Parentheses"
        self.assertEqual("Parentheses", util.strip_parens(text))

    def test_strip_backwards_parentheses(self):
        """Remove parentheses that are in wrong order"""
        text = ")Paren("
        self.assertEqual("Paren", util.strip_parens(text))

    def test_strip_backwards_quotes(self):
        """Remove quotes that are in wrong order,
        using punctuation to identify opening and closing quotes"""
        text = ".\" She said, \""
        self.assertEqual(". She said, ", util.strip_straight_quotes(text))

    def test_strip_interleaved_quotes(self):
        """Correctly handle balanced quotes mixed with unbalanced ones."""
        text = "yes,\" he said. \"Yes, but \"no.\""
        self.assertEqual("yes, he said. Yes, but \"no.\"",
                         util.strip_straight_quotes(text))

    def test_strip_interleaved_parentheses(self):
        """Correctly handle closed parentheses mixed with unclosed ones."""
        text = "(It's true (but (it) might not be)"
        self.assertEqual("It's true (but (it) might not be)",
                         util.strip_parens(text))

    def test_curly_quotes(self):
        """Correctly strip curly quotes"""
        text = "“foo”"
        self.assertEqual("“foo”", util.strip_curly_quotes(text))

    def test_unbalanced_curly_quotes(self):
        text = "”foo”"
        self.assertEqual("foo", util.strip_curly_quotes(text))


def main():
    unittest.main()


if __name__ == '__main__':
    main()
