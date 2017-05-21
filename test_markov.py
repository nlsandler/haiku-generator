#!/usr/bin/env python3
import markov
import unittest


class MarkovTests(unittest.TestCase):
    long_text = ("It is a far, far better thing that I do, "
                 "than I have ever done; "
                 "it is a far, far better rest that I go to "
                 "than I have ever known.")
    short_text = "Here are words."
    # This text is also the content of test0.txt and test1.txt
    factory_text = "Here is some text. It is not long."
    expected_factory_dict = {
        "": ["Here", "It"],
        "Here": ["is"],
        "It": ["is"],
        "Here is": ["some"],
        "is some": ["text."],
        "some text.": ["It"],
        "text. It": ["is"],
        "It is": ["not"],
        "is not": ["long."]
    }

    def _compare_dictionaries(self, expected, actual):
        for key in expected:
            self.assertTrue(actual[key])
            self.assertEqual(expected[key], actual[key])
        for key in actual:
            self.assertTrue(expected[key])

    def test_update_prefix(self):
        prefix = markov._update_prefix(2, "I am", "a")
        self.assertEqual("am a", prefix)

    def test_update_short_prefix(self):
        prefix = markov._update_prefix(2, "I", "am")
        self.assertEqual("I am", prefix)

    def test_update_empty_prefix(self):
        prefix = markov._update_prefix(2, "", "I")
        self.assertEqual("I", prefix)

    def test_update_prefix_strip_space(self):
        prefix = markov._update_prefix(2, " I have", "a")
        self.assertEqual("have a", prefix)

    def test_update_prefix_strip_mid_space(self):
        prefix = markov._update_prefix(2, "I  have", "a")
        self.assertEqual("have a", prefix)

    def test_update_prefix_strip_end_space(self):
        prefix = markov._update_prefix(2, "I have ", "a")
        self.assertEqual("have a", prefix)

    def test_prefix_too_short(self):
        with self.assertRaises(ValueError):
            markov.MarkovChain(0)

    def test_update_chain(self):
        prefix_len = 2
        word_dict = {
            "": ["It"],
            "It": ["is"],
            "It is": ["a"],
            "is a": ["far,", "far,"],
            "a far,": ["far", "far"],
            "far, far": ["better", "better"],
            "far better": ["thing", "rest"],
            "better thing": ["that"],
            "thing that": ["I"],
            "that I": ["do,", "go"],
            "I do,": ["than"],
            "do, than": ["I"],
            "than I": ["have", "have"],
            "I have": ["ever", "ever"],
            "have ever": ["done;", "known."],
            "ever done;": ["it"],
            "done; it": ["is"],
            "it is": ["a"],
            "better rest": ["that"],
            "rest that": ["I"],
            "I go": ["to"],
            "go to": ["than"],
            "to than": ["I"]
        }
        chain = markov.MarkovChain(prefix_len)
        chain._update(self.long_text)
        self._compare_dictionaries(word_dict, chain._chain)

    def test_update_chain_longer_prefix(self):
        prefix_len = 3
        word_dict = {
            "": ["It"],
            "It": ["is"],
            "It is": ["a"],
            "It is a": ["far,"],
            "is a far,": ["far", "far"],
            "a far, far": ["better", "better"],
            "far, far better": ["thing", "rest"],
            "far better thing": ["that"],
            "better thing that": ["I"],
            "thing that I": ["do,"],
            "that I do,": ["than"],
            "I do, than": ["I"],
            "do, than I": ["have"],
            "than I have": ["ever", "ever"],
            "I have ever": ["done;", "known."],
            "have ever done;": ["it"],
            "ever done; it": ["is"],
            "done; it is": ["a"],
            "it is a": ["far,"],
            "far better rest": ["that"],
            "better rest that": ["I"],
            "rest that I": ["go"],
            "that I go": ["to"],
            "I go to": ["than"],
            "go to than": ["I"],
            "to than I": ["have"]
        }

        chain = markov.MarkovChain(prefix_len)
        chain._update(self.long_text)
        self._compare_dictionaries(word_dict, chain._chain)

    def test_add_chain_start(self):
        chain = markov.MarkovChain(2)
        chain._update("This is a sentence.")
        chain._add_chain_start("I have some text.")
        expected_dict = {
            "": ["This", "I"],
            "This": ["is"],
            "This is": ["a"],
            "is a": ["sentence."],
            "I": ["have"]
        }
        self._compare_dictionaries(expected_dict, chain._chain)

    def test_add_sentences(self):
        chain = markov.MarkovChain(2)
        chain._add_sentences(self.factory_text)
        self._compare_dictionaries(self.expected_factory_dict, chain._chain)

    def test_from_string(self):
        chain = markov.MarkovChain.from_string(self.factory_text)
        self._compare_dictionaries(self.expected_factory_dict, chain._chain)

    def test_from_file(self):
        """Test that both sentences are starting points for text generation"""
        chain = markov.MarkovChain.from_files(["test/test0.txt"], 2)
        self._compare_dictionaries(self.expected_factory_dict, chain._chain)

    def test_from_files_with_newline(self):
        chain = markov.MarkovChain.from_files(["test/test1.txt"], 2)
        self._compare_dictionaries(self.expected_factory_dict, chain._chain)

    def test_from_multiple_files(self):
        file_names = ["test/test2.txt", "test/test3.txt"]
        prefix_len = 2
        chain = markov.MarkovChain.from_files(file_names, prefix_len)
        expected_dict = {
            "": ["I", "I"],
            "I": ["am", "am"],
            "I am": ["a", "a"],
            "am a": ["cat!", "rat."]
        }
        self._compare_dictionaries(expected_dict, chain._chain)

    def test_generate(self):
        chain = markov.MarkovChain.from_string(self.short_text, prefix_len=1)
        generated_text = chain.generate(3)
        # only one possible string in this case,
        # so generated text will be identical to input
        self.assertEqual(self.short_text, generated_text)

    def test_generate_high_word_limit(self):
        """Stop generating text when you run out of valid suffixes."""
        long_word_count = 10
        chain = markov.MarkovChain.from_string(self.short_text, prefix_len=1)
        generated_text = chain.generate(long_word_count)
        self.assertEqual(self.short_text, generated_text)

    def test_generate_low_word_limit(self):
        """Stop at the word limit, even if there are more valid suffixes."""
        short_word_count = 2
        text = "This is a short piece of sample text."
        chain = markov.MarkovChain.from_string(text)
        generated_text = chain.generate(short_word_count)
        self.assertEqual("This is", generated_text)

    def test_next_word(self):
        text = "Here is some text!"
        chain = markov.MarkovChain.from_string(text)
        next_word = chain.next_word("Here is some")
        self.assertEqual("text!", next_word)

    def test_next_word_short_prefix(self):
        text = "Here is some text!"
        chain = markov.MarkovChain.from_string(text)
        next_word = chain.next_word("Here")
        self.assertEqual("is", next_word)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
