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

def strip_unbalanced_punctuation(text, opening_char, closing_char):
    """Remove unbalanced punctuation (e.g parentheses) from text"""
    #iterate over text
    #when you encounter an opening_char, start looking for a closing closing_char
    #if you don't find one by the end of the text, remove opening_char
    #when you encounter a closing_char if it doesn't match an opening_char, remove it
    #so we need to track how many opening parens we have, and where they are
    opening_chars = [] #opening chars we're looking for a match for
    unmatched_closing_chars = [] #closing chars that don't have a match - delete at end of loop
    for idx, c in enumerate(text):
        if c == opening_char:
            opening_chars.append(idx)
        elif c == closing_char:
            if opening_chars:
                opening_chars.pop()
            else:
                unmatched_closing_chars.append(idx)
    char_indices = [i for (i,_) in enumerate(text) if not(i in opening_chars or i in unmatched_closing_chars)]
    stripped_text = "".join([text[i] for i in char_indices])
    return stripped_text

def strip_punct_lambda(text, delim, is_opening):
    """Remove unbalanced punctuation (e.g parentheses) from text"""
    #iterate over text
    #when you encounter an opening_char, start looking for a closing closing_char
    #if you don't find one by the end of the text, remove opening_char
    #when you encounter a closing_char if it doesn't match an opening_char, remove it
    #so we need to track how many opening parens we have, and where they are
    opening_chars = [] #opening chars we're looking for a match for
    unmatched_closing_chars = [] #closing chars that don't have a match - delete at end of loop
    for idx, c in enumerate(text):
        if c == delim:
            if is_opening(text, idx):
                opening_chars.append(idx)
            else:
                if opening_chars:
                    opening_chars.pop()
                else:
                    unmatched_closing_chars.append(idx)
    char_indices = [i for (i,_) in enumerate(text) if not(i in opening_chars or i in unmatched_closing_chars)]
    stripped_text = "".join([text[i] for i in char_indices])
    return stripped_text

def strip_straight_quotes(text):
    def is_opening(text, i):
        if text[i-1] in string.whitespace:
            # Bar. "Foo...
            return True
        elif len(text) == i + 1:
            #It's the last quote in the text so assume it's closing
            return False
        elif text[i+1] in string.whitespace:
            # foo." Bar...
            return False
        else:
            #No clear indication, just guess True
            return True
    return strip_punct_lambda(text, "\"", is_opening)
