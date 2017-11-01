import pygame, sys, random, copy
from pygame.locals import *

# CONSTANTS, yo

# Game window width and height
WINDOWWIDTH = 400
WINDOWHEIGHT = 500

# The infinite loops runs 30 times in one second
FPS = 30

# How big should be one small box
# when you modify this, also modify the main font, as the X lives inside a box
BOXSIZE = 100

# Width of the line in pixels : This is the thing that actually separate the input small boxes
GAPSIZE = 5

# Playing board width : How many small boxes needs to fit in the board
BOARDWIDTH = 3
BOARDHEIGHT = 3

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

XMARGIN = int((WINDOWWIDTH -(BOARDWIDTH * (BOXSIZE + GAPSIZE)))/2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE)))/2)

# RGB COLOUR MODEL
#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)
COMBLUE  = (233, 232, 255)


# GAME COLOURS

# Background Color
BGCOLOR = BLACK

# BOX color - UNUSED AS OF NOW
BOXCOLOR = BLUE

# The line which joins 3 consecutive elements at the end
LINECOLOR = YELLOW


def main():

    global FPSCLOCK, DISPLAYSURFACE

    # Initialise the library my friend
    pygame.init()

    # Hold the clock as a variable - to tick later : controls the loop iterations per second.
    FPSCLOCK = pygame.time.Clock()

    # The Surface over which everything will be drawn - Window width and height
    DISPLAYSURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    # mainFont : Font for drawing X and O in the boxes
    # Modification required : Remove magic number & put something relative to box
    mainFont = pygame.font.SysFont('Helvetica', 90)

    # smallFont : draws the score box and the end game credits
    smallFont = pygame.font.SysFont('Helvetica', 25)

    # Caption of window
    pygame.display.set_caption('Tic-Tac-Toe')

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
    mainBoard = makeEachBoxFalse(False)
    # Initially used boxes
    usedBoxes = makeEachBoxFalse(False)

    # Player turn : bool variable
    playerTurnDone = False

    # Paint the surface black
    DISPLAYSURFACE.fill(BGCOLOR)

    '''
    Draw all the required lines
    '''
    drawLines()

    # The GRAND game loop
    while True:

        # set mouseClick as False
        mouseClicked = False

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
        boxx, boxy = getBoxAtPixel(mousex, mousey)


        # If Inside the board, move forward, else ignore
        if boxx != None and boxy != None:

            # If box is not already used, & mouse if clicked just now, move forward
            if not usedBoxes[boxx][boxy] and mouseClicked and playerTurnDone is False:
                # DRAW X
                markBoxX(boxx, boxy, mainFont)
                # Play sound
                BEEP1.play()

                # set true to used Boxes
                usedBoxes[boxx][boxy] = True
                # Mark mainboard
                mainBoard[boxx][boxy] = XMARK
                # Player turn done
                playerTurnDone = True

                # Update display - early update
                # Needs update, or the last iteration isn't displayed.
                # Further, to solve this issue, we could extend one iteration,
                # But this approach is also cool, so good
                pygame.display.update()

            # If computer turn, play the move
            elif playerTurnDone == True:
                # a little delay - time pause for 500 ms
                pygame.time.wait(500)
                # derive the boxes to be marked with AI
                boxx, boxy = computerTurnWithAI(usedBoxes, mainBoard)

                # mark box, play sound
                markBoxO(boxx, boxy, mainFont)
                BEEP2.play()
                # update tables
                usedBoxes[boxx][boxy] = True
                mainBoard[boxx][boxy] = OMARK
                # next is player turn
                playerTurnDone = False
                pygame.display.update()

        # Check if anyone won the game, after the previous move
        playerWins, computerWins = gameWon(mainBoard)

        if playerWins:
            pygame.time.wait(500)
            highlightWin(mainBoard)
            BEEP3.play()
            pygame.display.update()
            playerScore += 1
            usedBoxes, mainBoard, playerTurnDone, playerWins, computerWins = boardReset(usedBoxes, mainBoard, playerTurnDone, playerWins, computerWins)
            DISPLAYSURFACE.fill(BGCOLOR)
            drawLines()
            
        elif computerWins:
            pygame.time.wait(500)
            highlightWin(mainBoard)
            BEEP3.play()
            pygame.display.update()
            computerScore += 1
            usedBoxes, mainBoard, playerTurnDone, playerWins, computerWins = boardReset(usedBoxes, mainBoard, playerTurnDone, playerWins, computerWins)
            DISPLAYSURFACE.fill(BGCOLOR)
            drawLines()

        else:
            if gameOver(usedBoxes, mainBoard):
                tieScore += 1
                usedBoxes, mainBoard, playerTurnDone, playerWins, computerWins = boardReset(usedBoxes, mainBoard, playerTurnDone, playerWins, computerWins)
                DISPLAYSURFACE.fill(BGCOLOR)
                drawLines()

        if tieScore >= 2:
            DISPLAYSURFACE.fill(BGCOLOR)
            pygame.display.update()
            pygame.time.wait(1000)
            warGameEnding(smallFont, COMPUTERVOICE)
            pygame.display.update()
            usedBoxes, mainBoard, playerTurnDone, playerWins, computerWins = boardReset(usedBoxes, mainBoard, playerTurnDone, playerWins, computerWins)
            tieScore = 0
            playerScore = 0
            computerScore = 0
            DISPLAYSURFACE.fill(BGCOLOR)
            drawLines()

        

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


