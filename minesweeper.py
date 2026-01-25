#!/usr/bin/env python3
"""
ASCII Minesweeper Game
A command-line version of the classic Minesweeper game using ASCII characters.
"""

import random
import os
import sys
import time
import readline
import argparse

class MinesweeperGame:
    def __init__(self, width=10, height=10, mines=15, lives=1):
        """Initialize the game with the specified dimensions and number of mines."""
        self.width = width
        self.height = height
        self.mines = mines
        self.board = []  # The actual board with mines and numbers
        self.display_board = []  # What the player sees
        self.first_move = True
        self.game_over = False
        self.win = False
        self.lives = lives  # Current remaining lives
        self.max_lives = lives  # Initial lives for UI display logic
        self.triggered_mines = set()  # Set of (x, y) tuples for hit mines
        
        # Initialize the boards
        self.initialize_boards()
    
    def initialize_boards(self):
        """Initialize the game boards."""
        # Initialize the actual board with empty cells
        self.board = [['0' for _ in range(self.width)] for _ in range(self.height)]
        
        # Initialize the display board with hidden cells
        self.display_board = [['■' for _ in range(self.width)] for _ in range(self.height)]
    
    def place_mines(self, first_x, first_y):
        """Place mines randomly on the board, avoiding the first clicked position."""
        mines_placed = 0
        while mines_placed < self.mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            
            # Avoid placing a mine at the first clicked position or adjacent to it
            if abs(x - first_x) <= 1 and abs(y - first_y) <= 1:
                continue
            
            # Place a mine if there isn't one already
            if self.board[y][x] != 'X':
                self.board[y][x] = 'X'
                mines_placed += 1
        
        # Calculate numbers for cells adjacent to mines
        self.calculate_numbers()
    
    def calculate_numbers(self):
        """Calculate the number of adjacent mines for each cell."""
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 'X':
                    continue
                
                # Count adjacent mines
                count = 0
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if dx == 0 and dy == 0:
                            continue
                        
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height and self.board[ny][nx] == 'X':
                            count += 1
                
                self.board[y][x] = str(count)
    
    def display(self):
        """Display the current state of the game."""
        os.system('clear' if os.name == 'posix' else 'cls')
        print("ASCII MINESWEEPER")
        print(f"Mines: {self.mines}")
        # Show lives counter only if max_lives > 1
        if self.max_lives > 1:
            print(f"Lives: {self.lives}")

        # Print column numbers at top
        print("   ", end="")
        for x in range(self.width):
            print(f"{x % 10} ", end="")
        # Add column numbers at top right if width >= 10
        if self.width >= 10:
            print("  ")
        else:
            print()

        # Print top border
        print("  +" + "-" * (self.width * 2 - 1) + "+")

        # Print rows
        for y in range(self.height):
            print(f"{y % 10} |", end="")
            for x in range(self.width):
                cell = self.display_board[y][x]
                # Display flags in red
                if cell == '⚑':
                    print(f"\033[91m{cell}\033[0m ", end="")
                # Display triggered mines in red
                elif (x, y) in self.triggered_mines and cell == 'X':
                    print(f"\033[91m{cell}\033[0m ", end="")
                else:
                    print(f"{cell} ", end="")
            print("|", end="")
            # Add row numbers on the right if height >= 10
            if self.height >= 10:
                print(f" {y % 10}")
            else:
                print()

        # Print bottom border
        print("  +" + "-" * (self.width * 2 - 1) + "+")

        # Print column numbers at bottom if width >= 10
        if self.width >= 10:
            print("   ", end="")
            for x in range(self.width):
                print(f"{x % 10} ", end="")
            print()

        # Print game status
        if self.game_over:
            if self.win:
                print("You win! All mines flagged correctly.")
            else:
                if self.lives == 0:
                    print("Game over! You ran out of lives.")
                else:
                    print("Game over! You hit a mine.")
        else:
            print("Commands: r x y (reveal), f x y (flag), u x y (unflag), q (quit)")
    
    def reveal(self, x, y):
        """Reveal a cell at the specified coordinates."""
        # Check if coordinates are valid
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        
        # Check if the cell is already revealed or flagged
        if self.display_board[y][x] != '■':
            return False
        
        # If it's the first move, place mines
        if self.first_move:
            self.place_mines(x, y)
            self.first_move = False
        
        # Check if the cell contains a mine
        if self.board[y][x] == 'X':
            self.lives -= 1
            self.triggered_mines.add((x, y))
            self.display_board[y][x] = 'X'

            if self.lives == 0:
                self.game_over = True
                self.reveal_all_mines()

            return 'mine'
        
        # Reveal the cell
        self.display_board[y][x] = self.board[y][x]
        
        # If the cell has no adjacent mines, reveal adjacent cells recursively
        if self.board[y][x] == '0':
            self.display_board[y][x] = ' '
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        self.reveal(nx, ny)
        
        # Check if the player has won
        self.check_win()
        return True

    def handle_mine_hit(self):
        """Handle the mine explosion animation and pause."""
        self.display()
        print("\nBOOM!")
        if self.lives > 0:
            life_word = "life" if self.lives == 1 else "lives"
            print(f"You hit a mine! {self.lives} {life_word} remaining.")
            input("Press Enter to continue...")
        else:
            print("You hit a mine!")

    def flag(self, x, y):
        """Flag a cell at the specified coordinates."""
        # Check if coordinates are valid
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        
        # Check if the cell is hidden
        if self.display_board[y][x] == '■':
            self.display_board[y][x] = '⚑'
            self.check_win()
            return True
        
        return False
    
    def unflag(self, x, y):
        """Remove a flag from a cell at the specified coordinates."""
        # Check if coordinates are valid
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        
        # Check if the cell is flagged
        if self.display_board[y][x] == '⚑':
            self.display_board[y][x] = '■'
            return True
        
        return False
    
    def reveal_all_mines(self):
        """Reveal all mines on the board."""
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 'X':
                    self.display_board[y][x] = 'X'
    
    def check_win(self):
        """Check if the player has won the game."""
        # The player wins if all non-mine cells are revealed
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != 'X' and self.display_board[y][x] in ['■', '⚑']:
                    return False
                # Allow triggered mines to count toward win condition
                if self.board[y][x] == 'X':
                    if (x, y) not in self.triggered_mines and self.display_board[y][x] != '⚑':
                        return False

        self.win = True
        self.game_over = True
        return True

