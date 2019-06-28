"""
A simple command-line game that allows people to guess 4 letter English words called- Guess Moi
This module controls the entire game flow by interacting with other modules in the package
"""

import game
import stringDatabase
import random


class Guess:
    """
    This class represents the game itself (including the menu)
    """

    string_database = stringDatabase.StringDatabase()

    current_guess_word = ''

    current_player_guess_word = ''

    games = []

    def __init__(self):
        """
        Constructor that starts the game by invoking the start_game() method
        """
        print('\n???? Guess Moi Game ????\n')
        self.start_game()

    @classmethod
    def start_game(cls):
        """
        This method controls the game flow by interacting with user to get input and displays an output appropriately  
        """
        game_over = 0
        game_limit = 0
        while game_over == 0 and game_limit < 100:
            cls.select_random_guess_word()
            print("\n***New Round Begins***\n")
            choice = []
            missed_letter_freq = 0
            missed_guess_freq = 0
            request_letter_freq = 0
            round_started = 0
            status = ''
            score = 0
            round_over = 0
            quit_game = 0
            won = 0
            current_game = game.Game(cls.current_guess_word, choice, missed_letter_freq, missed_guess_freq,
                                     request_letter_freq, status, score, cls.current_player_guess_word)
            cls.current_player_guess_word = '----'
            while round_over == 0:
                print('\nCurrent Word: ' + cls.current_guess_word)
                print('\nCurrent Guess: ' + cls.current_player_guess_word)
                round_choice = cls.game_menu()
                if round_choice == 'g':
                    round_started = 1
                    choice.append('g')
                    if cls.is_correct_guess():
                        print('Brilliant Guess! You Won this round !')
                        status = 'Success'
                        won = 1
                        round_over = 1
                    else:
                        missed_guess_freq = missed_guess_freq + 1
                        print('Ops Wrong Guess! Try Again...')
                elif round_choice == 't':
                    round_started = 1
                    choice.append('t')
                    if cls.confirm_quit():
                        print('\nThe Word is- ' + cls.current_guess_word)
                        status = 'Gave up'
                        round_over = 1
                    else:
                        print('Great! Keep Trying...')
                elif round_choice == 'l':
                    round_started = 1
                    choice.append('l')
                    request_letter_freq = request_letter_freq + 1
                    if cls.is_correct_letter():
                        print('Great! Wohooo')
                    else:
                        missed_letter_freq = missed_letter_freq + 1
                        print('Ops Wrong guess! Try Again...')
                elif round_choice == 'q':
                    choice.append('q')
                    if cls.confirm_quit():
                        if round_started == 1:
                            status = 'Gave up'
                        else:
                            status = 'Quit'
                        round_over = 1
                        quit_game = 1
                if won == 0:
                    if cls.is_found_word():
                        status = 'Success'
                        won = 1
                        round_over = 1
            current_game.set_choice(choice)
            current_game.set_status(status)
            current_game.set_missed_guess_frequency(missed_guess_freq)
            current_game.set_missed_letter_frequency(missed_letter_freq)
            current_game.set_request_letter_frequency(missed_letter_freq)
            current_game.set_guessed_word(cls.current_player_guess_word)
            current_game.set_score(current_game.calculate_game_score(current_game))
            cls.games.append(current_game)
            if quit_game == 1:
                game_over = 1
            game_limit = game_limit + 1
        # print report
        game.Game.print_report(cls.games)

    @classmethod
    def select_random_guess_word(cls):
        """
        This method will set the random word from StringDatabase to current_guess_word 
        """
        cls.string_database.read_guess_words_from_file()
        cls.current_guess_word = random.choice(cls.string_database.guess_words)

    @staticmethod
    def game_menu():
        """
        This method will display the game menu and prompts the player to enter their choice
        :return: user's choice as a character from game menu
        """
        return input('\ng = guess, t = tell me, l for a letter, and q to quit\nEnter your choice:')

    @staticmethod
    def confirm_quit():
        """
        This method will display a confirm message to quit and prompt player to enter their choice 
        :return: player's choice as a boolean value- 1 if yes, 0 if no
        """
        confirm = input('\nAre you sure? (yes or no)- ')
        if confirm.lower() == 'yes':
            return 1
        return 0

    @classmethod
    def is_correct_guess(cls):
        """
        This method will display a prompt message to let player enter a word to guess the string directly and checks if the string is same as the currect guess word
        :return: 1 if correct guess, else 0
        """
        if cls.current_guess_word == input('\nEnter your guess- ').lower():
            return 1
        return 0

    @classmethod
    def is_correct_letter(cls):
        """
        This method will prompt player to enter a letter and checks if the letter exists in the currect guess word
        :return: 1 if correct letter guess, else 0
        """
        correct_letter = 0
        correct_letter_counter = 0
        i = 0
        letter = input('\nEnter a letter- ').lower()
        player_guess_word = list(cls.current_player_guess_word)
        for word_letter in cls.current_guess_word:
            if letter == word_letter:
                correct_letter = 1
                correct_letter_counter = correct_letter_counter + 1
                player_guess_word[i] = letter
            i = i + 1
        cls.current_player_guess_word = "".join(player_guess_word)
        if correct_letter == 1:
            if correct_letter_counter == 1:
                print('\nYou found 1 letter')
            else:
                print('\nYou found ' + str(correct_letter_counter) + ' letters')
        return correct_letter

    @classmethod
    def is_found_word(cls):
        """
        This method checks if the player has found the entire current guess word
        :return: 1 if player has won the round, else 0
        """
        if cls.current_guess_word == cls.current_player_guess_word:
            print('\nBrilliant! You Won this round!')
            return 1
        return 0


new_game = Guess()
