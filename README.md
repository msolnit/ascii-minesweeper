# ASCII Minesweeper

A command-line version of the classic Minesweeper game using ASCII characters.

## Description

This is a fully-featured Minesweeper game that runs in your terminal. The game includes:

- Multiple difficulty levels (Easy, Medium, Hard, and Custom)
- ASCII-based interface
- Flag and unflag functionality
- First-click protection (you'll never hit a mine on your first move)
- Auto-reveal for empty cells

## How to Play

1. Run the game using Python:
   ```
   python minesweeper.py
   ```
   
   Or make it executable and run directly:
   ```
   chmod +x minesweeper.py
   ./minesweeper.py
   ```

2. Select a difficulty level:
   - Easy: 10x10 grid with 15 mines
   - Medium: 16x16 grid with 40 mines
   - Hard: 24x24 grid with 99 mines
   - Custom: Define your own grid size and number of mines

3. Game Commands:
   - `reveal x y`: Reveal the cell at coordinates (x, y)
   - `flag x y`: Place a flag at coordinates (x, y)
   - `unflag x y`: Remove a flag from coordinates (x, y)
   - `quit`: Exit the game

4. Game Rules:
   - Numbers indicate how many mines are adjacent to that cell
   - Flag all mines to win
   - If you reveal a mine, you lose
   - Empty cells (shown as spaces) automatically reveal adjacent cells

## Symbols

- `■`: Hidden cell
- `⚑`: Flagged cell
- `X`: Mine (only shown when game is over)
- `0-8`: Number of adjacent mines (0 is displayed as a space)

## Tips

- Your first move is always safe
- Use flags to mark cells you suspect contain mines
- Use the numbers to deduce where mines are located

Enjoy the game!
