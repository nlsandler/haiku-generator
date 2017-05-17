#!/usr/bin/env python3
import markov
import util
import pickle

def get_next_word(chain, seed_text, remaining_syllables):
    """Generate a word with fewer than the specified number of syllables"""
    #try to get a valid word 100 times
    for i in range(100):
        word = chain.next_word(seed_text)
        if (util.in_dict(word)
            and util.get_syllable_count(word) <= remaining_syllables):
            #This word is valid
            return word
    else:
        #After 100 attempts, give up
        raise RuntimeError("Couldn't find a valid word")

def generate_line(chain, syllable_count, previous_text=""):
    remaining_syllables = syllable_count
    seed_text = previous_text
    line = []
    while remaining_syllables > 0:
        next_word = get_next_word(chain, seed_text, remaining_syllables)
        seed_text += " " + next_word
        line.append(next_word)
        remaining_syllables -= util.get_syllable_count(next_word)
    return " ".join(line)

def generate_end_line(chain, syllable_count, previous):
    """Generate a line ending with punctuation (?!.)

    This is a cheap way to avoid the most awkward and abrupt endings"""

    #Try 100 times to generate a line with end punctuation
    for i in range(100):
        three = generate_line(chain, 5, previous)
        if three[-1] in ".!?":
            #last line ends with punctuation, so use it
            return three
    else:
        raise RuntimeError("Doesn't end with punctuation!")

def generate_haiku_attempt(chain):
    one = generate_line(chain, 5)
    two = generate_line(chain, 7, one)
    three = generate_end_line(chain, 5, " ".join([one, two]))
    return "\n".join([one, two, three])

def generate_haiku(chain):
    while True:
        #Keep trying until we get a haiku
        #Note that if a valid haiku cannot be produced from the text,
        #this will loop forever
        try:
            haiku = generate_haiku_attempt(chain)
            break
        except RuntimeError:
            continue
    cleaned_haiku = util.strip_punctuation(haiku)
    return cleaned_haiku

if __name__ == '__main__':
    args = util.parse_args()
    chain = markov.MarkovChain.from_files(args.input, args.prefix_len)
    haiku = generate_haiku(chain)
    print(haiku)
