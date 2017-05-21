"""Markov chain text generator.

This module exports the MarkovChain class.
"""
import random
import os
import nltk


def _update_prefix(prefix_len, current_prefix, new_word):
    """Remove first word from a prefix, and adds a new word to the end.

    If the prefix contains fewer than prefix_len words,
    as it will at the very beginning of the chain,
    don't pop off the first word.
    """
    prefix_words = current_prefix.split()
    # pop off first word, unless prefix is shorter than prefix_len
    if len(prefix_words) == prefix_len:
        prefix_words.pop(0)
    elif len(prefix_words) > prefix_len:
        raise ValueError("Prefix is too long!")

    # add current word to prefix
    prefix_words.append(new_word)
    new_prefix = " ".join(prefix_words)

    return new_prefix.strip()


class MarkovChain:
    """A Markov chain text generator.

    To build a chain, this class creates a dictionary from each prefix
    to a list of all possible words that could follow that prefix (where every
    substring consisting of ``_prefix_len`` words is a prefix).
    If a word follows a prefix at more than one point in the text, it will
    appear more than once on the list of next words in that prefix's dictionary
    entry.

    In order to generate long chunks of text, the factory methods (from_string
    and from_files) first build the chain from the whole text at once,
    treating it as a single string. However, this means the generated text
    will always start the same way as the original text. To prevent this,
    the input text is broken into sentences, and the start of each sentence is
    added as a possible starting point for generated text.

    Public methods:
        from_string (class method): Construct a markov chain from a string
        from_files (class method): Construct a markov chain from the contents
            of a list of files
        generate: Generate text.
        next_word: Given some text, generate the next word.

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
            "": []
        }

    def _update(self, text):
        """Update the chain with the provided text."""
        current_prefix = ""
        word_list = text.split()
        for word in word_list:
            # add word to chain for appropriate prefix
            if current_prefix not in self._chain:
                self._chain[current_prefix] = []
            self._chain[current_prefix].append(word)

            current_prefix = _update_prefix(self._prefix_len,
                                            current_prefix, word)

    def _add_chain_start(self, sentence):
        """Update chain with first _prefix_len words of the sentence.

        This should be called on sentences that have already been added to
        the chain. By re-adding just the first _prefix_len words here,
        we make it possible to start generated text with this sentence.
        """
        words = text.split()
        sentence_start = words[:self._prefix_len]
        self._update(" ".join(sentence_start))

    def _add_sentences(self, text):
        # First read in everything as one string,
        # So we can generate more than one sentence at a time
        self._update(text)
        # now make each sentence a starting point
        # first sentence already is, so ignore it
        sentences = nltk.sent_tokenize(text)[1:]
        for sentence in sentences:
            # make each sentence a starting point!
            self._add_chain_start(sentence)

    @classmethod
    def from_string(cls, text, prefix_len=2):
        """Build a markov chain from a string.

        Args:
            text (string): the input text
            prefix_len: optional prefix length

        Returns:
            A MarkovChain
        """
        chain = cls(prefix_len)
        chain._add_sentences(text)
        return chain

    @classmethod
    def from_files(cls, file_names, prefix_len):
        """Build a Markov chain from a list of files.

        Args:
            file_names (list of strings): files to read input text from
            prefix_len: the prefix length of the Markov chain

        Returns:
            A MarkovChain
        """
        chain = cls(prefix_len)
        for file_name in file_names:
            with open(file_name, 'r') as f:
                text = " ".join(f.read().splitlines())
                chain._add_sentences(text)
                # chain.update_from_file(f)
        return chain

    def generate(self, word_count, current_text=""):
        """Generate word_count words.

        Args:
            word_count (int): number of words to generate
            current_text (string): optional seed text, which can be any length

        Returns:
            The generated text, as a string
        """
        current_prefix = prefix
        generated_words = []
        for i in range(word_count):
            if current_prefix in self._chain:
                word = random.choice(self._chain[current_prefix])
            else:
                # we're out of prefixes,
                # so just return what we've generated thus far
                break

            generated_words.append(word)
            current_prefix = _update_prefix(self._prefix_len,
                                            current_prefix, word)

        return " ".join(generated_words)

    def next_word(self, current_text):
        """Given some text, generate another word.

        Args:
            current_text (string): seed text, which can be any length

        Returns:
            The next word (as a string)
        """
        prefix_words = current_text.split()[-self._prefix_len:]
        prefix = " ".join(prefix_words)
        return self.generate(1, prefix=prefix)