def drawLines():

    #######VERTICAL LINES########
    
    left = XMARGIN + BOXSIZE
    top = YMARGIN

    # How wide is the vertical line
    width = GAPSIZE
    # height : How thick is the vertical line
    height = (BOXSIZE + GAPSIZE) * BOARDHEIGHT

    #  vertical rectangle needs to be drawn from top
    vertRect1 = pygame.Rect(left, top, width, height)
    pygame.draw.rect(DISPLAYSURFACE, WHITE, vertRect1)

    #  horizontal rectangle needs to be drawn from beside the first box
    vertRect2 = pygame.Rect(left + BOXSIZE + GAPSIZE, top, width, height)
    pygame.draw.rect(DISPLAYSURFACE, WHITE, vertRect2)

    '''
    The Thing i do not understand is why only one side of rectange is visible
    '''
    '''
    vertRect3 = pygame.Rect(left + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE, top, width, height)
    pygame.draw.rect(DISPLAYSURFACE, WHITE, vertRect3)
    '''

    ########HORIZONTAL LINES ##########

    # need to draw horizontal lines

    # left side distance = XMARGIN
    left = XMARGIN

    # Top distance is = YMARGIN + (for skipping the first box) BOXSIZE
    top = YMARGIN + BOXSIZE

    # How wide is the vertical line
    width = (BOXSIZE + GAPSIZE) * BOARDWIDTH
    # height : How thick is the horizontal line
    height = GAPSIZE

    #  horizontal rectangle needs to be drawn from top
    horizRect1 = pygame.Rect(left, top, width, height)
    pygame.draw.rect(DISPLAYSURFACE, WHITE, horizRect1)

    #  horizontal rectangle needs to be drawn from below the first box
    horizRect2 = pygame.Rect(left, top + BOXSIZE + GAPSIZE, width, height)
    pygame.draw.rect(DISPLAYSURFACE, WHITE, horizRect2)


'''
@Objective : converts each box in the Board to FALSE
@Approach  : each each element of row, make all the boxes in its column FALSE
@Note : The Box is list of lists. 
For each Row one sublist, one sublist represents columns
'''


def makeEachBoxFalse(val):
    usedBoxes = []
    for i in range(BOARDWIDTH):
        # append a list
        usedBoxes.append([val] * BOARDHEIGHT)
    # Return a list of lists
    return usedBoxes


def drawScoreBoard(smallFont, playerScore, computerScore, tieScore):
    scoreBoard = smallFont.render('Player: ' + str(playerScore) + '     ' + 'Computer: ' + str(computerScore) + '      ' + 'Tie: ' + str(tieScore), True, COMBLUE, BGCOLOR)
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


def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            # Draw a rectangle from top left coordinate of the box
            # If made box and mouse pixel intersect, we found it right
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


'''
@:function : leftTopCoordsOfBox
@:returns : The top left coordinates of a Small BOX
@:approach : absolute pixel = X Margin + (box size + width) * box number

'''


def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return left, top


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


