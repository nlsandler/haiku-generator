#!/usr/bin/env python3
"""A haiku generator.

Build a Markov chain using the specified input files and prefix length,
and generate a haiku using that Markov chain.
"""
import markov
import util


def get_next_word(chain, seed_text, remaining_syllables):
    """Generate a word with fewer than the specified number of syllables.

    Args:
        chain (MarkovChain): Markov chain to use to generate the next word.
        seed_text (string): The text that's been generated so far.
        remaining_syllables (int): Maximum number of syllables allowed.
    Returns:
        The generated word (string).
    Raises:
        RuntimeError, if it fails to generate an acceptable word after
            100 tries. This error will be caught in generate_haiku().
    """
    # try to get a valid word 100 times
    for i in range(100):
        word = chain.next_word(seed_text)
        if (util.in_dict(word) and
            util.get_syllable_count(word) <= remaining_syllables):
            # This word is valid
            return word
    else:
        # After 100 attempts, give up
        raise RuntimeError("Couldn't find a valid word")


def generate_line(chain, syllable_count, previous_text=""):
    """Generate a line with the specified number of syllables.

    Args:
        chain (MarkovChain): Markov chain to use to generate line
        syllable_count (int): How many syllables the line should have.
        previous_text (string): The text that's been generated so far.
    Returns:
        The generated line (string)
    """
    remaining_syllables = syllable_count
    seed_text = previous_text
    line = []
    while remaining_syllables > 0:
        next_word = get_next_word(chain, seed_text, remaining_syllables)
        seed_text += " " + next_word
        line.append(next_word)
        remaining_syllables -= util.get_syllable_count(next_word)
    return " ".join(line)


def generate_end_line(chain, syllable_count, previous_text):
    """Generate the last line of the haiku.

    This line must end with punctuation (.?!) to prevents awkward endings
    in the middle of a phrase.

    Args
        chain (MarkovChain): Markov chain to use to generate line
        syllable_count (int): How many syllables the line should have.
        previous_text (string): The text that's been generated so far.
    Returns:
        The generated line (string)
    Raises:
        RuntimeError if the generated line doesn't end with punctuation.
            This error will be caught in generate_haiku()
    """
    # Try 100 times to generate a line with end punctuation
    for i in range(100):
        three = generate_line(chain, 5, previous_text)
        if three[-1] in ".!?":
            # last line ends with punctuation, so use it
            return three
    else:
        raise RuntimeError("Doesn't end with punctuation!")


def generate_haiku_attempt(chain):
    """Try to generate a haiku.

    Let any RuntimeErrors propagate up to generate_haiku()

    Args:
        chain (MarkovChain): Markov chain to use to generate line
    Returns:
        The generated haiku (string).
    """
    one = generate_line(chain, 5)
    two = generate_line(chain, 7, one)
    three = generate_end_line(chain, 5, " ".join([one, two]))
    return "\n".join([one, two, three])


def generate_haiku(chain):
    """Generate a haiku, and fix any mismatched punctuation in the result.

    If it fails to generate a haiku, try again...and keep trying forever.

    Args:
        chain (MarkovChain): Markov chain to use to generate line
    Returns:
        The generated haiku (string).
    """
    while True:
        # NOTE: if a valid haiku can't be generated from this text,
        # this will loop forever!
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
