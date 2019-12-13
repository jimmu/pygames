from random import randint
import sys

WIDTH = 1000 # Width of window
HEIGHT = 800 # Height of window
player = Actor("player") # Load in the player Actor image
rocketBase = Actor("player")
rocketStage1 = Actor("player")
fuel = Actor("player")
player.pos = 250, 100 # Set the player screen position
rocketBase.left = 100
rocketBase.bottom = HEIGHT
rocketStage1.left =  500
rocketStage1.bottom = HEIGHT
fuel.left=300
fuel.bottom=520
gameState="lookingForStage1"
GRAVITY=-0.25
JETPACK_STRENGTH=0.52
global ySpeed
rocketSpeed=0

def draw(): # Pygame Zero draw function
    global allThePlatforms
    
    screen.fill((128, 128, 128))
    player.draw()
    rocketBase.draw()
    rocketStage1.draw()
    fuel.draw()
    for platform in allThePlatforms:
        screen.draw.filled_rect((Rect((platform["left"], platform["top"]), (platform["width"], platform["height"]))), platform["colour"])
 
def update(): # Pygame Zero update function
    global ySpeed
    global gameState
    global rocketSpeed

    topBound=getTopBound()
    bottomBound=getBottomBound()
    leftBound=getLeftBound()
    rightBound=getRightBound()

    if keyboard.left: player.x -= 2
    if keyboard.right: player.x += 2

    if player.right > rightBound: player.right=rightBound;
    if player.left < leftBound: player.left=leftBound;
    if player.right >WIDTH: player.left=0
    if player.left <0: player.right =WIDTH;

    if keyboard.up : ySpeed += JETPACK_STRENGTH
    #Now because of gravity
    ySpeed += GRAVITY
    player.bottom -= ySpeed

    #Don't let us fall through the land
    if player.bottom >= bottomBound:
        player.bottom = bottomBound
        ySpeed=0

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
            gameState = "lookingForFuel"
    elif gameState == "lookingForFuel" :
        if (player.colliderect(fuel)) :
            gameState = "carryingFuel"
    elif gameState == "carryingFuel" :
        if (player.colliderect(rocketBase)) :
            fuel.right = rocketBase.left
            fuel.bottom = rocketBase.bottom
            gameState = "WIN"
        
    if gameState == "carryingStage1" :
        rocketStage1.left = player.right
        rocketStage1.bottom = player.top
    elif gameState == "carryingFuel" :
        fuel.left = player.right
        fuel.bottom = player.top
    elif gameState == "WIN" :
        if rocketBase.bottom <= 0 :
            sys.exit()
        rocketSpeed += 0.1
        rocketBase.bottom -= rocketSpeed
        rocketStage1.bottom -= rocketSpeed

def getTopBound():
    global allThePlatforms
    topBound=0
    for platform in allThePlatforms:
        if ((player.top >= platform["top"]+platform["height"]) and
            (player.right > platform["left"]) and
            (player.left < (platform["left"]+platform["width"]))):
            # We're directly below the platform
            topBound=max(topBound, platform["top"]+platform["height"])
    return topBound

def getBottomBound():
    global allThePlatforms
    bottomBound=HEIGHT
    for platform in allThePlatforms:
        if ((player.bottom <= platform["top"]) and
            (player.right > platform["left"]) and
            (player.left < (platform["left"]+platform["width"]))):
            # We're directly above the platform
            bottomBound=min(bottomBound, platform["top"])
    return bottomBound;

def getLeftBound():
    global allThePlatforms
    leftBound=0
    for platform in allThePlatforms:
        if ((player.left >= platform["left"]+platform["width"]) and
            (player.bottom > platform["top"]) and
            (player.top < (platform["top"]+platform["height"]))):
            # We're directly right of the platform
            leftBound=max(leftBound, platform["left"]+platform["width"])
    return leftBound

def getRightBound():
    global allThePlatforms
    rightBound=WIDTH    
    for platform in allThePlatforms:
        if ((player.right <= platform["left"]) and
            (player.bottom > platform["top"]) and
            (player.top < (platform["top"]+platform["height"]))):
            # We're directly left of the platform
            rightBound=min(rightBound, platform["left"])
    return rightBound

def makePlatforms():    
    global platform, platform2, allThePlatforms
    platform={"left" : 200,
              "top" : 220,
              "width" : 500,
              "height" : 20,
              "colour" : (0,175,0)
              }
    platform2={"left" : 300,
              "top" : 520,
              "width" : 300,
              "height" : 20,
              "colour" : (255, 255, 0)
              }
    platform3={"left" : 700,
              "top" : 720,
              "width" : 200,
              "height" : 18,
              "colour" : (2, 9, 244)
              }
    
    allThePlatforms=[platform, platform2, platform3]
                            
# End of functions
makePlatforms()
ySpeed=0
