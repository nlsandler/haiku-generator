#!/usr/bin/env python3
import markov
import util
import pickle

def generate_line(chain, syllable_count, previous=""):
    remaining_syllables = syllable_count
    running_text = previous
    while remaining_syllables > 0:
        for i in range(500):
            next_word = chain.next_word(running_text)
            if util.in_dict(next_word):
                syllables = util.get_syllable_count(next_word)
                if syllables <= remaining_syllables:
                    remaining_syllables -= syllables
                    running_text = running_text + " " + next_word
                    break
        else:
            raise RuntimeError("Couldn't make line")

        #process next word
    #return line without seed text/first space
    line = running_text[len(previous) + 1:]
    return line

def generate_haiku_attempt(chain):
    one = generate_line(chain, 5)
    #print(one)
    two = generate_line(chain, 7, one)
    #print(two)
    three = generate_line(chain, 5, two)
    #print(three)
    last_word = three.split()[-1]
    if not last_word[-1] in ".!?":
        raise RuntimeError("this haiku is garbage!")
    return [one, two, three]

def generate_haiku(chain):
    while True:
        try:
            haiku_lines = generate_haiku_attempt(chain)
            break
        except RuntimeError:
            continue
    print ("\n".join(haiku_lines))

if __name__ == '__main__':
    args = util.parse_args()
    chain = markov.MarkovChain.from_files(args.input, 2)
    #with open("pickled_chain", "rb") as f:
    #    chain = pickle.load(f)
    generate_haiku(chain)