def markBoxX(boxx, boxy, mainFont):
    '''
    This creates a new Surface with the specified text rendered on it. 
    pygame provides no way to directly draw text on an existing Surface:
    instead you must use Font.render() to create an image (Surface) of the text, 
    then blit this image onto another Surface.
    '''
    # Use Main Font to - render Xmark on a new surface
    mark = mainFont.render(XMARK, True, WHITE)
    '''
    Surfaces don't have a position, so you have to store the blit position in the rect. 
    When you call the get_rect method of a pygame.Surface, Pygame creates a new rect
    with the size of the surface with coordinates (x,y)=(0,0). 
    '''
    # Obtain the rectangle object of surface.
    markRect = mark.get_rect()

    # find center of small box
    centerx, centery = centerxAndCenteryOfBox(boxx, boxy)

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


def markBoxO(boxx, boxy, mainFont):
    centerx, centery = centerxAndCenteryOfBox(boxx, boxy)
    mark = mainFont.render(OMARK, True, WHITE)
    markRect = mark.get_rect()
    markRect.centerx = centerx
    markRect.centery = centery
    DISPLAYSURFACE.blit(mark, markRect)


'''
@:Function : computerTurnWithAI
@: Objective : The smart AI
'''


def computerTurnWithAI(usedBoxes, mainBoard):

    ## Step 1: Check to see if there is a winning move ##
    
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            mainBoardCopy = copy.deepcopy(mainBoard)
            if usedBoxes[boxx][boxy] == False:
                mainBoardCopy[boxx][boxy] = OMARK
                playerWins, computerWins = gameWon(mainBoardCopy)

                if computerWins == True:
                    return boxx, boxy




    ## Step 2: Check to see if there is a potential win that needs to be blocked ##
    
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDWIDTH):
            mainBoardCopy = copy.deepcopy(mainBoard)
            if usedBoxes[boxx][boxy] == False:
                mainBoardCopy[boxx][boxy] = XMARK
                playerWins, computerWins = gameWon(mainBoardCopy)

                if playerWins == True:
                    return boxx, boxy




    ## Step 3: Check if the center is empty ##

    mainBoardCopy = copy.deepcopy(mainBoard)

    if mainBoardCopy[1][1] == False:
        return 1, 1

    


    ## Step 4: Prevent a potential fork ##

    if ((mainBoardCopy[0][0] == mainBoardCopy[2][2] == XMARK) or
        (mainBoardCopy[0][2] == mainBoardCopy[2][0] == XMARK)):
        if mainBoardCopy[1][2] == False:
            return 1, 2

    if mainBoard[1][0] == XMARK:
        if mainBoard[0][1] == XMARK:
            if mainBoard[0][0] == False:
                return 0, 0

    if mainBoard[1][0] == XMARK:
        if mainBoard[2][1] == XMARK:
            if mainBoard[2][0] == False:
                return 2, 0

    if mainBoard[0][1] == XMARK:
        if mainBoard[1][2] == XMARK:
            if mainBoard[0][2] == False:
                return 0, 2

    if mainBoard[2][1] == XMARK:
        if mainBoard[1][2] == XMARK:
            if mainBoard[2][2] == False:
                return 2, 2
        

    if (mainBoard[0][2] == XMARK):
        if (mainBoard[2][1] == XMARK):
            if mainBoard[1][2] == False:
                return 1, 2
        elif (mainBoard[1][0]):
            if mainBoard[0][1] == False:
                return 0, 1

    if mainBoard[2][2] == XMARK:
        if mainBoard[0][1] == XMARK:
            if mainBoard[1][2] == False:
                return 1, 2
        elif mainBoard[1][0] == XMARK:
            if mainBoard[2][1] == False:
                return 2, 1

    if mainBoard[0][0] == XMARK:
        if mainBoard[2][1] == XMARK:
            if mainBoard[1][0] == False:
                return 1, 0
        elif mainBoard[1][2] == XMARK:
            if mainBoard[0][1] == False:
                return 0, 1

    if mainBoard[2][0] == XMARK:
        if mainBoard[1][2] == XMARK:
            if mainBoard[2][1] == False:
                return 2, 1
        elif mainBoard[0][1] == XMARK:
            if mainBoard[1][0] == False:
                return 1, 0

    

    

    
                            



    ## Step 5: Check if a corner is open ##
    
    xlist = [0, 2, 0, 2]
    ylist = [0, 2, 0, 2]

    random.shuffle(xlist)
    random.shuffle(ylist)

    for x in xlist:
        for y in ylist:
            if mainBoardCopy[x][y] == False:
                return x, y
    
    



    ## Step 6: Check if a side is open ##

    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            if mainBoardCopy[boxx][boxy] == False:
                return boxx, boxy








