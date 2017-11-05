# E3T
E3T - Extended Tic Tac Toe

Extending the standard 3x3 tic tac toe to a 9x9 version with new rules.

## Development phase
starting to manipulate and see what's possible.

## Todo List

- [ ] Rename to Ultimate Tic tac toe
- [X] Add a 3x3 prototype
- [X] Document the prototype
- [ ] Refer books, gain more pygame knowledge 
- [ ] Define rules for new extended version
- [X] Define data structure
- [X] Start coding
- [X] Implement User 
- [ ] Implement AI
- [ ] Graphics prototype
- [ ] Implementing
		- [ ] small box win
		- [ ] winning Line graphics
		- [ ] Big win
		- [ ] Game over
		- [ ] Tie


## Rules

Ultimate Tic Tac Toe is 9 normal games of Tic Tac Toe played simultaneously. The board is made up of 9 tiles, each of which contains 9 squares. Your move will dictate where your opponent can play however. So if you play your piece in the top right square of a tile, then your opponent must play their next piece in the top right tile.

### There are two variations of this game:

#### First Tile Wins - The first player to win a single tile.
#### 3 Tiles in a Row (harder) - The first player to win 3 tiles in a row wins. The first player get's to place their piece in any square on the board. After that you are are limited to the tile your opponent sends you to. 

### There are two exceptions to this however.

- Your opponent sends you to a tile that has already been won (either by you or them).

- Your opponent sends you to a tile which is full.
If either of these occur then you get an open turn and may place your piece on any tile you like.