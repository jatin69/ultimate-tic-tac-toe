import pygame, sys, random, copy
from pygame.locals import *

# CONSTANTS, yo

# Game window width and height



makeFullscreen = True
# If fullscreen, use user's current resolution
makeFullscreen = False
# else use these window coordinates
# else use these window coordinates
WINDOWWIDTH = 800
WINDOWHEIGHT = 768

# The infinite loops runs 30 times in one second
# This much FPS is enough.
FPS = 30

# How big should be one small box
# when you modify this, also modify the main font, as the X lives inside a box
BOXSIZE = 43

MARKSIZE = 41

SMALLFONTSIZE = 30

# Width of the line in pixels : This is the thing that actually separate the input small boxes
GAPSIZE = 2

BIGBOXSIZE = 3

# square board size
BOARDSIZE = 9

# Playing board width : How many small boxes needs to fit in the board
BOARDWIDTH = BOARDSIZE
BOARDHEIGHT = BOARDSIZE

# TEXT Markers to be drawn
XMARK = 'X'
OMARK = 'O'

'''
Board size = BOXSIZE + GAPSIZE
# The BOARD IS SQUARE. so same size in width and height.

remaining space on X axis = (Window width - Board size)
Margin on X axis = remaining space on X axis // 2

remaining space on Y axis = (Window height - Board size)
Margin on Y axis = remaining space on Y axis // 2

Note that these margins are coordinates

'''

XMARGIN = (WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) // 2
YMARGIN = (WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) // 2

# RGB COLOUR MODEL
#            R    G    B
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COMBLUE = (233, 232, 255)

# GAME COLOURS

# Background Color
BGCOLOR = BLACK

# BOX color - UNUSED AS OF NOW
# BOXCOLOR = BLUE

# The line which joins 3 consecutive elements at the end
LINECOLOR = YELLOW