##### Functions dealing with an end of game ########

'''
Function : gameWon()
Purpose: Checks all the 8 scenarios of game winning and return the winner, if any
'''

def gameWon(mainBoard):

    # Player win by consecutive X mark
    if ((mainBoard[0][0] == mainBoard[1][0] == mainBoard[2][0] == XMARK) or
        (mainBoard[0][1] == mainBoard[1][1] == mainBoard[2][1] == XMARK) or
        (mainBoard[0][2] == mainBoard[1][2] == mainBoard[2][2] == XMARK) or
        (mainBoard[0][0] == mainBoard[0][1] == mainBoard[0][2] == XMARK) or
        (mainBoard[1][0] == mainBoard[1][1] == mainBoard[1][2] == XMARK) or
        (mainBoard[2][0] == mainBoard[2][1] == mainBoard[2][2] == XMARK) or
        (mainBoard[0][0] == mainBoard[1][1] == mainBoard[2][2] == XMARK) or
        (mainBoard[0][2] == mainBoard[1][1] == mainBoard[2][0] == XMARK)):

        playerWins = True
        computerWins = False
        return playerWins, computerWins

    # Computer win by consecutive O mark
    elif ((mainBoard[0][0] == mainBoard[1][0] == mainBoard[2][0] == OMARK) or
          (mainBoard[0][1] == mainBoard[1][1] == mainBoard[2][1] == OMARK) or
          (mainBoard[0][2] == mainBoard[1][2] == mainBoard[2][2] == OMARK) or
          (mainBoard[0][0] == mainBoard[0][1] == mainBoard[0][2] == OMARK) or
          (mainBoard[1][0] == mainBoard[1][1] == mainBoard[1][2] == OMARK) or
          (mainBoard[2][0] == mainBoard[2][1] == mainBoard[2][2] == OMARK) or
          (mainBoard[0][0] == mainBoard[1][1] == mainBoard[2][2] == OMARK) or
          (mainBoard[0][2] == mainBoard[1][1] == mainBoard[2][0] == OMARK)):

        playerWins = False
        computerWins = True
        return playerWins, computerWins

    # No one won
    else:
        playerWins = False
        computerWins = False
        return playerWins, computerWins


'''
@:Function : gameOver
@:purpose: checks is the game is over - no space left to move
@:approach : If any one the boxes from used boxes is false, it means its not has been used.
Means, Board has still space left, return false to game over

If no space left, it is a game over
'''

def gameOver(usedBoxes, mainBoard):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            if usedBoxes[boxx][boxy] == False:
                return False

    else:
        return True


def boardReset(usedBoxes, mainBoard, playerTurnDone, playerWins, computerWins):
    pygame.time.wait(1000)
    usedBoxes = makeEachBoxFalse(False)
    mainBoard = makeEachBoxFalse(False)
    playerTurnDone = False
    playerWins = computerWins = False

    return usedBoxes, mainBoard, playerTurnDone, playerWins, computerWins


def highlightWin(mainBoard):

    scenario1 = 1
    scenario2 = 2
    scenario3 = 3
    scenario4 = 4
    scenario5 = 5
    scenario6 = 6
    scenario7 = 7
    scenario8 = 8
    
    if mainBoard[0][0] == mainBoard[1][0] == mainBoard[2][0]:
        highLightBoxes(mainBoard, scenario1)

    
    elif mainBoard[0][1] == mainBoard[1][1] == mainBoard[2][1]:
        highLightBoxes(mainBoard, scenario2)

    
    elif mainBoard[0][2] == mainBoard[1][2] == mainBoard[2][2]:
        highLightBoxes(mainBoard, scenario3)

    
    elif mainBoard[0][0] == mainBoard[0][1] == mainBoard[0][2]:
        highLightBoxes(mainBoard, scenario4)

    
    elif mainBoard[1][0] == mainBoard[1][1] == mainBoard[1][2]:
        highLightBoxes(mainBoard, scenario5)

    
    elif mainBoard[2][0] == mainBoard[2][1] == mainBoard[2][2]:
        highLightBoxes(mainBoard, scenario6)

    
    elif mainBoard[0][0] == mainBoard[1][1] == mainBoard[2][2]:
        highLightBoxes(mainBoard, scenario7)

    
    elif mainBoard[2][0] == mainBoard[1][1] == mainBoard[0][2]:
        highLightBoxes(mainBoard, scenario8)


