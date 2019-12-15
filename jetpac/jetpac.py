from random import randint
import sys

WIDTH = 1000 # Width of window
HEIGHT = 800 # Height of window
player = Actor("player") # Load in the player Actor image
rocketBase = Actor("rocketbaseoff")
rocketStage1 = Actor("rocketdoor")
rocketStage2 = Actor("rocketnosewithoutperson")
fuel = Actor("fuel")
player.pos = 250, 100 # Set the player screen position
rocketBase.left = 100
rocketBase.bottom = HEIGHT
rocketStage1.left =  500
rocketStage1.bottom = HEIGHT
rocketStage2.bottom=220
rocketStage2.right=700
fuel.left=300
fuel.bottom=520
gameState="lookingForStage1"
GRAVITY=-0.25
JETPACK_STRENGTH=0.52
global ySpeed
rocketSpeed=0

class Platform:
    def __init__(self, left, top, width, height, colour):
        self.left=left
        self.top=top
        self.width=width
        self.height=height
        self.right=left+width
        self.bottom=top+height
        self.colour=colour

def draw(): # Pygame Zero draw function
    global allThePlatforms
    global gameState
    
    screen.fill((000, 000, 000))
    if gameState != "WIN":
        player.draw()
    if gameState != "WIN":
        fuel.draw()
        
    rocketBase.draw()
    rocketStage1.draw()
    rocketStage2.draw()

    for platform in allThePlatforms:
        screen.draw.filled_rect((Rect((platform.left, platform.top), (platform.width, platform.height))), platform.colour)
 
def update(): # Pygame Zero update function
    global ySpeed
    global gameState
    global rocketSpeed

    if keyboard.left:
        leftBound=getLeftBound()
        player.x -= 2
        if player.left < leftBound: player.left=leftBound;
        if player.left <0: player.right =WIDTH;

    if keyboard.right:
        rightBound=getRightBound()
        player.x += 2
        if player.right > rightBound: player.right=rightBound;
        if player.right >WIDTH: player.left=0
    
    if keyboard.up :
        ySpeed += JETPACK_STRENGTH
        player.image="playerwithjet"
    else :
        player.image="player"
        
    #Now because of gravity
    ySpeed += GRAVITY

    if ySpeed  <= 0:
        bottomBound=getBottomBound()
        #Don't let us fall through the land
        player.bottom -= ySpeed
        if player.bottom >= bottomBound:
            player.bottom = bottomBound
            ySpeed=0
    else:
        topBound=getTopBound()
        player.bottom -= ySpeed
        #Don't let us fly past the top of the screen
        if player.top < topBound:
            player.top = topBound
            ySpeed=0

    #Have we picked up any rocket parts?
    if gameState == "lookingForStage1" :
        if (player.colliderect(rocketStage1)) :
            gameState = "carryingStage1"
    elif gameState == "carryingStage1" :
        if (player.colliderect(rocketBase)) :
            rocketStage1.left = rocketBase.left
            rocketStage1.bottom = rocketBase.top
            gameState = "lookingForStage2"
    elif gameState == "lookingForStage2" :
        if (player.colliderect(rocketStage2)) :
            gameState = "carryingStage2"        
    elif gameState == "carryingStage2" :
        if (player.colliderect(rocketBase)) :
            rocketStage2.left = rocketStage1.left
            rocketStage2.bottom = rocketStage1.top
            gameState = "lookingForFuel"
    elif gameState == "lookingForFuel" :
        if (player.colliderect(fuel)) :
            gameState = "carryingFuel"
    elif gameState == "carryingFuel" :
        if (player.colliderect(rocketBase)) :
            fuel.right = rocketBase.left
            fuel.bottom = rocketBase.bottom
            rocketBase.image="rocketbaseon"
            rocketStage2.image="rocketnose"
            gameState = "WIN"
        
    if gameState == "carryingStage1" :
        rocketStage1.left = player.right
        rocketStage1.bottom = player.top
    elif gameState == "carryingStage2" :
        rocketStage2.left = player.right
        rocketStage2.bottom = player.top
    elif gameState == "carryingFuel" :
        fuel.left = player.right
        fuel.bottom = player.top
    elif gameState == "WIN" :
        if rocketBase.bottom <= 0 :
            sys.exit()
        rocketSpeed += 0.1
        rocketBase.bottom -= rocketSpeed
        rocketStage1.bottom -= rocketSpeed
        rocketStage2.bottom -= rocketSpeed

def getTopBound():
    global allThePlatforms
    topBound=0
    for platform in allThePlatforms:
        if ((player.top >= platform.bottom) and
            (player.right > platform.left) and
            (player.left < platform.right)):
            # We're directly below the platform
            topBound=max(topBound, platform.bottom)
    return topBound

def getBottomBound():
    global allThePlatforms
    bottomBound=HEIGHT
    for platform in allThePlatforms:
        if ((player.bottom <= platform.top) and
            (player.right > platform.left) and
            (player.left < (platform.right))):
            # We're directly above the platform
            bottomBound=min(bottomBound, platform.top)
    return bottomBound;

def getLeftBound():
    global allThePlatforms
    leftBound = -1000
    for platform in allThePlatforms:
        if ((player.left >= platform.right) and
            (player.bottom > platform.top) and
            (player.top < (platform.bottom))):
            # We're directly right of the platform
            leftBound=max(leftBound, platform.right)
    return leftBound

def getRightBound():
    global allThePlatforms
    rightBound = WIDTH*2    
    for platform in allThePlatforms:
        if ((player.right <= platform.left) and
            (player.bottom > platform.top) and
            (player.top < (platform.bottom))):
            # We're directly left of the platform
            rightBound=min(rightBound, platform.left)
    return rightBound

def makePlatforms():    
    global allThePlatforms
    allThePlatforms=[Platform(200, 220, 500, 20, (0, 175, 0)),
                     Platform(300, 520, 300, 20, (255, 255, 0)),
                     Platform(700, 720, 200, 18, (2, 9, 244))
                    ]
                            
# End of functions
makePlatforms()
ySpeed=0