def main():
    # Initialise pygame to access all video modules
    pygame.init()

    global FPSCLOCK, DISPLAYSURFACE, winner_records

    # Hold the clock as a variable - to tick later : controls the loop iterations per second.
    FPSCLOCK = pygame.time.Clock()

    # The Surface over which everything will be drawn - Window width and height

    if (makeFullscreen):
        # Get user's screen resolution
        user_info = pygame.display.Info()
        DISPLAYSURFACE = pygame.display.set_mode((user_info.current_w, user_info.current_h), pygame.FULLSCREEN)
    else:
        DISPLAYSURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    # mainFont : Font for drawing X and O in the boxes
    # Modification required : Remove magic number & put something relative to box
    mainFont = pygame.font.SysFont('Helvetica', MARKSIZE)

    # smallFont : draws the score box and the end game credits
    smallFont = pygame.font.SysFont('Helvetica', SMALLFONTSIZE)

    # Caption of window
    pygame.display.set_caption('Tic-Tac-Toe dev')

    # Mouse coordinates
    mousex = 0
    mousey = 0

    # score board variables
    playerScore = 0
    computerScore = 0
    tieScore = 0
    playerWins = False
    computerWins = False

    # sounds
    # sound of Player move
    BEEP1 = pygame.mixer.Sound('beep2.ogg')
    # sound of computer move
    BEEP2 = pygame.mixer.Sound('beep3.ogg')

    # Winning sound of any player
    BEEP3 = pygame.mixer.Sound('beep1.ogg')

    # computer voice at the end of game
    COMPUTERVOICE = pygame.mixer.Sound('wargamesclip.ogg')

    '''
    Defines the major data structure 
    The whole Board is a list of list.  [ [col1], [col2], [col3] ]
    The function makeEachBoxFalse() returns a list of all false boxes
    '''
    # Main board variable
    # change its name to initialise....
    mainBoard, winner_records = makeEachBoxFalse(False)
    # Initially used boxes
    # usedBoxes = makeEachBoxFalse(False)

    # Player turn : bool variable
    game_turn = 'player'

    # Paint the surface black
    DISPLAYSURFACE.fill(BGCOLOR)

    '''
    Draw all the required lines
    '''
    drawLines()

    # highlight(mainBoard, 0)

    # The GRAND game loop

    expected_row = None
    expected_column = None

    while True:

        # set mouseClick as False
        mouseClicked = False

        # did the player move
        moved = False

        # Check for events for event queue
        for event in pygame.event.get():

            # For Game exiting
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If mouse is moving, update the location
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos

            # If mouse button just came up, it means the button is clicked
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        '''
        @:purpose : when mouse is clicked, we need to put X or O at the correct box
        So to obtain the exact box where the mouse is clicked, this function is used.
        @:returns: The box coordinates, where mouse is clicked
        '''
        row, column, box_row, box_column = getBoxAtPixel(mousex, mousey)
        # correct here, perfect
        # print(row, column, box_row, box_column)

        # Firstmost turn

        # This code just highlights
        # actual law enforcement must be done


        # mouse is clicked + not first time
        if mouseClicked and expected_column is not None and expected_row is not None:

            if expected_row == 'any' and expected_column == 'any':
                for i in range(3):
                    for j in range(3):
                        # match entered row and stuff
                        if row == i and column == j:
                            # If not a non winner - reject
                            if winner_records[i][j][0]['winner'] != None:
                                row = None
                                column = None
                                # matched with clicked box



            # + row does not match expected
            elif (row != expected_row or column != expected_column):
                row = None
                column = None
                pygame.display.update()
                highlight(mainBoard, expected_row, expected_column, GREEN)

                # print(row, column)

        # If Inside the board, move forward, else ignore
        if row is not None and column is not None and box_row is not None and box_column is not None:

            if game_turn == 'player' and mainBoard[row][column][box_row][box_column] is False and mouseClicked:
                markBox(row, column, box_row, box_column, mainFont, XMARK)
                BEEP1.play()
                mainBoard[row][column][box_row][box_column] = XMARK
                # Player turn done
                game_turn = 'computer'

                expected_row = box_row
                expected_column = box_column

                # remove green color
                # dehighlight(mainBoard, row, column)
                # In case of any, i gotta dehighlight everything..... focus
                for i in range(3):
                    for j in range(3):
                        dehighlight(mainBoard, i, j)

                pygame.display.update()
                highlight(mainBoard, expected_row, expected_column, GREEN)

                if winner_records[expected_row][expected_column][0]['winner'] is not None:
                    expected_row = 'any'
                    expected_column = 'any'

                    if expected_row == 'any' and expected_column == 'any':
                        # highlight all valid boxes
                        for i in range(3):
                            for j in range(3):
                                if winner_records[i][j][0]['winner'] is None:
                                    highlight(mainBoard, i, j, GREEN)
                                else:
                                    dehighlight(mainBoard, i, j)


                else:
                    # just green color
                    highlight(mainBoard, expected_row, expected_column, GREEN)



                    # highlight all expect this, make it red
                    # neh, not now - later RED
                    # highlight(mainBoard, expected_row, expected_column, RED)
                    # for i in range(3):
                    #     for j in range(3):
                    #         if winner_records[i][j][0]['winner'] is None:
                    #             highlight(mainBoard, i, j, GREEN)
                    #         else:
                    #             dehighlight(mainBoard, i, j)
                    #
                    # expected_row = 'any'
                    # expected_column = 'any'

                # else:
                #     # highlight needed and dehighlight all
                #     highlight(mainBoard, expected_row, expected_column, GREEN)
                #     for i in range(3):
                #         for j in range(3):
                #             if i==expected_row and j==expected_column:
                #                 highlight(mainBoard, i, j, GREEN)
                #             else:
                #                 dehighlight(mainBoard, i, j)
                #     # just redundant checks
                #     expected_row = i
                #     expected_column = j

                pygame.time.wait(500)
                pygame.display.update()
                moved = True

            # make it mouse clickable for now, add AI Later
            elif game_turn == 'computer' and mainBoard[row][column][box_row][box_column] is False and mouseClicked:
                # derive move from AI later
                markBox(row, column, box_row, box_column, mainFont, OMARK)
                BEEP2.play()
                mainBoard[row][column][box_row][box_column] = OMARK
                # Player turn done
                game_turn = 'player'

                expected_row = box_row
                expected_column = box_column

                # remove green color
                # dehighlight(mainBoard, row, column)
                # In case of any, i gotta dehighlight everything..... focus
                for i in range(3):
                    for j in range(3):
                        dehighlight(mainBoard, i, j)

                pygame.display.update()
                highlight(mainBoard, expected_row, expected_column, GREEN)

                if winner_records[expected_row][expected_column][0]['winner'] is not None:
                    expected_row = 'any'
                    expected_column = 'any'

                    if expected_row == 'any' and expected_column == 'any':
                        # highlight all valid boxes
                        for i in range(3):
                            for j in range(3):
                                if winner_records[i][j][0]['winner'] is None:
                                    highlight(mainBoard, i, j, GREEN)
                                else:
                                    dehighlight(mainBoard, i, j)


                else:
                    # just green color
                    highlight(mainBoard, expected_row, expected_column, GREEN)



                    # highlight all expect this, make it red
                    # neh, not now - later RED
                    # highlight(mainBoard, expected_row, expected_column, RED)
                    # for i in range(3):
                    #     for j in range(3):
                    #         if winner_records[i][j][0]['winner'] is None:
                    #             highlight(mainBoard, i, j, GREEN)
                    #         else:
                    #             dehighlight(mainBoard, i, j)
                    #
                    # expected_row = 'any'
                    # expected_column = 'any'

                # else:
                #     # highlight needed and dehighlight all
                #     highlight(mainBoard, expected_row, expected_column, GREEN)
                #     for i in range(3):
                #         for j in range(3):
                #             if i==expected_row and j==expected_column:
                #                 highlight(mainBoard, i, j, GREEN)
                #             else:
                #                 dehighlight(mainBoard, i, j)
                #     # just redundant checks
                #     expected_row = i
                #     expected_column = j

                pygame.time.wait(500)
                pygame.display.update()
                moved = True

        # If box is not already used, & mouse if clicked just now, move forward
        # WORK REQUIRED here
        # If Inside the board, move forward, else ignore
        # if boxx != None and boxy != None:
        #
        #     # If box is not already used, & mouse if clicked just now, move forward
        #     if not usedBoxes[boxx][boxy] and mouseClicked and playerTurnDone is False:
        #         # DRAW X
        #         markBoxX(boxx, boxy, mainFont)
        #         # Play sound
        #         BEEP1.play()
        #
        #         # set true to used Boxes
        #         usedBoxes[boxx][boxy] = True
        #         # Mark mainboard
        #         mainBoard[boxx][boxy] = XMARK
        #         # Player turn done
        #         playerTurnDone = True
        #
        #         # Update display - early update
        #         # Needs update, or the last iteration isn't displayed.
        #         # Further, to solve this issue, we could extend one iteration,
        #         # But this approach is also cool, so good
        #         pygame.display.update()
        #
        #     # If computer turn, play the move
        #     elif playerTurnDone == True:
        #         # a little delay - time pause for 500 ms
        #         pygame.time.wait(500)
        #
        #
        #         # derive the boxes to be marked with AI
        #         boxx, boxy = computerTurnWithAI(usedBoxes, mainBoard)
        #         # AI processed.
        #
        #         # mark box, play sound
        #         markBoxO(boxx, boxy, mainFont)
        #         BEEP2.play()
        #         # update tables
        #         usedBoxes[boxx][boxy] = True
        #         mainBoard[boxx][boxy] = OMARK
        #         # next is player turn
        #         playerTurnDone = False
        #         pygame.display.update()

        # Check if anyone won the game, after the previous move

        # return a, b, c as three consecutive boxes which helped won
        # a= (box_row1, box_column1) , similarly all 3
        # a, b, c are tuples


        if moved is True:

            # if winner_records[expected_row][expected_column][0]['winner'] is not None:
            #     expected_row = 'any'
            #     expected_column = 'any'


            if winner_records[row][column][0]['winner'] is None:
                winner, b1, b2, b3 = smallGameWon(mainBoard, row, column, box_row, box_column)

            else:
                winner = winner_records[row][column][0]['winner']
                b1 = winner_records[row][column][0]['winner_tuple'][0]
                b2 = winner_records[row][column][0]['winner_tuple'][1]
                b3 = winner_records[row][column][0]['winner_tuple'][2]

            # If player won, highlight the boxes, play sound, reset board for next turn
            # print(winner, row, column, b1, b2, b3)
            # Returned when no more space left
            if winner is 'tie':
                tieScore += 1
                winner_records[row][column][0]['winner'] = 'tie'
                winner_records[row][column][0]['winner_tuple'] = (b1, b2, b3)

            elif winner is 'player':

                playerScore += 1
                pygame.time.wait(500)
                highlightWin(mainBoard, row, column, b1, b2, b3)
                BEEP3.play()
                winner_records[row][column][0]['winner'] = 'player'
                winner_records[row][column][0]['winner_tuple'] = (b1, b2, b3)
                pygame.display.update()

            elif winner is 'computer':
                computerScore += 1
                pygame.time.wait(500)
                highlightWin(mainBoard, row, column, b1, b2, b3)
                BEEP3.play()
                winner_records[row][column][0]['winner'] = 'player'
                winner_records[row][column][0]['winner_tuple'] = (b1, b2, b3)
                pygame.display.update()

                # No reset required in our case.
                # mainBoard, playerTurnDone, playerWins, computerWins = boardReset(mainBoard, playerTurnDone, playerWins, computerWins)
                # DISPLAYSURFACE.fill(BGCOLOR)
                # drawLines()

        # will add this
        # maintain a WINNERMATRIX for big board
        # winner = gameWon(mainBoard)


        # else:
        #     if gameOver(mainBoard):
        #         tieScore += 1
        #         mainBoard, playerTurnDone, playerWins, computerWins = boardReset(mainBoard,
        #                                                                          playerTurnDone, playerWins,
        #                                                                          computerWins)
        #         DISPLAYSURFACE.fill(BGCOLOR)
        #         drawLines()

        # Time to END THE GAME
        # if tieScore >= 1:
        #     DISPLAYSURFACE.fill(BGCOLOR)
        #     pygame.display.update()
        #     pygame.time.wait(1000)
        #     # end game credits
        #     warGameEnding(smallFont, COMPUTERVOICE)
        #     pygame.display.update()
        #
        #     # RESET BOARD
        #     mainBoard, playerTurnDone, playerWins, computerWins = boardReset(mainBoard,
        #                                                                      playerTurnDone, playerWins,
        #                                                                      computerWins)
        #     tieScore = 0
        #     playerScore = 0
        #     computerScore = 0
        #     DISPLAYSURFACE.fill(BGCOLOR)
        #     drawLines()

        # score board
        drawScoreBoard(smallFont, playerScore, computerScore, tieScore)

        # Render the updated graphics on screen
        pygame.display.update()

        # Tick the CLOCK
        FPSCLOCK.tick(FPS)


