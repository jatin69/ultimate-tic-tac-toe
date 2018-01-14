import pygame, sys, random, copy
from pygame.locals import *


"""
NEXT GOALs ->>

modify score card 
Manage screens -> commit
bundle up -> commit -> release
see function independencies -> experiment some shit
set game_loop.md as per it
"""


# ALso a possible data structure,, but will need to redefine my entire logic of finding coordinates, maybeee
theBoard = {'top-L': 'O', 'top-M': 'O', 'top-R': 'O',
            'mid-L': 'X', 'mid-M': 'X', 'mid-R': ' ',
            'low-L': ' ', 'low-M': ' ', 'low-R': 'X'}

# TL, TM, TR
# ML, MM, MR
# BL, BM, BR




# CONSTANTS

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


def main(level):
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

    # testing variables
    # playerScore = 3
    # computerScore = 6
    # tieScore = 0

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
    mainBoard, winner_records = initialise_new_game(False)
    # Initially used boxes
    # usedBoxes = makeEachBoxFalse(False)


    # Paint the surface black
    DISPLAYSURFACE.fill(BGCOLOR)

    # Draw all the required lines
    drawLines()

    # The GRAND game loop

    # Player turn : bool variable
    game_turn = 'player'
    expected_row = None
    expected_column = None

    game_done = False

    while True:

        # set mouseClick as False
        mouseClicked = False


        # did the player move
        moved = False
        mousex, mousey = None, None
        row, column, box_row, box_column = (None, None, None, None)

        # Check for events for event queue
        for event in pygame.event.get():

            # For Game exiting
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If mouse is moving, update the location
            # elif event.type == MOUSEMOTION:
            #     mousex, mousey = event.pos

            # If mouse button just came up, it means the button is clicked
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

            if game_done is True:
                mouseClicked = False

        '''
        @:purpose : when mouse is clicked, we need to put X or O at the correct box
        So to obtain the exact box where the mouse is clicked, this function is used.
        @:returns: The box coordinates, where mouse is clicked
        '''
        if mousex is not None and mousey is not None:
            row, column, box_row, box_column = getBoxAtPixel(mousex, mousey)

        # correct here, perfect
        # print(row, column, box_row, box_column)

        # Firstmost turn

        # This code just highlights
        # actual law enforcement must be done

        # mouse is clicked + not first time
        if mouseClicked and expected_column is not None and expected_row is not None \
                and row is not None and column is not None:

            if expected_row == 'any' and expected_column == 'any':
                if winner_records[row][column][0]['winner'] is not None:
                    row = None
                    column = None

            # + row does not match expected
            elif row != expected_row or column != expected_column:
                row = None
                column = None
                pygame.display.update()
                highlight(mainBoard, expected_row, expected_column, GREEN)

            # print(row, column)

        # If Inside the board, move forward, else ignore
        if row is not None and column is not None and box_row is not None and box_column is not None:

            if mainBoard[row][column][box_row][box_column] is False and mouseClicked:

                MARK, BEEP = None, None

                if game_turn == 'player':
                    MARK = XMARK
                    BEEP = BEEP1
                    game_turn = 'computer'

                elif game_turn == 'computer':
                    MARK = OMARK
                    BEEP = BEEP2
                    game_turn = 'player'


                markBox(row, column, box_row, box_column, mainFont, MARK)
                mainBoard[row][column][box_row][box_column] = MARK
                moved = True
                pygame.display.update()
                BEEP.play()
                # Player turn done

                expected_row = box_row
                expected_column = box_column

                # remove green color
                # dehighlight(mainBoard, row, column)
                # In case of any, i gotta dehighlight everything..... focus
                for i in range(3):
                    for j in range(3):
                        dehighlight(mainBoard, i, j)

                pygame.display.update()

                if moved is True:

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
                        # in case of tie, b1 is none >>> handle later

                    elif winner is 'player':
                        playerScore += 1
                        pygame.time.wait(500)
                        highlightWin(mainBoard, row, column, b1, b2, b3)
                        BEEP3.play()
                        winner_records[row][column][0]['winner'] = 'X'
                        winner_records[row][column][0]['winner_tuple'] = (b1, b2, b3)
                        #print(winner_records[row][column][0]['winner_tuple'])
                        pygame.display.update()

                    elif winner is 'computer':
                        computerScore += 1
                        pygame.time.wait(500)
                        highlightWin(mainBoard, row, column, b1, b2, b3)
                        BEEP3.play()
                        winner_records[row][column][0]['winner'] = 'O'
                        winner_records[row][column][0]['winner_tuple'] = (b1, b2, b3)
                        #print(winner_records[row][column][0]['winner_tuple'])
                        pygame.display.update()

                        # No reset required in our case.
                        # mainBoard, playerTurnDone, playerWins, computerWins = boardReset(mainBoard, playerTurnDone, playerWins, computerWins)
                        # DISPLAYSURFACE.fill(BGCOLOR)
                        # drawLines()

                pygame.display.update()
                # highlight(mainBoard, expected_row, expected_column, GREEN)

                if winner_records[expected_row][expected_column][0]['winner'] is not None:
                    expected_row = 'any'
                    expected_column = 'any'

                if expected_row == 'any' and expected_column == 'any':
                    # highlight all valid boxes
                    for i in range(3):
                        for j in range(3):
                            if winner_records[i][j][0]['winner'] is None:
                                highlight(mainBoard, i, j, GREEN)
                            # else:
                            #     dehighlight(mainBoard, i, j)

                else:
                    # just green color
                    highlight(mainBoard, expected_row, expected_column, GREEN)

                pygame.time.wait(500)
                #pygame.display.update()

        drawScoreBoard(smallFont, playerScore, computerScore, tieScore)

        # Render the updated graphics on screen
        pygame.display.update()

        # start here for MAJOR Line

        if level == "easy":
            mega_winner = checkMegaWinEasy(mainBoard, winner_records)

            # // check who wins and alos tue
            if mega_winner is not None:
                drawWinner(smallFont, mega_winner)
                if mega_winner == 'tie':
                    # fill bg black and etc display
                    # tie display on screen
                    game_done = True

                else:
                    for row in range(3):
                        for col in range(3):
                            if winner_records[row][col][0]['winner'] == mega_winner:
                                highlight(mainBoard, row, col, RED)
                            else:
                                dehighlight(mainBoard, row, col)

        elif level == "smart":
            mega_winner, mb1, mb2, mb3 = checkMegaWinHeadOn(mainBoard, winner_records)

            if mega_winner is not None:
                drawWinner(smallFont, mega_winner)
                if mega_winner == 'tie':
                    # fill bg black and etc display
                    # tie display on screen
                    game_done = True
                    # pass
                else:
                    highlightMegaWin(mainBoard, mega_winner, mb1, mb2, mb3)
                    game_done = True

        # Render the updated graphics on screen
        pygame.display.update()

        # Tick the CLOCK
        FPSCLOCK.tick(FPS)


