#!/usr/bin/env python3
"""
ASCII Minesweeper Game
A command-line version of the classic Minesweeper game using ASCII characters.
"""

import random
import os
import sys
import time

class MinesweeperGame:
    def __init__(self, width=10, height=10, mines=15):
        """Initialize the game with the specified dimensions and number of mines."""
        self.width = width
        self.height = height
        self.mines = mines
        self.board = []  # The actual board with mines and numbers
        self.display_board = []  # What the player sees
        self.first_move = True
        self.game_over = False
        self.win = False
        
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
        
        # Print column numbers
        print("   ", end="")
        for x in range(self.width):
            print(f"{x % 10} ", end="")
        print()
        
        # Print top border
        print("  +" + "-" * (self.width * 2 - 1) + "+")
        
        # Print rows
        for y in range(self.height):
            print(f"{y % 10} |", end="")
            for x in range(self.width):
                print(f"{self.display_board[y][x]} ", end="")
            print("|")
        
        # Print bottom border
        print("  +" + "-" * (self.width * 2 - 1) + "+")
        
        # Print game status
        if self.game_over:
            if self.win:
                print("You win! All mines flagged correctly.")
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
            self.display_board[y][x] = 'X'
            self.game_over = True
            self.reveal_all_mines()
            return True
        
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
                if self.board[y][x] == 'X' and self.display_board[y][x] != '⚑':
                    return False
        
        self.win = True
        self.game_over = True
        return True

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
                
                # Validate custom settings
                width = max(5, min(30, width))
                height = max(5, min(30, height))
                mines = max(1, min(width * height // 4, mines))
                
                return width, height, mines
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

def main():
    """Main function to run the game."""
    print("Welcome to ASCII Minesweeper!")
    print("------------------------------")
    
    # Get difficulty settings
    width, height, mines = get_difficulty()
    
    # Create the game
    game = MinesweeperGame(width, height, mines)
    
    # Main game loop
    while not game.game_over:
        game.display()
        
        # Get player command
        command = input("Enter command: ")
        cmd, x, y = parse_command(command)
        
        if cmd == 'r':
            game.reveal(x, y)
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