###### Functions to set up the board  #########

'''
@objective : draw the lines that appear in the main board
@usage     : This function will be used to draw 9 lines
'''

# old draw lines
'''
def drawLines():
    # works fine. But we need more sophisticated graphics.
    #:return:
    
    left = XMARGIN
    top = YMARGIN

    ########HORIZONTAL LINES ##########
    # Length of horizontal line
    width = (BOXSIZE + GAPSIZE) * BOARDWIDTH
    # height of line
    height = GAPSIZE

    # DRAW 8 lines
    for line_no in range(1, BOARDSIZE):
        #  horizontal rectangle needs to be drawn from top
        horizRect1 = pygame.Rect(left, top + line_no*(BOXSIZE + GAPSIZE), width, height)
        pygame.draw.rect(DISPLAYSURFACE, GREEN, horizRect1)


    #######VERTICAL LINES########

    # swap because, they both are opposite for horizontal and vertical lines
    width, height = height, width

    # DRAW 8 lines
    for line_no in range(1, BOARDSIZE):
        #  horizontal rectangle needs to be drawn from top
        horizRect1 = pygame.Rect(left + line_no*(BOXSIZE + GAPSIZE), top, width, height)
        pygame.draw.rect(DISPLAYSURFACE, WHITE, horizRect1)
'''


# experimental
# Does not interfere with new data structure
def drawLines():
    '''
    Works fine. But we need more sophisticated graphics.
    :return:
    '''
    BIGBOXSIZE = (BOXSIZE + GAPSIZE) * BOARDWIDTH
    BIGBOARDSIZE = BOARDSIZE // 3
    left = XMARGIN
    top = YMARGIN

    ########HORIZONTAL LINES ##########
    # Length of horizontal line
    width = (BOXSIZE + GAPSIZE) * BOARDWIDTH
    # height of line
    height = GAPSIZE

    # DRAW 3 lines of BIG BOARD
    for line_no in range(3, BOARDSIZE, 3):
        #  horizontal rectangle needs to be drawn from top
        horizRect1 = pygame.Rect(left, top + line_no * (BOXSIZE + GAPSIZE), width, height)
        pygame.draw.rect(DISPLAYSURFACE, GREEN, horizRect1, 5)

    # DRAW 8 lines
    # for boundaries - change to range(0, BOARDSIZE+1)
    for line_no in range(0, BOARDSIZE + 1):
        #  horizontal rectangle needs to be drawn from top
        horizRect1 = pygame.Rect(left, top + line_no * (BOXSIZE + GAPSIZE), width, height)
        pygame.draw.rect(DISPLAYSURFACE, WHITE, horizRect1)

    #######VERTICAL LINES########

    # swap because, they both are opposite for horizontal and vertical lines
    width, height = height, width

    # DRAW 3 lines of BIG BOARD
    for line_no in range(3, BOARDSIZE, 3):
        #  horizontal rectangle needs to be drawn from top
        horizRect1 = pygame.Rect(left + line_no * (BOXSIZE + GAPSIZE), top, width, height)
        pygame.draw.rect(DISPLAYSURFACE, GREEN, horizRect1, 5)

    # DRAW 8 lines
    for line_no in range(0, BOARDSIZE + 1):
        #  horizontal rectangle needs to be drawn from top
        horizRect1 = pygame.Rect(left + line_no * (BOXSIZE + GAPSIZE), top, width, height)
        pygame.draw.rect(DISPLAYSURFACE, WHITE, horizRect1)


'''
@Objective : converts each box in the Board to FALSE
@Approach  : each each element of row, make all the boxes in its column FALSE
@Note : The Box is list of lists. 
For each Row one sublist, one sublist represents columns
'''


