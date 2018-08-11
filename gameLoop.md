# Game Loop

- While TRUE :

  - user wants to quit if eascape key comes up or window is closed

  - if mouse is clicked, i.e. mouse button just came up, set mouse pointer coordinates, else coordinates -> None
  - obtain the "exact box" (row, column, box_r, box_c )at that pixel coordinate if coordinate is not None
  - if this box has already been won -> set exact_box -> None
  - if this small box already marked -> set box none

  - IF inside a valid BOX ( exact box,coordinates is not None)
  - ready to make a move -> X or O ( either player or computer)
  - make X/O move, make entry in Data Structure, sound Beep1/Beep2 as per move. You have now `MOVED` (can be removed)
  - set expected row/Column for next move

  - as soon as move is done.

# will be done at last - hold

- `De-highlight` all the boxes (1 mostly / many in "any case")

- check who won the current box with this move, if won/tie, make entry in win records & put in winner tuples, also hold Winner
- `if someone won`, increment the winner player's score, `pygame.time.wait(500)` for a delay efect and then `highlightWin` by drawing a line over won tuples, also play the `BEEP3`

- if expected row/Column is already won (Recheck global records) -> set expected = `"any"`
- Now `highlight` all the expected boxes (1 or "any")

- Board got changed because of this, Screen needs update
  In our case, everything needs to be redrawn, because we keep
  updating highlighted boxes and stuff.

winners independent
But, we made highlight and dehighlight independedent....

another approach -> keep them sane->

do heavy lifting at end,
this will take away the delay effect,-> even if conditioned

- unequal intervals

3 funcs
highlightWin -> draws line
highlight -> box
dehighlight -> box
-> once highlighted or dehighlighted -> all its members need to be redrawn as well

It's better to do everything at last

everything includes -> (if this combination does not work, go procedural)

1. paint the board black (will dehighlight all boxes) -> individual dehighlight not necessary

2. `highlightWin` for winners (those not None) -> (special focus to current winner) ?? i wanna see it go beep3()

3. `highlight expected` boxes (green surface draw) -> to be done via function call -> coordinate calculation -> green draw.

4. draw lines
5. `redraw()` all -> just extend over two loops

Cluttered code ->> do shit changes later