###### Functions to set up the board  #########

"""
:objective: highlight the mega win
"""

def highlightMegaWin(mainBoard, mega_winner, mb1, mb2, mb3):
    """

    :param mainBoard:
    :param mega_winner:
    :param mb1:
    :param mb2:
    :param mb3:
    :return:
    """
    for row in range(3):
        for col in range(3):
            dehighlight(mainBoard, row, col)

    highlight(mainBoard, mb1[0], mb1[1], RED)
    highlight(mainBoard, mb2[0], mb2[1], RED)
    highlight(mainBoard, mb3[0], mb3[1], RED)


def checkMegaWinEasy(mainBoard, winner_records):
    """

    :param mainBoard:
    :param winner_records:
    :return:
    """
    mega_winner = None
    player, computer, tie = 0, 0, 0

    for row in range(3):
        for col in range(3):
            boxStatus = winner_records[row][col][0]['winner']

            if boxStatus is None:
                return mega_winner

            if boxStatus == 'X':
                player += 1
            elif boxStatus == 'O':
                computer += 1
            elif boxStatus == 'tie':
                tie += 1

    if player == computer :
        mega_winner = 'tie'
    elif player > computer:
        mega_winner = 'X'
    elif computer > player:
        mega_winner = 'O'

    return mega_winner

"""
@objective : returns true if game cannot continue
"""


def checkMegaWinHeadOn(mainBoard, winner_records):
    """

    :param mainBoard:
    :param winner_records:
    :return:
    """
    mega_winner, mb1, mb2, mb3 = None, None, None, None

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

    for ((i1, j1), (i2, j2), (i3, j3)) in possible_cases:

        if 'X' == winner_records[i1][j1][0]['winner'] \
                == winner_records[i2][j2][0]['winner'] \
                == winner_records[i3][j3][0]['winner']:
            mega_winner = 'X'
            mb1 = (i1, j1)
            mb2 = (i2, j2)
            mb3 = (i3, j3)
            break

        elif 'O' == winner_records[i1][j1][0]['winner'] \
                == winner_records[i2][j2][0]['winner'] \
                == winner_records[i3][j3][0]['winner']:
            mega_winner = 'O'
            mb1 = (i1, j1)
            mb2 = (i2, j2)
            mb3 = (i3, j3)
            break

    return mega_winner, mb1, mb2, mb3