def makeEachBoxFalse(val):
    """
    Time to modify you my friend

    Initially it was this,
    [
        [False, False, False],
        [False, False, False],
        [False, False, False]
    ]

    Not wanna make this ->>>
    [
    [ False, False, False, False, False, False, False, False, False ],
    [ False, False, False, False, False, False, False, False, False ],
    [ False, False, False, False, False, False, False, False, False ],
    [ False, False, False, False, False, False, False, False, False ],
    [ False, False, False, False, False, False, False, False, False ],
    [ False, False, False, False, False, False, False, False, False ],
    [ False, False, False, False, False, False, False, False, False ],
    [ False, False, False, False, False, False, False, False, False ],
    [ False, False, False, False, False, False, False, False, False ]
    ]

    But this - data structure variable


    :param val:
    :return:
    """

    # convert it to looping structure
    data_structure_required = [
        [
            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ],  # small box 0

            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ],  # small box 1

            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ]  # small box 2
        ],  # big row zero

        [
            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ],  # small box 0

            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ],  # small box 1

            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ]  # small box 2
        ],  # big row one

        [
            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ],  # small box 0

            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ],  # small box 1

            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ]  # small box 2
        ]  # big row two
    ]

    winner_records = [
        [
            [
                {
                    'winner': None,
                    'winner_tuple': None

                },
            ],  # small box 0

            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ],  # small box 1

            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ]  # small box 2
        ],  # big row zero

        [
            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ],  # small box 0

            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ],  # small box 1

            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ]  # small box 2
        ],  # big row one

        [
            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ],  # small box 0

            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ],  # small box 1

            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ]  # small box 2
        ]  # big row two
    ]

    usedBoxes = []
    usedBoxes = copy.deepcopy(data_structure_required)
    '''for i in range(BOARDWIDTH):
        # append a list
        usedBoxes.append([val] * BOARDHEIGHT)
    # Return a list of lists
    '''
    return usedBoxes, winner_records


def smallGameWon(mainBoard, row, column, box_row, box_column):
    '''

    :param mainBoard:
    :param row:
    :param column:
    :param box_row:
    :param box_column:
    :return:
    '''

    checkMark = XMARK
    possible_cases = [
        # rows
        ((0, 0), (0, 1), (0, 2)),
        ((1, 0), (1, 1), (1, 2)),
        ((2, 0), (2, 1), (2, 2)),

        # columns
        ((0, 0), (1, 0), (2, 0)),
        ((0, 1), (1, 1), (2, 1)),
        ((0, 2), (1, 2), (2, 2)),

        # diagnoals
        ((0, 0), (1, 1), (2, 2)),
        ((0, 2), (1, 1), (2, 0))

    ]

    winner = 'tie'
    box1 = ()
    box2 = ()
    box3 = ()

    for ((i1, j1), (i2, j2), (i3, j3)) in possible_cases:
        if mainBoard[row][column][i1][j1] == mainBoard[row][column][i2][j2] == mainBoard[row][column][i3][j3]:

            if mainBoard[row][column][i1][j1] == 'X':
                winner = 'player'
                box1 = (i1, j1)
                box2 = (i2, j2)
                box3 = (i3, j3)
                return winner, box1, box2, box3

            elif mainBoard[row][column][i1][j1] == 'O':
                winner = 'computer'
                box1 = (i1, j1)
                box2 = (i2, j2)
                box3 = (i3, j3)
                return winner, box1, box2, box3

    # if atleast one space is left, no one is winner
    for i in range(0, 3):
        for j in range(0, 3):
            if mainBoard[row][column][i][j] is False:
                winner = None
                return winner, box1, box2, box3

    # else, tie
    return winner, box1, box2, box3


    # If no one won, and no space is left, it is a TIE, as set as default


    # winning tiny boxes coordinates
    # Player win by consecutive X mark
    # if ((mainBoard[0][0] == mainBoard[1][0] == mainBoard[2][0] == XMARK) or
    #     (mainBoard[0][1] == mainBoard[1][1] == mainBoard[2][1] == XMARK) or
    #     (mainBoard[0][2] == mainBoard[1][2] == mainBoard[2][2] == XMARK) or
    #     (mainBoard[0][0] == mainBoard[0][1] == mainBoard[0][2] == XMARK) or
    #     (mainBoard[1][0] == mainBoard[1][1] == mainBoard[1][2] == XMARK) or
    #     (mainBoard[2][0] == mainBoard[2][1] == mainBoard[2][2] == XMARK) or
    #     (mainBoard[0][0] == mainBoard[1][1] == mainBoard[2][2] == XMARK) or
    #     (mainBoard[0][2] == mainBoard[1][1] == mainBoard[2][0] == XMARK)):
    #
    #     playerWins = True
    #     computerWins = False
    #     return playerWins, computerWins
    #
    # # Computer win by consecutive O mark
    # elif ((mainBoard[0][0] == mainBoard[1][0] == mainBoard[2][0] == OMARK) or
    #       (mainBoard[0][1] == mainBoard[1][1] == mainBoard[2][1] == OMARK) or
    #       (mainBoard[0][2] == mainBoard[1][2] == mainBoard[2][2] == OMARK) or
    #       (mainBoard[0][0] == mainBoard[0][1] == mainBoard[0][2] == OMARK) or
    #       (mainBoard[1][0] == mainBoard[1][1] == mainBoard[1][2] == OMARK) or
    #       (mainBoard[2][0] == mainBoard[2][1] == mainBoard[2][2] == OMARK) or
    #       (mainBoard[0][0] == mainBoard[1][1] == mainBoard[2][2] == OMARK) or
    #       (mainBoard[0][2] == mainBoard[1][1] == mainBoard[2][0] == OMARK)):
    #
    #     playerWins = False
    #     computerWins = True
    #     return playerWins, computerWins
    #
    # # No one won
    # else:
    # playerWins = False
    # computerWins = False

    # more valid things are
    # return 'player'
    # return 'computer'
    # return None


    # b1 = ()
    # b2 = ()
    # b3 = ()
    # return winner, b1, b2, b3


