# E3T
E3T - Extended Tic Tac Toe


## Build options
 
use this wonderful pyinstaller wrapper app [auto-py-to-exe](https://github.com/brentvollebregt/auto-py-to-exe) and make a single file in no console mode & bundle up all your resources in a single folder say `files`.

Extending the standard 3x3 tic tac toe to a 9x9 version with new rules.

## Development phase
- [X] starting to manipulate and see what's possible.
- Initial game screen - for New game. Do everything without exiting the app
- difficulty level - easy, headon

#### Two versions

- [X] maximum score - easy level - just compare score and give answer - implementation done
- [X] winner if 3 in a row - smart level - game early over - Implementation done  

## Todo List

- [X] Rename to Ultimate Tic tac toe
- [X] Add a 3x3 prototype
- [X] Document the prototype
- [X] Refer books, gain more pygame knowledge 
- [X] Define rules for new extended version
- [X] Define data structure
- [X] Start coding
- [X] Implement User 
- [ ] Implement AI
- [X] Graphics prototype
- [ ] Implementing
		- [X] small box win
		- [X] winning Line graphics
		- [X] Big win - TO DO NEXT
		- [ ] ~~Big win line~~
		- [ ] Game over
		- [ ] Tie
		- [ ] A `END GAME` button
		- [ ] proper score manip 

- [ ] clean up comments	
- [ ] Brush up code PEP8 style


## Rules

Ultimate Tic Tac Toe is 9 normal games of Tic Tac Toe played simultaneously. The board is made up of 9 tiles, each of which contains 9 squares. Your move will dictate where your opponent can play however. So if you play your piece in the top right square of a tile, then your opponent must play their next piece in the top right tile.

### There are two variations of this game:

#### First Tile Wins - The first player to win a single tile.
#### 3 Tiles in a Row (harder) - The first player to win 3 tiles in a row wins. The first player get's to place their piece in any square on the board. After that you are are limited to the tile your opponent sends you to. 

### There are two exceptions to this however.

- Your opponent sends you to a tile that has already been won (either by you or them).

- Your opponent sends you to a tile which is full.
If either of these occur then you get an open turn and may place your piece on any tile you like.