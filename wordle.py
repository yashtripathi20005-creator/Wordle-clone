#!/usr/bin/env python3
"""
Wordle Clone - A terminal-based Wordle game
"""

import random
import sys
from colorama import init, Fore, Back, Style

# Initialize colorama for cross-platform color support
init(autoreset=True)

# Constants
MAX_ATTEMPTS = 6
WORD_LENGTH = 5


class WordleGame:
    """Main Wordle game class"""
    
    def __init__(self, word_list_path="wordlist.txt"):
        self.word_list_path = word_list_path
        self.words = self.load_words()
        self.target_word = ""
        self.attempts = []
        self.current_attempt = 0
        self.game_over = False
        self.won = False
        
    def load_words(self):
        """Load words from file or use default list"""
        try:
            with open(self.word_list_path, 'r') as f:
                words = [word.strip().upper() for word in f.readlines() 
                        if len(word.strip()) == WORD_LENGTH]
            if not words:
                raise ValueError("No valid words found")
            return words
        except (FileNotFoundError, ValueError):
            print(f"Warning: Could not load word list. Using default words.")
            return self.get_default_words()
    
    def get_default_words(self):
        """Return a default list of 5-letter words"""
        return [
            "APPLE", "BRAIN", "CHAIN", "DANCE", "EAGLE",
            "FLOUR", "GRACE", "HEART", "IMAGE", "JOKER",
            "KNIFE", "LIGHT", "MAGIC", "NIGHT", "OCEAN",
            "PEACE", "QUEEN", "RIVER", "STONE", "TIGER",
            "UNITY", "VALUE", "WATER", "XENON", "YOUTH",
            "ZEBRA", "CLOUD", "DREAM", "EARTH", "FLAME",
            "GREEN", "HAPPY", "IRONY", "JUICE", "KNEEL",
            "LAUGH", "MIRTH", "NOBLE", "OPERA", "PRIDE"
        ]
    
    def new_game(self):
        """Start a new game with a random word"""
        self.target_word = random.choice(self.words)
        self.attempts = []
        self.current_attempt = 0
        self.game_over = False
        self.won = False
    
    def make_guess(self, guess):
        """
        Process a player's guess
        Returns a list of (letter, color) tuples
        """
        if self.game_over:
            return None
        
        if len(guess) != WORD_LENGTH:
            return None
        
        guess = guess.upper()
        
        if not guess.isalpha():
            return None
        
        # Check if word is in dictionary
        if guess not in self.words:
            return None
        
        # Process the guess
        result = []
        target_list = list(self.target_word)
        guess_list = list(guess)
        
        # First pass: mark correct letters (green)
        for i in range(WORD_LENGTH):
            if guess_list[i] == target_list[i]:
                result.append((guess_list[i], 'green'))
                target_list[i] = None
                guess_list[i] = None
        
        # Second pass: mark misplaced letters (yellow)
        for i in range(WORD_LENGTH):
            if guess_list[i] is not None:
                if guess_list[i] in target_list:
                    result.append((guess_list[i], 'yellow'))
                    target_list[target_list.index(guess_list[i])] = None
                else:
                    result.append((guess_list[i], 'gray'))
        
        self.attempts.append(result)
        self.current_attempt += 1
        
        # Check win/lose conditions
        if guess == self.target_word:
            self.won = True
            self.game_over = True
        elif self.current_attempt >= MAX_ATTEMPTS:
            self.game_over = True
        
        return result
    
    def get_display_text(self):
        """Generate the game display text"""
        display = []
        
        # Header
        display.append(f"{'=' * 30}")
        display.append(f"  WORDLE CLONE  ({WORD_LENGTH} letters)")
        display.append(f"{'=' * 30}")
        
        # Show attempts
        for i in range(MAX_ATTEMPTS):
            if i < len(self.attempts):
                line = ""
                for letter, color in self.attempts[i]:
                    if color == 'green':
                        line += f"{Back.GREEN}{Fore.WHITE} {letter} {Style.RESET_ALL}"
                    elif color == 'yellow':
                        line += f"{Back.YELLOW}{Fore.BLACK} {letter} {Style.RESET_ALL}"
                    else:  # gray
                        line += f"{Back.LIGHTBLACK_EX}{Fore.WHITE} {letter} {Style.RESET_ALL}"
                display.append(line)
            else:
                display.append("_ " * WORD_LENGTH)
        
        # Show status
        display.append("-" * 30)
        if self.game_over:
            if self.won:
                display.append(f"{Fore.GREEN}🎉 YOU WON! 🎉")
                display.append(f"Word: {self.target_word}")
            else:
                display.append(f"{Fore.RED}😞 GAME OVER!")
                display.append(f"The word was: {Fore.YELLOW}{self.target_word}")
            display.append(f"Attempts: {self.current_attempt}/{MAX_ATTEMPTS}")
        else:
            display.append(f"Attempts: {self.current_attempt}/{MAX_ATTEMPTS}")
            display.append(f"Type a {WORD_LENGTH}-letter word:")
        
        display.append(f"{'=' * 30}")
        return "\n".join(display)


def play_game():
    """Main game loop"""
    game = WordleGame()
    
    print(f"{Fore.CYAN}{'=' * 40}")
    print(f"{Fore.CYAN}  WELCOME TO WORDLE CLONE!")
    print(f"{Fore.CYAN}  Guess the {WORD_LENGTH}-letter word in {MAX_ATTEMPTS} tries.")
    print(f"{Fore.CYAN}  Green: Correct letter and position")
    print(f"{Fore.CYAN}  Yellow: Correct letter, wrong position")
    print(f"{Fore.CYAN}  Gray: Letter not in word")
    print(f"{Fore.CYAN}{'=' * 40}\n")
    
    while True:
        game.new_game()
        
        while not game.game_over:
            print(game.get_display_text())
            
            # Get user input
            guess = input("> ").strip()
            
            if guess.lower() in ['quit', 'exit', 'q']:
                print(f"\nGoodbye! The word was {game.target_word}")
                return
            
            result = game.make_guess(guess)
            
            if result is None:
                print(f"{Fore.RED}Invalid guess. Please enter a valid {WORD_LENGTH}-letter word.")
                continue
        
        # Game over - show final state
        print(game.get_display_text())
        
        # Ask to play again
        while True:
            play_again = input(f"\nPlay again? (y/n): ").strip().lower()
            if play_again in ['y', 'yes']:
                break
            elif play_again in ['n', 'no']:
                print(f"\n{Fore.GREEN}Thanks for playing! Goodbye! 👋")
                return
            else:
                print(f"{Fore.RED}Please enter 'y' or 'n'.")


if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Game interrupted. Goodbye!")
        sys.exit(0)