def dehighlight(mainBoard, row, column):
    '''
    De highlight stuff
    :param mainBoard:
    :param row:
    :param column:
    :return:
    '''
    # BOX decides top and left  and width and height
    top = YMARGIN + (3 * row) * (BOXSIZE + GAPSIZE)
    left = XMARGIN + (3 * column) * (BOXSIZE + GAPSIZE)

    width = 3 * (BOXSIZE + GAPSIZE)
    height = 3 * (BOXSIZE + GAPSIZE)

    highlight_box_color = (140, 255, 26)
    horizRect1 = pygame.Rect(left, top, width, height)

    # highlight
    pygame.draw.rect(DISPLAYSURFACE, BLACK, horizRect1)
    # redraw lines
    drawLines()
    # redraw symbols
    redraw(mainBoard, row, column)
    # for now, come back after its safe
    if winner_records[row][column][0]['winner'] is not None:
        highlightWin(mainBoard, row, column,
                     winner_records[row][column][0]['winner_tuple'][0],
                     winner_records[row][column][0]['winner_tuple'][1],
                     winner_records[row][column][0]['winner_tuple'][2])


'''
Re draw symbols in that box after high lighting
'''


def highlight(mainBoard, row, column, color):
    '''

    :param color:
    :param mainBoard: the entire board, updates will happen here
    :param box_no: which box to highlight
    :return:
    '''
    # row = box_no // 3
    # column = box_no % 3

    # highlight_small_box = board[row][column]

    highlight_box_color = color

    # BOX decides top and left  and width and height
    top = YMARGIN + (3 * row) * (BOXSIZE + GAPSIZE)
    left = XMARGIN + (3 * column) * (BOXSIZE + GAPSIZE)

    width = 3 * (BOXSIZE + GAPSIZE)
    height = 3 * (BOXSIZE + GAPSIZE)

    highlight_box_color = (140, 255, 26)
    horizRect1 = pygame.Rect(left, top, width, height)

    # highlight
    pygame.draw.rect(DISPLAYSURFACE, highlight_box_color, horizRect1, 0)
    # redraw lines
    drawLines()
    # redraw symbols
    redraw(mainBoard, row, column)
    # for now, come back after its safe
    if winner_records[row][column][0]['winner'] is not None:
        highlightWin(mainBoard, row, column,
                     winner_records[row][column][0]['winner_tuple'][0],
                     winner_records[row][column][0]['winner_tuple'][1],
                     winner_records[row][column][0]['winner_tuple'][2])


def redraw(board, row, column):
    '''
    AIM: To redraw lost symbols
    :param board:
    :param row:
    :param column:
    :return:
    '''
    mainFont = pygame.font.SysFont('Helvetica', MARKSIZE)
    for boxx in range(3):
        for boxy in range(3):
            mark = board[row][column][boxx][boxy]
            if mark is not False:
                markBox(row, column, boxx, boxy, mainFont, mark)
                # done


def drawScoreBoard(smallFont, playerScore, computerScore, tieScore):
    scoreBoard = smallFont.render(
        'Player: ' + str(playerScore) + '     ' + 'Computer: ' + str(computerScore) + '      ' + 'Tie: ' + str(
            tieScore), True, COMBLUE, BGCOLOR)
    scoreBoardRect = scoreBoard.get_rect()
    scoreBoardRect.x = 0
    scoreBoardRect.y = 0
    DISPLAYSURFACE.blit(scoreBoard, scoreBoardRect)


##### Coordinate Functions #####

'''
@function name : getBoxAtPixel
@purpose : Return the box where pixel(x,y) lie
@approach : 
Iterate over each possible SMALL BOX, derive its top left coordinates

>>> AMAZING FUNCTION - core of it all
'''


# Needs to be modified with respect to new data structure
# But does not interfere
def getBoxAtPixel(x, y):
    for row in range(BIGBOXSIZE):
        for column in range(BIGBOXSIZE):
            for box_row in range(BIGBOXSIZE):
                for box_column in range(BIGBOXSIZE):

                    # left, top = leftTopCoordsOfBox(row, column, box_row, box_column)

                    # Reach BIG BOX + reach specific box inside it
                    top = (YMARGIN + (3 * row) * (BOXSIZE + GAPSIZE)) + (box_row * (BOXSIZE + GAPSIZE))
                    left = (XMARGIN + (3 * column) * (BOXSIZE + GAPSIZE)) + (box_column * (BOXSIZE + GAPSIZE))

                    boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
                    if boxRect.collidepoint(x, y):
                        return (row, column, box_row, box_column)

    return (None, None, None, None)
    #
    # for boxx in range(BOARDWIDTH):
    #     for boxy in range(BOARDHEIGHT):
    #         left, top = leftTopCoordsOfBox(boxx, boxy)
    #         # Draw a rectangle from top left coordinate of the box
    #         # If made box and mouse pixel intersect, we found it right
    #         boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
    #         if boxRect.collidepoint(x, y):
    #             return (boxx, boxy)
    # return (None, None)


'''
@:function : leftTopCoordsOfBox
@:returns : The top left coordinates of a Small BOX
@:approach : absolute pixel = X Margin + (box size + width) * box number

'''

'''
def leftTopCoordsOfBox(boxx, boxy):

    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return left, top
'''

'''
@:function : centerxAndCenteryOfBox
@:returns : center coordinates of a Small BOX
@:approach : find the top left, then add half the box from both sides
Minor note : a little extra on y side, because i want the X/O a lil down
'''


def centerxAndCenteryOfBox(boxx, boxy):
    centerx = boxx * (BOXSIZE + GAPSIZE) + XMARGIN + (BOXSIZE / 2)
    centery = boxy * (BOXSIZE + GAPSIZE) + YMARGIN + (BOXSIZE / 2) + 5
    return centerx, centery


##### Functions dealing with computer and player moves ######

'''
Functions to mark X and O in the main board
approach : 
1. render the mark surface from X
2. Obtain its rectangle
3. relocate the rectangle to correct small box
4. BLIZ the original mark over this relocated rectangle
'''


