"""A collection of utility functions used by the haiku module."""
from nltk.corpus import cmudict
import string
import argparse

syllable_dict = cmudict.dict()


def parse_args():
    """Parse command line and return input filenames and prefix length."""
    default_input = "corpus/moby_dick.txt"
    parser = argparse.ArgumentParser(
        description="Generate a haiku using Markov chains.")
    parser.add_argument("input", default=[default_input],
                        nargs="*",
                        help=("One or more input file(s) to use "
                              "for markov text generation. "
                              "By default uses ") + default_input+".")
    parser.add_argument("-l", "--prefix-len", dest="prefix_len",
                        type=int, default=2,
                        help="Markov chain prefix length (default is 2)")
    return parser.parse_args()


def _normalize(word):
    """Convert word to a form we can look up in CMU dictionary."""
    return word.strip().strip(string.punctuation).lower()


def in_dict(word):
    """Check whether a word is in the CMU pronouncing dictionary."""
    word = _normalize(word)
    return (word in syllable_dict)


def _is_vowel(phone):
    """Check whether a phoneme from the CMU dictionary represents a vowel."""
    return any(c.isdigit() for c in phone)


def get_syllable_count(word):
    """Get the number of syllables in a word.

    Each sylllable corresponds to one vowel phoneme in the CMU dictionary.
    Some words have multiple pronunciations, so just pick the first one.
    """
    word = _normalize(word)
    phones = syllable_dict[word][0]
    return len([phone for phone in phones if _is_vowel(phone)])


def _strip_unbalanced_punctuation(text, is_open_char, is_close_char):
    """Remove unbalanced punctuation (e.g parentheses or quotes) from text.

    Removes each opening punctuation character for which it can't find
    corresponding closing character, and vice versa.
    It can only handle one type of punctuation
    (e.g. it could strip quotes or parentheses but not both).
    It takes functions (is_open_char, is_close_char),
    instead of the characters themselves,
    so that we can determine from nearby characters whether a straight quote is
    an opening or closing quote.

    Args:
        text (string): the text to fix
        is_open_char: a function that accepts the text and an index,
            and returns true if the character at that index is
            an opening punctuation mark.
        is_close_char: same as is_open_char for closing punctuation mark.

    Returns:
        The text with unmatched punctuation removed.
    """
    # lists of unmatched opening and closing chararacters
    opening_chars = []
    unmatched_closing_chars = []
    for idx, c in enumerate(text):
        if is_open_char(text, idx):
            opening_chars.append(idx)
        elif is_close_char(text, idx):
            if opening_chars:
                # this matches a character we found earlier
                opening_chars.pop()
            else:
                # this doesn't match any opening character
                unmatched_closing_chars.append(idx)
    char_indices = [i for (i, _) in enumerate(text)
                    if not(i in opening_chars or i in unmatched_closing_chars)]
    stripped_text = "".join([text[i] for i in char_indices])
    return stripped_text


def _strip_parens(text):
    """Remove any unmatched parentheses from a string."""
    def is_open(txt, idx):
        return txt[idx] == "("

    def is_close(txt, idx):
        return txt[idx] == ")"

    return _strip_unbalanced_punctuation(text, is_open, is_close)


def _strip_curly_quotes(text):
    """Remove any unmatched curly quotes from a string."""
    def is_open(text, idx):
        return text[idx] == "“"

    def is_close(text, idx):
        return text[idx] == "”"

    return _strip_unbalanced_punctuation(text, is_open, is_close)


def _strip_straight_quotes(text):
    """Remove any unmatched straight quotes from a string."""
    def quote_is_open(text, idx):
        if text[idx-1] in string.whitespace:
            # Bar. "Foo...
            return True
        elif len(text) == idx + 1:
            # It's the last character in the text so assume it's closing
            return False
        elif text[idx+1] in string.whitespace:
            # foo." Bar...
            return False
        else:
            # No clear indication, just guess True
            return True

    def is_open(text, idx):
        return text[idx] == "\"" and quote_is_open(text, idx)

    def is_close(text, idx):
        return text[idx] == "\"" and not quote_is_open(text, idx)

    return _strip_unbalanced_punctuation(text, is_open, is_close)


def strip_punctuation(text):
    """Remove unmatched parentheses and quotes from a string."""
    text = _strip_straight_quotes(text)
    text = _strip_curly_quotes(text)
    text = _strip_parens(text)
    return text
