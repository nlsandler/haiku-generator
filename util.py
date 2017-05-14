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
    return word.strip(string.punctuation).strip().lower()

def in_dict(word):
    word = normalize(word)
    phones = pronouncing.phones_for_word(word)
    return (len(phones) > 0)

def get_syllable_count(word):
    word = normalize(word)
    phones = pronouncing.phones_for_word(word)[0]
    return len(pronouncing.stresses(phones))

def verse_to_prose(verse):
    """Replace newlines with spaces, and remove extra spaces"""
    lines = verse.splitlines()
    lines = [line for line in lines if line.strip()]
    return " ".join(lines)