def markBox(row, column, box_row, box_column, mainFont, MARK):
    '''
    This creates a new Surface with the specified text rendered on it. 
    pygame provides no way to directly draw text on an existing Surface:
    instead you must use Font.render() to create an image (Surface) of the text, 
    then blit this image onto another Surface.
    '''
    # Use Main Font to - render Xmark on a new surface
    mark = mainFont.render(MARK, True, WHITE)
    '''
    Surfaces don't have a position, so you have to store the blit position in the rect. 
    When you call the get_rect method of a pygame.Surface, Pygame creates a new rect
    with the size of the surface with coordinates (x,y)=(0,0). 
    '''
    # Obtain the rectangle object of surface.
    markRect = mark.get_rect()

    # find center of small box
    # Reach BIG BOX + reach specific box inside it
    top = (YMARGIN + (3 * row) * (BOXSIZE + GAPSIZE)) + (box_row * (BOXSIZE + GAPSIZE))
    left = (XMARGIN + (3 * column) * (BOXSIZE + GAPSIZE)) + (box_column * (BOXSIZE + GAPSIZE))

    # then go to center of box
    centerx = left + (BOXSIZE + GAPSIZE) // 2
    centery = top + (BOXSIZE + GAPSIZE) // 2

    # centerx, centery = centerxAndCenteryOfBox(boxx, boxy)

    # update the center = to center of the current box, so that TEXT appears inside box
    # Interesting Note : pygame re calculates the top and left automatically, when i change the center
    markRect.centerx = centerx
    markRect.centery = centery

    # BLIT(source,destination)
    DISPLAYSURFACE.blit(mark, markRect)


'''
Function : markBoxO
Approach : Exactly same as markBoxX
'''

'''
def markBoxO(boxx, boxy, mainFont):
    centerx, centery = centerxAndCenteryOfBox(boxx, boxy)
    mark = mainFont.render(OMARK, True, WHITE)
    markRect = mark.get_rect()
    markRect.centerx = centerx
    markRect.centery = centery
    DISPLAYSURFACE.blit(mark, markRect)
'''

'''
@:Function : computerTurnWithAI
@: Objective : The smart AI
@: approach : 
1. check if AI can win with this move
2. check if Player can win with his next move, block that move
- IF BOTH SAFE, PROCEED -
3. Occupy center
4. Check if there is a fork ( a probable path leading to 2 winning situations )
5. occupy corners
6. occupy sides

'''


def computerTurnWithAI(usedBoxes, mainBoard):
    ## Step 1: Check to see if there is a winning move ##
    '''

    :param usedBoxes: a list of currently used boxes
    :param mainBoard: The main board
    :return: the AI move
    :approach: For each un-used box, play the AI move(O), and see if we can win
    '''
    pass

    # for boxx in range(BOARDWIDTH):
    #     for boxy in range(BOARDHEIGHT):
    #         mainBoardCopy = copy.deepcopy(mainBoard)
    #         if usedBoxes[boxx][boxy] == False:
    #             mainBoardCopy[boxx][boxy] = OMARK
    #             playerWins, computerWins = gameWon(mainBoardCopy)
    #
    #             if computerWins == True:
    #                 return boxx, boxy
    #
    #
    #
    #
    # ## Step 2: Check to see if there is a potential win that needs to be blocked ##
    # '''
    # :approach: For each un-used box, play the player move (X), and see if we can win
    # '''
    #
    # for boxx in range(BOARDWIDTH):
    #     for boxy in range(BOARDWIDTH):
    #         mainBoardCopy = copy.deepcopy(mainBoard)
    #         if usedBoxes[boxx][boxy] == False:
    #             mainBoardCopy[boxx][boxy] = XMARK
    #             playerWins, computerWins = gameWon(mainBoardCopy)
    #
    #             if playerWins == True:
    #                 return boxx, boxy
    #
    #
    # ## Step 3: Check if the center is empty ##
    # # center is located at 1,1
    # mainBoardCopy = copy.deepcopy(mainBoard)
    #
    # if mainBoardCopy[1][1] == False:
    #     return 1, 1
    #
    #
    # ## Step 4: Prevent a potential fork ##
    # '''
    # A fork is a potential move  resulting in two winning situations
    # 2 distance fork
    # 1 distance fork
    # '''
    #
    # if ((mainBoardCopy[0][0] == mainBoardCopy[2][2] == XMARK) or
    #     (mainBoardCopy[0][2] == mainBoardCopy[2][0] == XMARK)):
    #     if mainBoardCopy[1][2] == False:
    #         return 1, 2
    #
    #
    # if mainBoard[1][0] == XMARK:
    #     if mainBoard[0][1] == XMARK:
    #         if mainBoard[0][0] == False:
    #             return 0, 0
    #
    # if mainBoard[1][0] == XMARK:
    #     if mainBoard[2][1] == XMARK:
    #         if mainBoard[2][0] == False:
    #             return 2, 0
    #
    # if mainBoard[0][1] == XMARK:
    #     if mainBoard[1][2] == XMARK:
    #         if mainBoard[0][2] == False:
    #             return 0, 2
    #
    # if mainBoard[2][1] == XMARK:
    #     if mainBoard[1][2] == XMARK:
    #         if mainBoard[2][2] == False:
    #             return 2, 2
    #
    #
    # if (mainBoard[0][2] == XMARK):
    #     if (mainBoard[2][1] == XMARK):
    #         if mainBoard[1][2] == False:
    #             return 1, 2
    #     elif (mainBoard[1][0]):
    #         if mainBoard[0][1] == False:
    #             return 0, 1
    #
    # if mainBoard[2][2] == XMARK:
    #     if mainBoard[0][1] == XMARK:
    #         if mainBoard[1][2] == False:
    #             return 1, 2
    #     elif mainBoard[1][0] == XMARK:
    #         if mainBoard[2][1] == False:
    #             return 2, 1
    #
    # if mainBoard[0][0] == XMARK:
    #     if mainBoard[2][1] == XMARK:
    #         if mainBoard[1][0] == False:
    #             return 1, 0
    #     elif mainBoard[1][2] == XMARK:
    #         if mainBoard[0][1] == False:
    #             return 0, 1
    #
    # if mainBoard[2][0] == XMARK:
    #     if mainBoard[1][2] == XMARK:
    #         if mainBoard[2][1] == False:
    #             return 2, 1
    #     elif mainBoard[0][1] == XMARK:
    #         if mainBoard[1][0] == False:
    #             return 1, 0
    #
    #
    #
    #
    #
    #
    #
    #
    # # if any corener is empty , grab it
    #
    # ## Step 5: Check if a corner is open ##
    #
    # xlist = [0, 2, 0, 2]
    # ylist = [0, 2, 0, 2]
    #
    # random.shuffle(xlist)
    # random.shuffle(ylist)
    #
    # for x in xlist:
    #     for y in ylist:
    #         if mainBoardCopy[x][y] == False:
    #             return x, y
    #
    #
    #
    #
    # # any side which is empty
    #
    # ## Step 6: Check if a side is open ##
    #
    # for boxx in range(BOARDWIDTH):
    #     for boxy in range(BOARDHEIGHT):
    #         if mainBoardCopy[boxx][boxy] == False:
    #             return boxx, boxy
    #
    #
    #


