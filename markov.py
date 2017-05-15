"""
Chain:
Map<Prefix -> string[]>
where a prefix is n words

1) Build the chain
    read in all the words
    get list of words
    for word in ("", "", word) :
        make prefix
2) Generate n words
"""
import random
import os
import nltk

def _update_prefix(prefix_len, current_prefix, new_word):
    """Removes first word from a prefix, and adds a new word to the end.
    If the prefix contains fewer than prefix_len words,
    as it will at the very beginning of the chain,
    don't pop off the first word.
    """
    #split prefix into word list
    prefix_words = current_prefix.split()
    #if length is not less than prefix_len, remove first word
    if len(prefix_words) == prefix_len:
        prefix_words.pop(0)
    elif len(prefix_words) > prefix_len:
        raise ValueError("Prefix is too long!")

    #add current word to prefix
    prefix_words.append(new_word)
    new_prefix = " ".join(prefix_words)

    return new_prefix.strip()

class MarkovChain:
    """A Markov chain of text.

    The chain is a dictionary from a prefix to a list of words.
    Each prefix consists of prefixLen words, represented as a single string.
    TODO: rest of docstring
    """

    def __init__(self, prefix_len):
        """Initialize the Markov chain.

        Args:
            prefix_len (int): number of words in each prefix
        """
        if prefix_len < 1:
            raise ValueError('Prefix length must be at least one')

        self._prefix_len = prefix_len
        self._chain = {
            "" : []
        }

    def _add_chain_start(self, text):
        """Make this text a possible start to the chain,
        but don't read in the whole thing."""

        words = text.split()
        sentence_start = words[:self._prefix_len]
        self.update(" ".join(sentence_start))

    def update_from_file(self, f):
        text = " ".join(f.read().splitlines())
        self.update(text)
        #make each sentence a starting point
        #first sentence already is, so ignore it
        sentences = nltk.sent_tokenize(text)[1:]
        for sentence in sentences:
            #make each sentence a starting point!
            self._add_chain_start(sentence)

    @classmethod
    def from_files(cls, file_names, prefix_len):
        chain = cls(prefix_len)
        for file_name in file_names:
            with open(file_name, 'r') as f:
                chain.update_from_file(f)
        return chain

    def update(self, text):
        """Update the chain with the provided text.

        Args:
            text (string): input text to build chain from
        """
        current_prefix = ""
        word_list = text.split()
        for word in word_list:
            #add word to chain for appropriate prefix
            if not current_prefix in self._chain:
                self._chain[current_prefix] = []
            self._chain[current_prefix].append(word)

            current_prefix = _update_prefix(self._prefix_len, current_prefix, word)

    def generate(self, word_count, prefix=""):
        """Generate word_count words.

        Args:
            word_count (int): number of words to generate

        Returns:
            The generated text, as a string
        """
        current_prefix = prefix
        generated_words = []
        for i in range(word_count):
            if current_prefix in self._chain:
                word = random.choice(self._chain[current_prefix])
            else:
                #we're out of prefixes, just return what we've generated thus far
                break

            generated_words.append(word)
            current_prefix = _update_prefix(self._prefix_len, current_prefix, word)

        return " ".join(generated_words)

    def next_word(self, current_text):
        """Given a line, generate another word.

        Args:
            line (string): the text generated so far.

        Returns:
            The next word (as a string)
        """
        prefix_words = current_text.split()[-self._prefix_len:]
        prefix = " ".join(prefix_words)
        return self.generate(1, prefix=prefix)
