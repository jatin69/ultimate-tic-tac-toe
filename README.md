# Ultimate Tic Tac Toe

~~E3T - Extended Tic Tac Toe~~

Extending the standard 3x3 tic tac toe to a 9x9 version with new rules.

## Rules

Ultimate Tic Tac Toe is 9 normal games of Tic Tac Toe played simultaneously. The board is made up of 9 tiles, each of which contains 9 squares. Your move will dictate where your opponent can play however. So if you play your piece in the top right square of a tile, then your opponent must play their next piece in the top right tile. The first player get's to place their piece in any square on the board. After that you are are limited to the tile your opponent sends you to.

## Two Versions

### First Tile Wins (Easy)

The first player to win a maximum tiles.

### 3 Tiles in a Row (Smart)

The first player to win 3 tiles in a row wins.

## Rule Exceptions

There are two exceptions to this however.

- Your opponent sends you to a tile that has already been won (either by you or them).
- Your opponent sends you to a tile which is full.

If either of these occur then you get an open turn and may place your piece on any tile you like.

## Additional Information

- If you are interested in reading the details of game loop, refer [here](gameLoop.md)
- If you are interested in reading about the minute details, refer the [dev doc](devDoc.md)
