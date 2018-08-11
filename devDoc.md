# Dev Doc

## Build options

use this wonderful pyinstaller wrapper app [auto-py-to-exe](https://github.com/brentvollebregt/auto-py-to-exe) and make a single file in no console mode & bundle up all your resources in a single folder say `files`.

- use `python -m pydoc -w tic_tac_toe` to generate documentation

## Versions

- [x] easy level - maximum score - just compare score and give answer - implementation done
- [x] smart level - winner if 3 in a row - game needs to be early over - Implementation done

## Task List

- [x] Rename to Ultimate Tic tac toe
- [x] Add a 3x3 [prototype](https://github.com/jatin69/ultimate-tic-tac-toe/tree/prototype)
- [x] Document the prototype
- [x] Refer books, gain more pygame knowledge
- [x] Define rules for new extended version
- [x] Define data structure
- [x] Start coding
- [x] Implement User
- [x] Graphics prototype
- [x] small box win
- [x] winning Line graphics
- [x] Big win implementation
- [ ] ~~Big win line~~ Big Win color
- [x] Tie Detection
- [x] difficulty - easy and smart
- [ ] Handle Key Presses
  - Press `Esc` to quit the application
  - Press `Q` to terminate current game
  - Press `N` to restart the game
- [X] modify score card
  - Player 1 ( X )
  - Player 2 ( O )
  - Tie
  - Winner is Player 1 ( X )
  - Winner is Player 2 ( O )
  - Font change maybe
  - space out a little
- [X] Implement computer move
   - [X] random
   - [X] AI
- [X] Refactor 'O' to Omark & 'X' to Xmark at all places
- [ ] Setup Proper color scheme
- [ ] Make more screens
  - [ ] Welcome screen
  - [ ] Choose Single Player (against AI) or Two Player
  - [X] single game ~~vs tournament (keeping track of multiple games)~~
  - [ ] Exit bye bye screeen
- [ ] Document code ( check out sphinx ) & clean up comments & Brush up code PEP8 style
- [ ] Document complete game loop
- [ ] Bundle up for release
- [ ] Upload to pygame store

## Bugs

- In scoreboard, with each win, `tie = 0` becomes `tie = 0))` . IDK why, gotta inspect

## Additional points

- ALso a possible data structure,, but will need to redefine my entire logic of finding coordinates,
```python
theBoard = {'top-L': 'O', 'top-M': 'O', 'top-R': 'O',
            'mid-L': 'X', 'mid-M': 'X', 'mid-R': ' ',
            'low-L': ' ', 'low-M': ' ', 'low-R': 'X'}
```