##### Functions dealing with an end of game ########

'''
Function : gameWon()
Purpose: Checks all the 8 scenarios of game winning and return the winner, if any
'''


def gameWon(mainBoard):
    # Player win by consecutive X mark
    # if ((mainBoard[0][0] == mainBoard[1][0] == mainBoard[2][0] == XMARK) or
    #     (mainBoard[0][1] == mainBoard[1][1] == mainBoard[2][1] == XMARK) or
    #     (mainBoard[0][2] == mainBoard[1][2] == mainBoard[2][2] == XMARK) or
    #     (mainBoard[0][0] == mainBoard[0][1] == mainBoard[0][2] == XMARK) or
    #     (mainBoard[1][0] == mainBoard[1][1] == mainBoard[1][2] == XMARK) or
    #     (mainBoard[2][0] == mainBoard[2][1] == mainBoard[2][2] == XMARK) or
    #     (mainBoard[0][0] == mainBoard[1][1] == mainBoard[2][2] == XMARK) or
    #     (mainBoard[0][2] == mainBoard[1][1] == mainBoard[2][0] == XMARK)):
    #
    #     playerWins = True
    #     computerWins = False
    #     return playerWins, computerWins
    #
    # # Computer win by consecutive O mark
    # elif ((mainBoard[0][0] == mainBoard[1][0] == mainBoard[2][0] == OMARK) or
    #       (mainBoard[0][1] == mainBoard[1][1] == mainBoard[2][1] == OMARK) or
    #       (mainBoard[0][2] == mainBoard[1][2] == mainBoard[2][2] == OMARK) or
    #       (mainBoard[0][0] == mainBoard[0][1] == mainBoard[0][2] == OMARK) or
    #       (mainBoard[1][0] == mainBoard[1][1] == mainBoard[1][2] == OMARK) or
    #       (mainBoard[2][0] == mainBoard[2][1] == mainBoard[2][2] == OMARK) or
    #       (mainBoard[0][0] == mainBoard[1][1] == mainBoard[2][2] == OMARK) or
    #       (mainBoard[0][2] == mainBoard[1][1] == mainBoard[2][0] == OMARK)):
    #
    #     playerWins = False
    #     computerWins = True
    #     return playerWins, computerWins
    #
    # # No one won
    # else:
    # playerWins = False
    # computerWins = False

    # more valid things are
    # return 'player'
    # return 'computer'
    return None


'''
@:Function : gameOver
@:purpose: checks is the game is over - no space left to move
@:approach : If any one the boxes from used boxes is false, it means its not has been used.
Means, Board has still space left, return false to game over

If no space left, it is a game over
'''


def gameOver(usedBoxes, mainBoard):
    for row in range(BIGBOXSIZE):
        for column in range(BIGBOXSIZE):
            for box_row in range(BIGBOXSIZE):
                for box_column in range(BIGBOXSIZE):
                    if mainBoard[row][column][box_row][box_column] is False:
                        return False

    return True

    # for boxx in range(BOARDWIDTH):
    #     for boxy in range(BOARDHEIGHT):
    #         if usedBoxes[boxx][boxy] == False:
    #             return False
    #
    # else:
    #     return True
    # return False


'''
Resets the game
'''


def boardReset(mainBoard, playerTurnDone, playerWins, computerWins):
    pygame.time.wait(1000)
    mainBoard, winner_records = makeEachBoxFalse(False)
    playerTurnDone = False
    playerWins = computerWins = False


