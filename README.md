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

### Quick Start

Option 1: Run the game without command-line parameters, and it will guide you through the options.
```
python minesweeper.py
```

Option 2: Run the game with command-line options to skip past the menu:
```bash
python minesweeper.py -d easy         # Start an easy game
python minesweeper.py -d m            # Start a medium game (short form)
python minesweeper.py -d hard         # Start a hard game
python minesweeper.py -w 15 -l 12 -m 20  # Custom 15x12 board with 20 mines
```

### Command-Line Options

- `-d, --difficulty {e,easy,m,medium,h,hard}` - Set difficulty level
- `-w, --width <5-30>` - Set board width (for custom games)
- `-l, --length <5-30>` - Set board height (for custom games)
- `-m, --mines <number>` - Set number of mines (for custom games)

**Examples:**
```bash
python minesweeper.py -d e                    # Easy game (short form)
python minesweeper.py --difficulty medium     # Medium game (long form)
python minesweeper.py -w 20 -l 20 -m 50       # Custom 20x20 with 50 mines
python minesweeper.py -w 12 -l 8              # Custom size, auto-calculate mines
```

### Difficulty Levels

- **Easy**: 10x10 grid with 15 mines
- **Medium**: 16x16 grid with 40 mines
- **Hard**: 24x24 grid with 99 mines
- **Custom**: Define your own grid size (5-30) and number of mines

### In-Game Commands

- `r x y` - Reveal the cell at coordinates (x, y)
- `f x y` - Place a flag at coordinates (x, y)
- `u x y` - Remove a flag from coordinates (x, y)
- `q` - Quit the game

Use the up/down arrow keys to access command history.

### Game Rules

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
