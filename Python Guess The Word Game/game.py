"""
This module will maintain information about a specific game
"""

import stringDatabase


class Game:
    """
    This class will contain information about a specific game and also other static methods to compute game operations
    """

    def __init__(self, word, choice, missed_letter_freq, missed_guess_freq, request_letter_freq, status, score,
                 guessed_word):
        """
        Constructor to initialize the game attributes
        :param word: the game's guess word as string
        :param choice: the player's choices for each round in the game as list
        :param missed_letter_freq: the number of times the player made a bad letter guess as a number 
        :param missed_guess_freq: the number of times the player made a bad word guess as a number
        :param request_letter_freq: the number of times the player made a letter guess
        :param status: the final result status of the specific game as String
        :param score: the final score of the specific game as a number
        :param guessed_word: the player's final guess word as string
        """
        self.__word = word
        self.__choice = choice
        self.__missed_letter_freq = missed_letter_freq
        self.__missed_guess_freq = missed_guess_freq
        self.__request_letter_freq = request_letter_freq
        self.__status = status
        self.__score = score
        self.__guessed_word = guessed_word

    def get_word(self):
        """
        Getter for the guess word
        :return: word as string
        """
        return self.__word

    def set_word(self, word):
        """
        Setter for the guess word
        :param word: as string
        """
        self.__word = word

    def get_choice(self):
        """
        Getter for the choices
        :return: choice as list
        """
        return self.__choice

    def set_choice(self, choice):
        """
        Setter for the choices
        :param choice: as list
        """
        self.__choice = choice

    def get_missed_letter_frequency(self):
        """
        Getter for the missed_letter_frequency 
        :return: missed_letter_frequency as number
        """
        return self.__missed_letter_freq

    def set_missed_letter_frequency(self, missed_letter_freq):
        """
        Setter for missed_letter_frequency
        :param missed_letter_freq: as number
        """
        self.__missed_letter_freq = missed_letter_freq

    def get_missed_guess_frequency(self):
        """
        Getter for missed_guess_frequency
        :return: missed_guess_frequency as number
        """
        return self.__missed_guess_freq

    def set_missed_guess_frequency(self, missed_guess_freq):
        """
        Setter for missed_guess_frequency
        :param missed_guess_freq: as number
        """
        self.__missed_guess_freq = missed_guess_freq

    def get_request_letter_frequency(self):
        """
        Getter for request_letter_frequency
        :return: request_letter_frequency as number
        """
        return self.__request_letter_freq

    def set_request_letter_frequency(self, request_letter_frequency):
        """
        Setter for request_letter_frequency
        :param request_letter_frequency: as number
        """
        self.__request_letter_freq = request_letter_frequency

    def get_status(self):
        """
        Getter for status
        :return: status as string
        """
        return self.__status

    def set_status(self, status):
        """
        Setter for status
        :param status: as string
        """
        self.__status = status

    def get_score(self):
        """
        Getter for score
        :return: score as number
        """
        return self.__score

    def set_score(self, score):
        """
        Setter for score
        :param score: as number
        """
        self.__score = score

    def get_guessed_word(self):
        """
        Getter for player's guessed_word
        :return: guessed_word as string
        """
        return self.__guessed_word

    def set_guessed_word(self, guessed_word):
        """
        Setter for guessed_word
        :param guessed_word: as string
        """
        self.__guessed_word = guessed_word

    @staticmethod
    def calculate_game_score(game):
        """
        This method will calculate the specific game's final score
        :param game: specific game's instance
        :return: specific game's final score as number
        """
        if game.__status == 'Success':
            return Game.calculate_success_score(game)
        else:
            return Game.calculate_gave_up_score(game)

    @staticmethod
    def calculate_success_score(game):
        """
        This method will calculate the score of the game in which player won 
        :param game: specific game's instance
        :return: specific game's final score as number
        """
        score = 0
        word = list(game.__word)
        guessed_word = list(game.__guessed_word)
        string_db = stringDatabase.StringDatabase
        i = 0
        for guessed_word_letter in guessed_word:
            if guessed_word_letter == '-':
                score += string_db.get_letter_frequency(word[i])
            i = i + 1
        if game.__request_letter_freq != 0:
            score = score / game.__request_letter_freq
        incorrect_guess_cost = 0.1 * game.__missed_guess_freq
        score = score - (score * incorrect_guess_cost)
        return score

    @staticmethod
    def calculate_gave_up_score(game):
        """
        This method will calculate the score of the game in which player lost 
        :param game: specific game's instance
        :return: specific game's final score as number
        """
        score = 0
        word = list(game.__word)
        guessed_word = list(game.__guessed_word)
        string_db = stringDatabase.StringDatabase
        i = 0
        for guessed_word_letter in guessed_word:
            if guessed_word_letter != '-':
                score += string_db.get_letter_frequency(word[i])
            i = i + 1
        return -score

    @staticmethod
    def print_report(games):
        """
        This method will display the entire game's report
        :param games: as list
        """
        print("\nGame", '\t', "Word", '\t', "Status", '\t', "Bad Guesses", '\t', "Missed Letters", '\t', "Score")
        print("----", '\t', "----", '\t', "------", '\t', "-----------", '\t', "--------------", '\t', "-----")

        i = 1
        final_score = 0
        for game in games:
            if game.__status != 'Quit':
                print(i, '\t', game.__word, '\t', game.__status, '\t', game.__missed_guess_freq, '\t\t',
                      game.__missed_letter_freq, '\t\t\t', round(game.__score, 2))
                final_score = final_score + game.__score
                i = i + 1

        final_score = round(final_score, 2)
        print('\n\nFinal Score: ' + str(final_score))