def highlightWin(mainBoard, row, column, b1, b2, b3):
    '''

    :param mainBoard: Highlights the winning situation
    :return:

    #Note: Can be highly optimised if i pass around the winning boxes
    '''

    # The three boxes needed are b1,b2,b3

    # startPos = (XMARGIN + (BOXSIZE / 2), YMARGIN + (BOXSIZE / 2))
    # endPos = (XMARGIN + (BOXSIZE / 2), YMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE / 2))

    # find center of small box
    # calculate start postion of line

    box_row = b1[0]
    box_column = b1[1]
    # Reach BIG BOX + reach specific box inside it + middle of it
    left = (XMARGIN + (3 * column) * (BOXSIZE + GAPSIZE)) + \
           (box_column * (BOXSIZE + GAPSIZE)) + \
           ((BOXSIZE) // 2)

    top = (YMARGIN + (3 * row) * (BOXSIZE + GAPSIZE)) + \
          (box_row * (BOXSIZE + GAPSIZE)) + \
          ((BOXSIZE) // 2)

    startPos = (left, top)

    box_row = b3[0]
    box_column = b3[1]
    # Reach BIG BOX + reach specific box inside it + middle of it
    left = (XMARGIN + (3 * column) * (BOXSIZE + GAPSIZE)) + \
           (box_column * (BOXSIZE + GAPSIZE)) + \
           ((BOXSIZE) // 2)
    top = (YMARGIN + (3 * row) * (BOXSIZE + GAPSIZE)) + \
          (box_row * (BOXSIZE + GAPSIZE)) + \
          ((BOXSIZE) // 2)

    endPos = (left, top)

    # print(startPos)
    # print(endPos)
    pygame.draw.line(DISPLAYSURFACE, LINECOLOR, startPos, endPos, 5)

    # return startPos, endPos

    # In the small box mainBoard[row][column], boxes b1, b2, b3 needs to be highlighted

    # scenario1 = 1
    # scenario2 = 2
    # scenario3 = 3
    # scenario4 = 4
    # scenario5 = 5
    # scenario6 = 6
    # scenario7 = 7
    # scenario8 = 8
    #
    # if mainBoard[0][0] == mainBoard[1][0] == mainBoard[2][0]:
    #     highLightBoxes(mainBoard, scenario1)
    #
    #
    # elif mainBoard[0][1] == mainBoard[1][1] == mainBoard[2][1]:
    #     highLightBoxes(mainBoard, scenario2)
    #
    #
    # elif mainBoard[0][2] == mainBoard[1][2] == mainBoard[2][2]:
    #     highLightBoxes(mainBoard, scenario3)
    #
    #
    # elif mainBoard[0][0] == mainBoard[0][1] == mainBoard[0][2]:
    #     highLightBoxes(mainBoard, scenario4)
    #
    #
    # elif mainBoard[1][0] == mainBoard[1][1] == mainBoard[1][2]:
    #     highLightBoxes(mainBoard, scenario5)
    #
    #
    # elif mainBoard[2][0] == mainBoard[2][1] == mainBoard[2][2]:
    #     highLightBoxes(mainBoard, scenario6)
    #
    #
    # elif mainBoard[0][0] == mainBoard[1][1] == mainBoard[2][2]:
    #     highLightBoxes(mainBoard, scenario7)
    #
    #
    # elif mainBoard[2][0] == mainBoard[1][1] == mainBoard[0][2]:
    #     highLightBoxes(mainBoard, scenario8)


'''
@:Objective : Draws a line after someone won
@approach :
Handles each win case separately with magic numbers

NOTE : Remove magic numbers
'''


def highLightBoxes(mainBoard, scenario):
    if scenario == 1:
        startPos = (XMARGIN + (BOXSIZE / 2), YMARGIN + (BOXSIZE / 2))
        endPos = (XMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE / 2), YMARGIN + (BOXSIZE / 2))

        pygame.draw.line(DISPLAYSURFACE, LINECOLOR, startPos, endPos, 10)

    elif scenario == 2:
        startPos = (XMARGIN + (BOXSIZE / 2), YMARGIN + BOXSIZE + GAPSIZE + (BOXSIZE / 2))
        endPos = (
            XMARGIN + (BOXSIZE / 2) + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE,
            YMARGIN + BOXSIZE + GAPSIZE + (BOXSIZE / 2))

        pygame.draw.line(DISPLAYSURFACE, LINECOLOR, startPos, endPos, 10)

    elif scenario == 3:
        startPos = (XMARGIN + (BOXSIZE / 2), YMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE / 2))
        endPos = (XMARGIN + (BOXSIZE / 2) + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE,
                  YMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE / 2))

        pygame.draw.line(DISPLAYSURFACE, LINECOLOR, startPos, endPos, 10)

    elif scenario == 4:
        startPos = (XMARGIN + (BOXSIZE / 2), YMARGIN + (BOXSIZE / 2))
        endPos = (XMARGIN + (BOXSIZE / 2), YMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE / 2))

        pygame.draw.line(DISPLAYSURFACE, LINECOLOR, startPos, endPos, 10)

    elif scenario == 5:
        startPos = (XMARGIN + BOXSIZE + GAPSIZE + (BOXSIZE / 2), YMARGIN + (BOXSIZE / 2))
        endPos = (
            XMARGIN + BOXSIZE + GAPSIZE + (BOXSIZE / 2),
            YMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE / 2))

        pygame.draw.line(DISPLAYSURFACE, LINECOLOR, startPos, endPos, 10)

    elif scenario == 6:
        startPos = (XMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE / 2), YMARGIN + (BOXSIZE / 2))
        endPos = (XMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE / 2),
                  YMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE / 2))

        pygame.draw.line(DISPLAYSURFACE, LINECOLOR, startPos, endPos, 10)

    elif scenario == 7:
        startPos = (XMARGIN + (BOXSIZE / 2), YMARGIN + (BOXSIZE / 2))
        endPos = (XMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE / 2),
                  YMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE / 2))

        pygame.draw.line(DISPLAYSURFACE, LINECOLOR, startPos, endPos, 10)

    elif scenario == 8:
        startPos = (XMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE / 2), YMARGIN + (BOXSIZE / 2))
        endPos = (XMARGIN + (BOXSIZE / 2), YMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE / 2))

        pygame.draw.line(DISPLAYSURFACE, LINECOLOR, startPos, endPos, 10)


def warGameEnding(smallFont, COMPUTERVOICE):
    COMPUTERVOICE.play()
    surfRect = DISPLAYSURFACE.get_rect()
    DISPLAYSURFACE.fill(BGCOLOR)

    # Render text
    computerMessage1 = smallFont.render('A strange game...', True, COMBLUE, BGCOLOR)
    # Shift its rectangle to the position where you want the text
    computerMessage1Rect = computerMessage1.get_rect()
    computerMessage1Rect.x = XMARGIN / 3
    computerMessage1Rect.y = YMARGIN * 2

    # uncover the words - draw computerMessage1 inside rectangle computerMessage1Rect
    uncoverWords(computerMessage1, computerMessage1Rect)
    pygame.time.wait(1000)

    computerMessage2 = smallFont.render('The only winning move is not to play.', True, COMBLUE, BGCOLOR)
    computerMessage2Rect = computerMessage2.get_rect()
    computerMessage2Rect.x = XMARGIN / 3
    computerMessage2Rect.centery = (YMARGIN * 2) + 50

    uncoverWords(computerMessage2, computerMessage2Rect)
    pygame.time.wait(3000)


def uncoverWords(text, textRect):
    # Copy the rectangle
    textRectCopy = copy.deepcopy(textRect)

    # Un necessary -- made copy because changes made while reveal speed
    blackRect = textRectCopy

    # Text is as wide as rectangle width ( of a rectangle which was originally derived from this text only )
    textLength = textRect.width

    # Revealing speed for text
    revealSpeed = 1

    # steps required to reveal whole text
    for i in range((textLength // revealSpeed) + 1):
        # draw text
        DISPLAYSURFACE.blit(text, textRect)
        # Draw a black rectangle over text
        pygame.draw.rect(DISPLAYSURFACE, BLACK, blackRect)
        pygame.display.update()
        # Move the black triangle slowly away
        blackRect.x += revealSpeed
        blackRect.width -= revealSpeed


if __name__ == '__main__':
    main()