def highLightBoxes(mainBoard, scenario):

    if scenario == 1:
        startPos = (XMARGIN + (BOXSIZE/2), YMARGIN + (BOXSIZE/2))
        endPos = (XMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2), YMARGIN + (BOXSIZE/2))
        

        pygame.draw.line(DISPLAYSURFACE, LINECOLOR, startPos, endPos, 10)

    elif scenario == 2:
        startPos = (XMARGIN + (BOXSIZE/2), YMARGIN + BOXSIZE + GAPSIZE + (BOXSIZE/2))
        endPos = (XMARGIN + (BOXSIZE/2) + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE, YMARGIN + BOXSIZE + GAPSIZE + (BOXSIZE/2))


        pygame.draw.line(DISPLAYSURFACE, LINECOLOR, startPos, endPos, 10)

    elif scenario == 3:
        startPos = (XMARGIN + (BOXSIZE/2), YMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2))
        endPos = (XMARGIN + (BOXSIZE/2) + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE, YMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2))


        pygame.draw.line(DISPLAYSURFACE, LINECOLOR, startPos, endPos, 10)

    elif scenario == 4:
        startPos = (XMARGIN + (BOXSIZE/2), YMARGIN + (BOXSIZE/2))
        endPos = (XMARGIN + (BOXSIZE/2), YMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2))
        

        pygame.draw.line(DISPLAYSURFACE, LINECOLOR, startPos, endPos, 10)

    elif scenario == 5:
        startPos = (XMARGIN + BOXSIZE + GAPSIZE + (BOXSIZE/2), YMARGIN + (BOXSIZE/2))
        endPos = (XMARGIN + BOXSIZE + GAPSIZE + (BOXSIZE/2), YMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2))
        

        pygame.draw.line(DISPLAYSURFACE, LINECOLOR, startPos, endPos, 10)

    elif scenario == 6:
        startPos = (XMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2), YMARGIN + (BOXSIZE/2))
        endPos = (XMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2), YMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2))
        

        pygame.draw.line(DISPLAYSURFACE, LINECOLOR, startPos, endPos, 10)

    elif scenario == 7:
        startPos = (XMARGIN + (BOXSIZE/2), YMARGIN + (BOXSIZE/2))
        endPos = (XMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2), YMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2))

        
        pygame.draw.line(DISPLAYSURFACE, LINECOLOR, startPos, endPos, 10)

    elif scenario == 8:
        startPos = (XMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2), YMARGIN + (BOXSIZE/2))
        endPos = (XMARGIN + (BOXSIZE/2), YMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE/2))
        

        pygame.draw.line(DISPLAYSURFACE, LINECOLOR, startPos, endPos, 10)
    
        

def warGameEnding(smallFont, COMPUTERVOICE):
    COMPUTERVOICE.play()
    surfRect = DISPLAYSURFACE.get_rect()
    DISPLAYSURFACE.fill(BGCOLOR)

    computerMessage1 = smallFont.render('A strange game...', True, COMBLUE, BGCOLOR)
    computerMessage1Rect = computerMessage1.get_rect()
    computerMessage1Rect.x = XMARGIN/3
    computerMessage1Rect.y = YMARGIN * 2

    uncoverWords(computerMessage1, computerMessage1Rect)
    pygame.time.wait(1000)
        

    computerMessage2 = smallFont.render('The only winning move is not to play.', True, COMBLUE, BGCOLOR)
    computerMessage2Rect = computerMessage2.get_rect()
    computerMessage2Rect.x = XMARGIN/3
    computerMessage2Rect.centery = (YMARGIN * 2) + 50

    uncoverWords(computerMessage2, computerMessage2Rect)
    pygame.time.wait(3000)




def uncoverWords(text, textRect):
    textRectCopy = copy.deepcopy(textRect)
    blackRect = textRectCopy
    textLength = textRect.width

    revealSpeed = 5
    

    for i in range((textLength // revealSpeed) + 1):
        DISPLAYSURFACE.blit(text, textRect)
        pygame.draw.rect(DISPLAYSURFACE, BLACK, blackRect)
        pygame.display.update()

        blackRect.x += revealSpeed
        blackRect.width -= revealSpeed

    
    

if __name__ == '__main__':
    main()

