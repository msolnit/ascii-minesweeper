# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Game

```bash
# Run with Python 3
python3 minesweeper.py

# Or run directly (executable)
./minesweeper.py

# Run with command-line options
python3 minesweeper.py -d easy              # Quick start with easy difficulty
python3 minesweeper.py -d m                 # Medium difficulty (short form)
python3 minesweeper.py -w 12 -l 8 -m 10     # Custom board: 12x8 with 10 mines
python3 minesweeper.py --help               # See all options
```

## Code Architecture

This is a single-file Python CLI game. The codebase follows a clear separation between game logic and user interaction:

### MinesweeperGame Class (lines 14-217)

The core game engine that maintains two parallel 2D arrays:
- `self.board`: The actual game state (mines='X', numbers='0'-'8')
- `self.display_board`: What the player sees (hidden='■', flag='⚑', or revealed values)

**Key architectural decisions:**
- **Lazy mine placement**: Mines are NOT placed during `__init__()`. They're placed on first move via `place_mines(first_x, first_y)` to guarantee first-click safety.
- **Recursive reveal**: When a '0' cell is revealed, `reveal()` calls itself recursively on adjacent cells.
- **Win condition**: Player must reveal all non-mine cells AND flag all mines correctly.

### Game Flow Functions (lines 220-359)

Three-stage initialization:
1. `parse_arguments()`: Parse command-line args using argparse
2. `get_game_settings(args)`: Convert args to (width, height, mines) tuple, or return None for interactive mode
3. `get_difficulty()`: Interactive prompts (only called if no CLI args)

All custom settings pass through `validate_game_settings()` which clamps values to valid ranges (width/height: 5-30, mines: 1 to 25% of board).

### Command Parsing

Commands shortened in recent commits:
- `r x y` = reveal
- `f x y` = flag
- `u x y` = unflag
- `q` = quit

The game uses `readline` for command history (up/down arrows work).

## Display System

- Uses ANSI escape codes for clearing screen (`os.system('clear')` on POSIX, `cls` on Windows)
- Flags displayed in red using ANSI color codes: `\033[91m⚑\033[0m`
- Row/column numbers shown on all 4 edges when board size >= 10 to help with coordinate entry
- Coordinate system: (0,0) is top-left, x=column, y=row

## Validation and Constraints

- Board dimensions: 5-30 (enforced by `validate_game_settings()`)
- Mine count: 1 to 25% of total cells
- Out-of-range values are clamped, not rejected
- Command-line custom dimensions (`-w`, `-l`, `-m`) can be partially specified; missing values default to 10 (or calculated mines if only dimensions given)