'''
@objective : draw the lines that appear in the main board
@usage     : This function will be used to draw 9 lines
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


def initialise_new_game(val):
    """
    :param val:
    :return:
    """

    # convert it to looping structure
    board_structure = [
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
    winner_records_structure = [
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

    # convert it to looping structure

    # values for testing purpose
    usedBoxes = [
        [
            [
                ['X', False, False],  # small box row 0
                [False, 'X', False],  # small box row 1
                [False, False, 'X']  # small box row 2
            ],  # small box 0

            [
                [False, False, 'O'],  # small box row 0
                [False, False, 'O'],  # small box row 1
                [False, False, 'O']  # small box row 2
            ],  # small box 1

            [
                ['O', False, False],  # small box row 0
                [False, 'O', False],  # small box row 1
                [False, False, 'O']  # small box row 2
            ]  # small box 2
        ],  # big row zero

        [
            [
                ['X', False, False],  # small box row 0
                [False, 'X', False],  # small box row 1
                [False, False, 'X']  # small box row 2
            ],  # small box 0

            [
                [False, False, 'O'],  # small box row 0
                [False, False, 'O'],  # small box row 1
                [False, False, 'O']  # small box row 2
            ],  # small box 1

            [
                ['O', False, False],  # small box row 0
                [False, 'O', False],  # small box row 1
                [False, False, 'O']  # small box row 2
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
            ],  # small box 0

            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ]  # small box 0
        ]  # big row zero
    ]
    winner_records = [
        [
            [
                {
                    'winner': 'X',
                    'winner_tuple': [[0, 0], [1, 1], [2, 2]]
                },
            ],  # small box 0

            [
                {
                    'winner': 'O',
                    'winner_tuple': [[0, 2], [1, 2], [2, 2]]

                }
            ],  # small box 1

            [
                {
                    'winner': 'O',
                    'winner_tuple': [[0, 0], [1, 1], [2, 2]]

                }
            ]  # small box 2
        ],  # big row zero
        [
            [
                {
                    'winner': 'X',
                    'winner_tuple': [[0, 0], [1, 1], [2, 2]]
                },
            ],  # small box 0

            [
                {
                    'winner': 'O',
                    'winner_tuple': [[0, 2], [1, 2], [2, 2]]

                }
            ],  # small box 1

            [
                {
                    'winner': 'O',
                    'winner_tuple': [[0, 0], [1, 1], [2, 2]]

                }
            ]  # small box 2
        ],  # big row zero
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
                },
            ],  # small box 0

            [
                {
                    'winner': None,
                    'winner_tuple': None
                },
            ]  # small box 0
        ]  # big row zero
    ]

    usedBoxes = [
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

    horizRect1 = pygame.Rect(left, top, width, height)

    # highlight
    pygame.draw.rect(DISPLAYSURFACE, BLACK, horizRect1)
    # redraw lines
    drawLines()
    # redraw symbols
    redraw(mainBoard, row, column)
    # for now, come back after its safe
    if winner_records[row][column][0]['winner'] is not None and winner_records[row][column][0]['winner'] != 'tie':
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

    # highlight_box_color = (140, 255, 26)
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


def drawWinner(smallFont, mega_winner):
    """

    :param mega_winner:
    :return:
    """
    if mega_winner == 'tie':
        message = smallFont.render('The Game resulted in a TIE', True, COMBLUE, BGCOLOR)

    elif mega_winner == 'X':
        message = smallFont.render('Winner is Player 1 ( X )', True, COMBLUE, BGCOLOR)

    elif mega_winner == 'O':
        message = smallFont.render('Winner is Player 2 ( O )', True, COMBLUE, BGCOLOR)

    messageRect = message.get_rect()

    messageRect.x = BOXSIZE * 5 - 10 + BOXSIZE
    messageRect.y = BOXSIZE - 5 + BOXSIZE + 15
    DISPLAYSURFACE.blit(message, messageRect)


def drawScoreBoard(smallFont, playerScore, computerScore, tieScore):
    scoreBoard = smallFont.render(
        'Player X : ' + str(playerScore) + '      ' + 'Player O : ' + str(computerScore) + '       ' + 'Tie: ' + str(
            tieScore), True, COMBLUE, BGCOLOR)
    scoreBoardRect = scoreBoard.get_rect()
    scoreBoardRect.x = BOXSIZE * 4 + 21
    scoreBoardRect.y = BOXSIZE - 5
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

    if x is None or y is None:
        return (None, None, None, None)

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
@:Function : gameOver
@:purpose: checks is the game is over - no space left to move
@:approach : If any one the boxes from used boxes is false, it means its not has been used.
Means, Board has still space left, return false to game over

If no space left, it is a game over
'''


def gameOver(mainBoard):
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
    mainBoard, winner_records = initialise_new_game(False)
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
    top = (YMARGIN + (3 * row) * (BOXSIZE + GAPSIZE)) + (box_row * (BOXSIZE + GAPSIZE)) + ((BOXSIZE) // 2)

    endPos = (left, top)

    # print(startPos)
    # print(endPos)
    pygame.draw.line(DISPLAYSURFACE, LINECOLOR, startPos, endPos, 5)

    # return startPos, endPos

    # In the small box mainBoard[row][column], boxes b1, b2, b3 needs to be highlighted


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
    # level = "smart"
    level = "easy"
    main(level)