"""
This module is responsible for all disk I/O
"""


class StringDatabase:
    """
    This class will maintain a database of strings and table of frequencies for each English alphabet
    """

    guess_words = []

    letter_frequency = {'a': 8.17, 'b': 1.49, 'c': 2.78, 'd': 4.25, 'e': 12.70,
                        'f': 2.23, 'g': 2.02, 'h': 6.09, 'i': 6.97, 'j': 0.15,
                        'k': 0.77, 'l': 4.03, 'm': 2.41, 'n': 6.75, 'o': 7.51,
                        'p': 1.93, 'q': 0.10, 'r': 5.99, 's': 6.33, 't': 9.06,
                        'u': 2.76, 'v': 0.98, 'w': 2.36, 'x': 0.15, 'y': 1.97,
                        'z': 0.07}

    @classmethod
    def read_guess_words_from_file(cls):
        """
        This method will read a text file and populate a list with 4 letter words
        """
        guess_words_file = open("four_letters.txt", "r")
        for guess_word in guess_words_file.read().split():
            cls.guess_words.append(guess_word)

    @classmethod
    def get_letter_frequency(cls, letter):
        """
        This method will get the frequency value of a alphabet
        :param letter: alphabet
        :return: frequency as number
        """
        return cls.letter_frequency[letter]
