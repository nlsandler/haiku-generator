from nltk.corpus import cmudict
import string
import argparse

syllable_dict = cmudict.dict()

def parse_args():
    parser = argparse.ArgumentParser(description="Generate a haiku using Markov chains.")
    parser.add_argument("input", default=["corpus/walden.txt"],
    nargs="*",
    help=("One or more input file(s) to use for markov text generation."
        " By default uses corpus/walden.txt."))
    parser.add_argument("-l","--prefix-len", dest="prefix_len",
        type=int, default=2, help="Markov chain prefix length (default is 2)")
    return parser.parse_args()

def normalize(word):
    return word.strip().strip(string.punctuation).lower()

def in_dict(word):
    word = normalize(word)
    return (word in syllable_dict)

def is_vowel(phone):
    return any(c.isdigit() for c in phone)

def get_syllable_count(word):
    word = normalize(word)
    phones = syllable_dict[word][0]
    return len([phone for phone in phones if is_vowel(phone)])

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
                #this matches a character we found earlier
                opening_chars.pop()
            else:
                #this doesn't match anything, so we need to remove it
                unmatched_closing_chars.append(idx)
    #get all indices not in opening_chars or unmatched_closing_chars
    char_indices = [i for (i,_) in enumerate(text)
                    if not(i in opening_chars or i in unmatched_closing_chars)]
    #get text defined by char_indices
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
            #It's the last character in the text so assume it's closing
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
    text = strip_straight_quotes(text)
    text = strip_curly_quotes(text)
    text = strip_parens(text)
    return text