def validate_game_settings(width, height, mines):
    """Validate and clamp game settings to acceptable ranges."""
    width = max(5, min(30, width))
    height = max(5, min(30, height))
    mines = max(1, min(width * height // 4, mines))
    return width, height, mines

def get_difficulty():
    """Get the difficulty level from the player."""
    print("Select difficulty:")
    print("1. Easy (10x10, 15 mines)")
    print("2. Medium (16x16, 40 mines)")
    print("3. Hard (24x24, 99 mines)")
    print("4. Custom")
    
    while True:
        try:
            choice = input("Enter your choice (1-4): ")
            if choice == '1':
                return 10, 10, 15
            elif choice == '2':
                return 16, 16, 40
            elif choice == '3':
                return 24, 24, 99
            elif choice == '4':
                width = int(input("Enter width (5-30): "))
                height = int(input("Enter height (5-30): "))
                mines = int(input(f"Enter number of mines (1-{width * height // 4}): "))

                return validate_game_settings(width, height, mines)
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def parse_command(command):
    """Parse a command string into a command and coordinates."""
    parts = command.strip().lower().split()
    
    if not parts:
        return None, None, None
    
    cmd = parts[0]
    
    if cmd == 'q':
        return cmd, None, None
    
    if len(parts) < 3:
        return None, None, None
    
    try:
        x = int(parts[1])
        y = int(parts[2])
        return cmd, x, y
    except ValueError:
        return None, None, None

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='ASCII Minesweeper - A command-line version of the classic Minesweeper game'
    )

    parser.add_argument(
        '-d', '--difficulty',
        choices=['e', 'easy', 'm', 'medium', 'h', 'hard'],
        help='Difficulty level: e/easy, m/medium, h/hard'
    )

    parser.add_argument(
        '-w', '--width',
        type=int,
        help='Board width (5-30, only for custom difficulty)'
    )

    parser.add_argument(
        '-l', '--length',
        type=int,
        help='Board height (5-30, only for custom difficulty)'
    )

    parser.add_argument(
        '-m', '--mines',
        type=int,
        help='Number of mines (only for custom difficulty)'
    )

    parser.add_argument(
        '-v', '--lives',
        type=int,
        default=1,
        help='Number of lives (default: 1)'
    )

    return parser.parse_args()

def get_game_settings(args):
    """Get game settings from command-line arguments or interactive mode.
    Returns (width, height, mines, lives) tuple."""
    # Check if difficulty is specified
    if args.difficulty:
        diff = args.difficulty.lower()
        if diff in ['e', 'easy']:
            return 10, 10, 15, args.lives
        elif diff in ['m', 'medium']:
            return 16, 16, 40, args.lives
        elif diff in ['h', 'hard']:
            return 24, 24, 99, args.lives

    # Check if custom dimensions are provided
    if args.width is not None or args.length is not None or args.mines is not None:
        # Default to easy settings if not all custom parameters are provided
        width = args.width if args.width is not None else 10
        height = args.length if args.length is not None else 10

        # Calculate default mines based on board size if not specified
        if args.mines is not None:
            mines = args.mines
        else:
            mines = max(1, (width * height) // 6)

        return validate_game_settings(width, height, mines) + (args.lives,)

    # No command-line arguments, use interactive mode
    return None

def main():
    """Main function to run the game."""
    print("Welcome to ASCII Minesweeper!")
    print("------------------------------")

    # Parse command-line arguments
    args = parse_arguments()

    # Get difficulty settings from arguments or interactive mode
    settings = get_game_settings(args)
    if settings:
        width, height, mines, lives = settings
    else:
        width, height, mines = get_difficulty()
        lives = 1  # Default lives for interactive mode

    # Create the game
    game = MinesweeperGame(width, height, mines, lives)
    
    # Main game loop
    while not game.game_over:
        game.display()
        
        # Get player command
        command = input("Enter command: ")
        cmd, x, y = parse_command(command)
        
        if cmd == 'r':
            result = game.reveal(x, y)
            if result == 'mine':
                game.handle_mine_hit()
        elif cmd == 'f':
            game.flag(x, y)
        elif cmd == 'u':
            game.unflag(x, y)
        elif cmd == 'q':
            print("Thanks for playing!")
            return
        else:
            print("Invalid command. Try 'r x y', 'f x y', 'u x y', or 'q'.")
            time.sleep(1)
    
    # Final display after game over
    game.display()
    
    # Ask to play again
    play_again = input("Play again? (y/n): ").strip().lower()
    if play_again == 'y':
        main()
    else:
        print("Thanks for playing!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame terminated by user.")
        sys.exit(0)
