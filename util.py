import pronouncing
import string
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Generate a haiku.")
    parser.add_argument("input", default=["corpus/walden.txt"],
    nargs="*",
    help=("One or more input file(s) to use for markov text generation."
        " By default uses corpus/walden.txt."))
    return parser.parse_args()

def normalize(word):
    return word.strip().strip(string.punctuation).lower()

def in_dict(word):
    word = normalize(word)
    phones = pronouncing.phones_for_word(word)
    return (len(phones) > 0)

def get_syllable_count(word):
    word = normalize(word)
    phones = pronouncing.phones_for_word(word)[0]
    return len(pronouncing.stresses(phones))

def strip_unbalanced_punctuation(text, is_open_char, is_close_char):
    """Remove unbalanced punctuation (e.g parentheses) from text"""
    #iterate over text
    #when you encounter an opening_char, start looking for a closing closing_char
    #if you don't find one by the end of the text, remove opening_char
    #when you encounter a closing_char if it doesn't match an opening_char, remove it
    #so we need to track how many opening parens we have, and where they are
    opening_chars = [] #opening chars we're looking for a match for
    unmatched_closing_chars = [] #closing chars that don't have a match - delete at end of loop
    for idx, c in enumerate(text):
        if is_open_char(text, idx):
            opening_chars.append(idx)
        elif is_close_char(text, idx):
            if opening_chars:
                opening_chars.pop()
            else:
                unmatched_closing_chars.append(idx)
    char_indices = [i for (i,_) in enumerate(text) if not(i in opening_chars or i in unmatched_closing_chars)]
    stripped_text = "".join([text[i] for i in char_indices])
    return stripped_text

def strip_parens(text):
    is_open = lambda text, idx: text[idx] == "("
    is_close = lambda text, idx: text[idx] == ")"
    return strip_unbalanced_punctuation(text, is_open, is_close)

def strip_curly_quotes(text):
    is_open = lambda text, idx: text[idx] == "“"
    is_close = lambda text, idx: text[idx] == "”"
    return strip_unbalanced_punctuation(text, is_open, is_close)

def strip_straight_quotes(text):
    def quote_is_open(text, idx):
        if text[idx-1] in string.whitespace:
            # Bar. "Foo...
            return True
        elif len(text) == idx + 1:
            #It's the last quote in the text so assume it's closing
            return False
        elif text[idx+1] in string.whitespace:
            # foo." Bar...
            return False
        else:
            #No clear indication, just guess True
            return True
    is_open = lambda text, idx: text[idx] == "\"" and quote_is_open(text, idx)
    is_close = lambda text, idx: text[idx] == "\"" and not quote_is_open(text, idx)
    return strip_unbalanced_punctuation(text, is_open, is_close)

def strip_punctuation(text):
    return strip_parens(strip_curly_quotes(strip_straight_quotes(text)))
