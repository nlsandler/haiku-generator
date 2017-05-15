#!/usr/bin/env python3
import markov
import unittest


class MarkovTests(unittest.TestCase):

    def compare_dictionaries(self, expected, actual):
        for key in expected:
            #make sure key is present
            self.assertTrue(actual[key])
            self.assertEqual(expected[key], actual[key])
        #make sure there are no keys in actual that aren't in expected
        for key in actual:
            self.assertTrue(expected[key])

    def test_prefix_too_short(self):
        """Prefix length must be greater or equal to one"""
        with self.assertRaises(ValueError):
            markov.MarkovChain(0)

    def test_build_chain(self):
        """Constructor should generate the chain correctly.

        Sample text:
        "It is a far, far better thing that I do, than I have ever done;
        it is a far, far better rest that I go to than I have ever known."
        """
        prefix_len = 2
        text = ("It is a far, far better thing that I do, than I have ever done;"
                " it is a far, far better rest that I go to than I have ever known.")
        word_dict = {
            "" : ["It"],
            "It" : ["is"],
            "It is" : ["a"],
            "is a" : ["far,", "far,"],
            "a far," : ["far", "far"],
            "far, far" : ["better", "better"],
            "far better" : ["thing", "rest"],
            "better thing" : ["that"],
            "thing that" : ["I"],
            "that I" : ["do,", "go"],
            "I do," : ["than"],
            "do, than" : ["I"],
            "than I" : ["have", "have"],
            "I have" : ["ever", "ever"],
            "have ever" : ["done;", "known."],
            "ever done;" : ["it"],
            "done; it" : ["is"],
            "it is" : ["a"],
            "better rest" : ["that"],
            "rest that" : ["I"],
            "I go" : ["to"],
            "go to" : ["than"],
            "to than" : ["I"]
        }
        chain = markov.MarkovChain(prefix_len)
        chain.update(text)
        self.compare_dictionaries(word_dict, chain._chain)

    def test_prefix_len(self):
        """Markov chain should respect given prefix length."""
        prefix_len = 3
        text = ("It is a far, far better thing that I do, than I have ever done;"
                " it is a far, far better rest that I go to than I have ever known.")
        word_dict = {
            "" : ["It"],
            "It" : ["is"],
            "It is" : ["a"],
            "It is a" : ["far,"],
            "is a far," : ["far", "far"],
            "a far, far" : ["better", "better"],
            "far, far better" : ["thing", "rest"],
            "far better thing" : ["that"],
            "better thing that" : ["I"],
            "thing that I" : ["do,"],
            "that I do," : ["than"],
            "I do, than" : ["I"],
            "do, than I" : ["have"],
            "than I have" : ["ever", "ever"],
            "I have ever" : ["done;", "known."],
            "have ever done;" : ["it"],
            "ever done; it" : ["is"],
            "done; it is" : ["a"],
            "it is a" : ["far,"],
            "far better rest" : ["that"],
            "better rest that" : ["I"],
            "rest that I" : ["go"],
            "that I go" : ["to"],
            "I go to" : ["than"],
            "go to than" : ["I"],
            "to than I" : ["have"]
        }

        chain = markov.MarkovChain(prefix_len)
        chain.update(text)
        self.compare_dictionaries(word_dict, chain._chain)

    def test_generate(self):
        """Generate should create valid generated text.

        When every prefix has only one possible suffix, it should produce the original text,
        regardless of prefix length.
        """
        text = "Here are words."
        chain = markov.MarkovChain(1)
        chain.update(text)
        generated_text = chain.generate(3)
        self.assertEqual(text, generated_text)

    def test_generate_high_word_limit(self):
        """Stop generating text when you run out of valid suffixes."""
        long_word_count = 10
        text = "Here are words."
        chain = markov.MarkovChain(1)
        chain.update(text)
        generated_text = chain.generate(long_word_count)
        self.assertEqual(text, generated_text)

    def test_generate_low_word_limit(self):
        """Stop at the word limit, even if there are more valid suffixes."""
        short_word_count = 2
        text = "This is a somewhat longer piece of sample text."
        chain = markov.MarkovChain(1)
        chain.update(text)
        generated_text = chain.generate(short_word_count)
        self.assertEqual("This is", generated_text)

    def test_next_word(self):
        text = "Here is some text!"
        chain = markov.MarkovChain(2)
        chain.update(text)
        next_word = chain.next_word("Here is some")
        self.assertEqual("text!", next_word)

    def test_next_word_short_prefix(self):
        text = "Here is some text!"
        chain = markov.MarkovChain(2)
        chain.update(text)
        next_word = chain.next_word("Here")
        self.assertEqual("is", next_word)
    def test_update_prefix(self):
        prefix = markov._update_prefix(2, "I am", "a")
        self.assertEqual("am a", prefix)
    def test_update_short_prefix(self):
        prefix = markov._update_prefix(2, "I", "am")
        self.assertEqual("I am", prefix)
    def test_update_empty_prefix(self):
        prefix = markov._update_prefix(2, "", "I")
        self.assertEqual("I", prefix)
    def test_update_prefix_with_space(self):
        prefix = markov._update_prefix(2, " I have", "a")
        self.assertEqual("have a", prefix)
    def test_update_prefix_mid_space(self):
        prefix = markov._update_prefix(2, "I  have", "a")
        self.assertEqual("have a", prefix)
    def test_update_prefix_end_space(self):
        prefix = markov._update_prefix(2, "I have ", "a")
        self.assertEqual("have a", prefix)
    def test_add_chain_start(self):
        """Test that a sentence is added as an entry point,
        but no duplicates are introduced."""
        chain = markov.MarkovChain(2)
        chain.update("This is a sentence.")
        chain._add_chain_start("I have some text.")
        expected_dict = {
            "": ["This", "I"],
            "This": ["is"],
            "This is": ["a"],
            "is a": ["sentence."],
            "I": ["have"]
        }
        self.compare_dictionaries(expected_dict, chain._chain)
    def test_add_chain_short_prefix(self):
        chain = markov.MarkovChain(1)
        chain.update("This is a sentence.")
        chain._add_chain_start("I have some text.")
        expected_dict = {
            "": ["This", "I"],
            "This": ["is"],
            "is": ["a"],
            "a": ["sentence."]
        }
        self.compare_dictionaries(expected_dict, chain._chain)
    def test_add_chain_long_prefix(self):
        chain = markov.MarkovChain(3)
        chain.update("This is a sentence.")
        chain._add_chain_start("I have some text here.")
        expected_dict = {
            "": ["This", "I"],
            "This": ["is"],
            "This is": ["a"],
            "This is a": ["sentence."],
            "I": ["have"],
            "I have": ["some"]
        }
        self.compare_dictionaries(expected_dict, chain._chain)
    def test_update_from_file(self):
        """Test that both sentences are entry points into the chain"""
        chain = markov.MarkovChain(2)
        with open("test/test0.txt","r") as f:
            chain.update_from_file(f)
        expected_dict = {
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
        self.compare_dictionaries(expected_dict, chain._chain)
    def test_update_from_file_with_newline(self):
        chain = markov.MarkovChain(2)
        with open("test/test1.txt","r") as f:
            chain.update_from_file(f)
        expected_dict = {
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
        self.compare_dictionaries(expected_dict, chain._chain)
    def test_from_files(self):
        file_names = ["test/test2.txt", "test/test3.txt"]
        prefix_len = 2
        chain = markov.MarkovChain.from_files(file_names, prefix_len)
        expected_dict = {
            "": ["I","I"],
            "I": ["am", "am"],
            "I am": ["a", "a"],
            "am a": ["cat!","rat."]
        }
        self.compare_dictionaries(expected_dict, chain._chain)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
