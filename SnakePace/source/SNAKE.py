# ╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║ ╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗ ║
# ║ ║  ████████  ███    ██       ██       ██    ██  ████████       ██████       ██       ██████████  ████████   ██  ║ ║
# ║ ║  ██        ██ █   ██     ██  ██     ██  ██    ██             ██   ██    ██  ██     ██          ██         ██  ║ ║
# ║ ║  ████████  ██  █  ██    ██    ██    ████      ████████       ██████    ██    ██    ██          ████████   ██  ║ ║
# ║ ║        ██  ██   █ ██   ██▀▀▀▀▀▀██   ██  ██    ██             ██       ██▀▀▀▀▀▀██   ██          ██             ║ ║
# ║ ║  ████████  ██    ███  ██        ██  ██    ██  ████████       ██      ██        ██  ██████████  ████████   ██  ║ ║
# ║ ╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝ ║
# ║                                                                                                                   ║
# ║                 ╔═══════════════════════════════════╗ ╔═══════════════════════════════════╗                       ║
# ║                 ║              Made By:             ║ ║              Notes:               ║                       ║
# ║                 ║            Peter Toth             ║ ║ To compile the code yourself you  ║                       ║
# ║                 ║                &                  ║ ║ first need to install pyglet and  ║                       ║
# ║                 ║        Yusufjon Fayfullaev        ║ ║ pygame!!                          ║                       ║
# ║                 ║                                   ║ ║                                   ║                       ║
# ║                 ║          Version: V1.0            ║ ║ In windows type in command prompt:║                       ║
# ║                 ║                                   ║ ║ pip install pygame                ║                       ║
# ║                 ║                                   ║ ║ pip install pyglet                ║                       ║
# ║                 ╚═══════════════════════════════════╝ ╚═══════════════════════════════════╝                       ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

#git fucked!!
# Importing modules
from turtle import *
import time
import random
import pyglet
import pygame
import os
import sys
from tkinter import *

# DO NOT REMOVE!!!  THIS IS NEEDED TO COMPILE INTO SINGLE EXE WITH PYINSTALLER WITHOUT ERRORS!!
# DEFINE ALL RESOURCE PATHS WITH "resource_path("RESOURCE PATH")"
# ----------------------------------------------------------------------------------------------
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
def pls_dont_crash(exctype, value, traceback):
    sys.exit(0)
sys.excepthook = pls_dont_crash
# ----------------------------------------------------------------------------------------------

# Setting window size, title and icon (basic Tkinter setup)
main_window = Tk()
main_window.overrideredirect(0) #change this value to disable window borders
main_window.geometry("625x725")
middle_Frame = LabelFrame(main_window, relief=FLAT)
middle_Frame.pack()
canvas = Canvas(middle_Frame, width=622, height=722, relief=FLAT, highlightthickness=0)
canvas.pack()
main_window.iconbitmap(resource_path('resources/apple.ico'))
main_window.title("SnakePace")
turtle_screen = TurtleScreen(canvas)
turtle_screen.bgpic(resource_path('resources/levels/menuBG.gif'))
turtle_screen.bgcolor("black")
main_window.resizable(False, False)
turtle_screen.tracer(0)


# Sound effects and music setup (pygame mixer)
pygame.mixer.init()
pygame.init()
GAME_SONG_END = pygame.USEREVENT + 1 #these 2 are for getting an end event when the music ends
MENU_SONG_END = pygame.USEREVENT + 2 #check the line above..
popsound = pygame.mixer.Sound(resource_path("resources/sound/pop.mp3"))
exitsound = pygame.mixer.Sound(resource_path("resources/sound/exit.mp3"))
fruitsound = pygame.mixer.Sound(resource_path("resources/sound/fruit.mp3"))
nextlevelsound = pygame.mixer.Sound(resource_path("resources/sound/nextlevel.mp3"))
hitsound = pygame.mixer.Sound(resource_path("resources/sound/hit.mp3"))
retrysound = pygame.mixer.Sound(resource_path("resources/sound/retry.mp3"))
welcomesound = pygame.mixer.Sound(resource_path("resources/sound/welcome.mp3"))
gameoversound = pygame.mixer.Sound(resource_path("resources/sound/gameover.mp3"))
pygame.mixer.Channel(0).play(pygame.mixer.Sound(resource_path('resources/sound/menuBG.mp3')))
pygame.mixer.Channel(0).pause()
LevelSound = resource_path("resources/sound/level1.mp3")
pygame.mixer.Channel(1).set_volume(0.3) #Note: volume control in pygame mixer is kinda broken under windows...
pygame.mixer.Channel(0).set_volume(0.3)
pygame.mixer.Channel(1).play(pygame.mixer.Sound(LevelSound))
pygame.mixer.Channel(1).pause()
pygame.mixer.Channel(1).set_endevent(GAME_SONG_END)
pygame.mixer.Channel(0).set_endevent(MENU_SONG_END)
soundSwitch = 0 # variable for avoiding an evil loop of restarting the music till python crashes...

# Welcome sound (I just thought it'd be neat..) -Fuzzky
pygame.mixer.Sound.play(welcomesound)

# Setting global variables
delay = 0.12 #First level speed
score = 0 #Initial score
goal = 5 #Initial goal
Current_level = 0 #Initial level count (yes it starts from 0 because I cba to change all the code)
animationCounter = 0 #Animation frame counter for the fruit animation (You will see why a bit more down...)
menuActive = 1 #Setting a menu/pause state so the game knows it's paused
retryActive = 0 #Setting initial state of the retry button
muteState = 0 #setting initial state for the mute button (Change this to 1 to mute the game as it starts)
reduceScore = 1 # setting the initial penalty for hitting the snake's tail
tails = [] #Setting up a variable for incrementing the snake's tail
lastDirection = "none" #setting the Last direction the head was moving (this is mainly used to avoid accidental tail hits)
LevelBG = 'resources/levels/level1.gif' #Setting initial 1st level background
winState = False #checks if the player has won or not (needed to not mess up the start button and pause message...)
obstacles = [] #Array to store all the obstacle objects in
obstacle_count = 0 #Variable to set up the initial obstacle count


# Importing font
# yeah... I had to import pyglet just to get custom fonts.. -Fuzzky
pyglet.font.add_file(resource_path('resources/LLPIXEL3.ttf'))
LLPixel = pyglet.font.load('LLPixel')

# Defining snake shape options
#There's a hella lot here so just scroll by...
tailGreen = resource_path("resources/sprites/tailgreen.gif")
tailBlue = resource_path("resources/sprites/tailblue.gif")
tailPurple = resource_path("resources/sprites/tailpurple.gif")
tailRed = resource_path("resources/sprites/tailred.gif")
tailYellow = resource_path("resources/sprites/tailyellow.gif")
tailPink = resource_path("resources/sprites/tailpink.gif")
turtle_screen.addshape(tailGreen)
turtle_screen.addshape(tailBlue)
turtle_screen.addshape(tailPurple)
turtle_screen.addshape(tailRed)
turtle_screen.addshape(tailYellow)
turtle_screen.addshape(tailPink)
snake_tail = tailGreen
headGreen = resource_path("resources/sprites/headgreen.gif")
headBlue = resource_path("resources/sprites/headblue.gif")
headPurple = resource_path("resources/sprites/headpurple.gif")
headRed = resource_path("resources/sprites/headred.gif")
headYellow = resource_path("resources/sprites/headyellow.gif")
headPink = resource_path("resources/sprites/headpink.gif")
turtle_screen.addshape(headGreen)
turtle_screen.addshape(headBlue)
turtle_screen.addshape(headPurple)
turtle_screen.addshape(headRed)
turtle_screen.addshape(headYellow)
turtle_screen.addshape(headPink)
greenSnakeButton = resource_path("resources/sprites/greensnake.gif")
blueSnakeButton = resource_path("resources/sprites/bluesnake.gif")
purpleSnakeButton = resource_path("resources/sprites/purplesnake.gif")
redSnakeButton = resource_path("resources/sprites/redsnake.gif")
yellowSnakeButton = resource_path("resources/sprites/yellowsnake.gif")
pinkSnakeButton = resource_path("resources/sprites/pinksnake.gif")
turtle_screen.addshape(greenSnakeButton)
turtle_screen.addshape(blueSnakeButton)
turtle_screen.addshape(purpleSnakeButton)
turtle_screen.addshape(redSnakeButton)
turtle_screen.addshape(yellowSnakeButton)
turtle_screen.addshape(pinkSnakeButton)

# Defining button shapes and menu screens
#yepp, even more custom shapes... I wish there was a way to just point to their location without "addshape"..
retryButton = resource_path("resources/sprites/retry.gif")
continueButton = resource_path("resources/sprites/continue.gif")
startButton = resource_path("resources/sprites/start.gif")
customizeButton = resource_path("resources/sprites/customize.gif")
exitButton = resource_path("resources/sprites/exit.gif")
muteButton = resource_path("resources/sprites/mute.gif")
muteButtonOff = resource_path("resources/sprites/muteoff.gif")
menuButton = resource_path("resources/sprites/MiniMenu.gif")
backButton = resource_path("resources/sprites/back.gif")
helpButton = resource_path("resources/sprites/help.gif")
helpPage = resource_path("resources/sprites/helppage.gif")
creditsPage = resource_path("resources/sprites/credits.gif")
creditsButton = resource_path("resources/sprites/creditsbutton.gif")
logo = resource_path("resources/sprites/logo.gif")
customizationPage = resource_path("resources/sprites/customizationpage.gif")
help2 = resource_path("resources/sprites/help2.gif")
win = resource_path("resources/sprites/youwin.gif")
obstacle_texture1 = resource_path("resources/sprites/obs1.gif")
turtle_screen.addshape(obstacle_texture1)
turtle_screen.addshape(help2)
turtle_screen.addshape(win)
turtle_screen.addshape(customizationPage)
turtle_screen.addshape(continueButton)
turtle_screen.addshape(logo)
turtle_screen.addshape(retryButton)
turtle_screen.addshape(muteButton)
turtle_screen.addshape(muteButtonOff)
turtle_screen.addshape(startButton)
turtle_screen.addshape(customizeButton)
turtle_screen.addshape(exitButton)
turtle_screen.addshape(helpButton)
turtle_screen.addshape(menuButton)
turtle_screen.addshape(backButton)
turtle_screen.addshape(creditsButton)
turtle_screen.addshape(creditsPage)
turtle_screen.addshape(helpPage)

# Defining fruit animation frames
# (This is needed simply because Turtle doesn't support animated gifs....sad..)
fruit_apple_frame1 = resource_path("resources/sprites/apple.gif")
fruit_apple_frame2 = resource_path("resources/sprites/apple1.gif")
fruit_apple_frame3 = resource_path("resources/sprites/apple2.gif")
fruit_apple_frame4 = resource_path("resources/sprites/apple3.gif")
fruit_apple_frame5 = resource_path("resources/sprites/apple4.gif")
turtle_screen.addshape(fruit_apple_frame1)
turtle_screen.addshape(fruit_apple_frame2)
turtle_screen.addshape(fruit_apple_frame3)
turtle_screen.addshape(fruit_apple_frame4)
turtle_screen.addshape(fruit_apple_frame5)
fruit_apple = [fruit_apple_frame1, fruit_apple_frame2, fruit_apple_frame3, fruit_apple_frame4,
               fruit_apple_frame5, fruit_apple_frame4, fruit_apple_frame3, fruit_apple_frame2]
fruit_grape_frame1 = resource_path("resources/sprites/grape.gif")
fruit_grape_frame2 = resource_path("resources/sprites/grape1.gif")
fruit_grape_frame3 = resource_path("resources/sprites/grape2.gif")
fruit_grape_frame4 = resource_path("resources/sprites/grape3.gif")
fruit_grape_frame5 = resource_path("resources/sprites/grape4.gif")
turtle_screen.addshape(fruit_grape_frame1)
turtle_screen.addshape(fruit_grape_frame2)
turtle_screen.addshape(fruit_grape_frame3)
turtle_screen.addshape(fruit_grape_frame4)
turtle_screen.addshape(fruit_grape_frame5)
fruit_grape = [fruit_grape_frame1, fruit_grape_frame2, fruit_grape_frame3, fruit_grape_frame4,
               fruit_grape_frame5, fruit_grape_frame4, fruit_grape_frame3, fruit_grape_frame2]
fruit_orange_frame1 = resource_path("resources/sprites/orange.gif")
fruit_orange_frame2 = resource_path("resources/sprites/orange1.gif")
fruit_orange_frame3 = resource_path("resources/sprites/orange2.gif")
fruit_orange_frame4 = resource_path("resources/sprites/orange3.gif")
fruit_orange_frame5 = resource_path("resources/sprites/orange4.gif")
turtle_screen.addshape(fruit_orange_frame1)
turtle_screen.addshape(fruit_orange_frame2)
turtle_screen.addshape(fruit_orange_frame3)
turtle_screen.addshape(fruit_orange_frame4)
turtle_screen.addshape(fruit_orange_frame5)
fruit_orange = [fruit_orange_frame1, fruit_orange_frame2, fruit_orange_frame3, fruit_orange_frame4,
                fruit_orange_frame5, fruit_orange_frame4, fruit_orange_frame3, fruit_orange_frame2, ]
fruit_banana_frame1 = resource_path("resources/sprites/banana.gif")
fruit_banana_frame2 = resource_path("resources/sprites/banana1.gif")
fruit_banana_frame3 = resource_path("resources/sprites/banana2.gif")
fruit_banana_frame4 = resource_path("resources/sprites/banana3.gif")
fruit_banana_frame5 = resource_path("resources/sprites/banana4.gif")
turtle_screen.addshape(fruit_banana_frame1)
turtle_screen.addshape(fruit_banana_frame2)
turtle_screen.addshape(fruit_banana_frame3)
turtle_screen.addshape(fruit_banana_frame4)
turtle_screen.addshape(fruit_banana_frame5)
fruit_banana = [fruit_banana_frame1, fruit_banana_frame2, fruit_banana_frame3, fruit_banana_frame4,
                fruit_banana_frame5, fruit_banana_frame4, fruit_banana_frame3, fruit_banana_frame2, ]

# creating main body/head of the snake
#planned to use a custom image, but turtle doesn't allow changing the rotation of custom shapes..
head = RawTurtle(turtle_screen)
head.shape('square')
head.color('#a6d601', 'white')
head.penup()
head.goto(0, -10)
head.direction = "Stop"
head.hideturtle()

# creating fruit in the game
fruit_shapes = [fruit_apple, fruit_grape, fruit_orange, fruit_banana]
fruit_type = ["Apples", "Grapes", "Oranges", "Bananas", "Apples"]
fruit = RawTurtle(turtle_screen)
fruit.speed(0)
fruit.penup()
fruit.goto(0, 52)
fruit.hideturtle()

# Setting up text turtle and writing out initial message
pen = RawTurtle(turtle_screen)
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 300)
pen.write("PRESS START", align="center", font=("LLPixel", 24, 'normal'))

# Menu and buttons shape Setup
#There's a lot here too... just scroll by..
HelpPage = RawTurtle(turtle_screen)
Back = RawTurtle(turtle_screen)
Help = RawTurtle(turtle_screen)
Start = RawTurtle(turtle_screen)
Customize = RawTurtle(turtle_screen)
Exit = RawTurtle(turtle_screen)
Mute = RawTurtle(turtle_screen)
MuteOFFbutton = RawTurtle(turtle_screen)
CreditsButton = RawTurtle(turtle_screen)
CreditsPage = RawTurtle(turtle_screen)
HowToPage = RawTurtle(turtle_screen)
MiniMenu = RawTurtle(turtle_screen)
CustomizePage = RawTurtle(turtle_screen)
SnakeTailColor = RawTurtle(turtle_screen)
SnakeHeadColor = RawTurtle(turtle_screen)
Help2 = RawTurtle(turtle_screen)
Win = RawTurtle(turtle_screen)

Start.shape(startButton)
Start.penup()
Start.goto(0, 50)
Customize.shape(customizeButton)
Customize.penup()
Customize.goto(0, -50)
Exit.shape(exitButton)
Exit.penup()
Exit.goto(0, -150)
Mute.shape(muteButtonOff)
Mute.penup()
Mute.goto(270, 320)
MuteOFFbutton.shape(muteButton)
MuteOFFbutton.penup()
MuteOFFbutton.goto(270, 320)
MiniMenu.shape(menuButton)
MiniMenu.penup()
MiniMenu.goto(-270, 320)
Help.shape(helpButton)
Help.penup()
Help.goto(-270, -320)
HelpPage.shape(helpPage)
HelpPage.penup()
HelpPage.goto(0, 0)
CreditsPage.shape(creditsPage)
CreditsPage.penup()
CreditsPage.goto(0, 0)
CustomizePage.shape(customizationPage)
CustomizePage.penup()
CustomizePage.goto(0, 0)
SnakeTailColor.color('green')
SnakeTailColor.shape(greenSnakeButton)
SnakeTailColor.penup()
SnakeTailColor.goto(0, -40)
SnakeHeadColor.color('#a6d601', 'white')
SnakeHeadColor.shape('square')
SnakeHeadColor.penup()
SnakeHeadColor.goto(147, -40)
CreditsButton.shape(creditsButton)
CreditsButton.penup()
CreditsButton.goto(0, -160)
Help2.shape(help2)
Help2.penup()
Help2.goto(0, -160)
Back.shape(backButton)
Back.penup()
Back.goto(-270, -320)
Retry = RawTurtle(turtle_screen)
Retry.shape(retryButton)
Retry.penup()
Retry.goto(0, 27)
Logo = RawTurtle(turtle_screen)
Logo.shape(logo)
Logo.penup()
Logo.goto(0, 170)
Win.shape(win)
Win.penup()
Win.goto(0, 0)
Mute.showturtle()
MiniMenu.showturtle()
Help.showturtle()
Logo.showturtle()
Help2.hideturtle()
SnakeHeadColor.hideturtle()
MuteOFFbutton.hideturtle()
MiniMenu.hideturtle()
Win.hideturtle()
CustomizePage.hideturtle()
SnakeTailColor.hideturtle()
HelpPage.hideturtle()
Back.hideturtle()
MiniMenu.hideturtle()
HowToPage.hideturtle()
CreditsPage.hideturtle()
CreditsButton.hideturtle()
Retry.hideturtle()
turtle_screen.update()
time.sleep(2)
pygame.mixer.Channel(0).unpause()

# defining button clicks and core game functions
#These 2 handle the snake color customization options
def snakeTailColor(a, b):
    global snake_tail
    global index
    if SnakeTailColor.color() == ("green", "green"):
        SnakeTailColor.color('blue')
        SnakeTailColor.shape(blueSnakeButton)
        snake_tail = tailBlue
    elif SnakeTailColor.color() == ("blue", "blue"):
        SnakeTailColor.color('purple')
        SnakeTailColor.shape(purpleSnakeButton)
        snake_tail = tailPurple
    elif SnakeTailColor.color() == ("purple", "purple"):
        SnakeTailColor.color('red')
        snake_tail = tailRed
        SnakeTailColor.shape(redSnakeButton)
    elif SnakeTailColor.color() == ("red", "red"):
        SnakeTailColor.color('yellow')
        SnakeTailColor.shape(yellowSnakeButton)
        snake_tail = tailYellow
    elif SnakeTailColor.color() == ("yellow", "yellow"):
        SnakeTailColor.color('pink')
        SnakeTailColor.shape(pinkSnakeButton)
        snake_tail = tailPink
    elif SnakeTailColor.color() == ("pink", "pink"):
        SnakeTailColor.color('green')
        SnakeTailColor.shape(greenSnakeButton)
        snake_tail = tailGreen
    if tails!=[]:
        tails[0].shape(snake_tail)
    for index in range(len(tails) - 1, 0, -1):
        tails[index].shape(snake_tail)

def snakeHeadColor(a, b):
    if SnakeHeadColor.color() == ((0.6509803921568628, 0.8392156862745098, 0.00392156862745098), 'white'):
        head.color("#282cae", "white")
        SnakeHeadColor.color("#282cae", "white")
    elif SnakeHeadColor.color() == ((0.1568627450980392, 0.17254901960784313, 0.6823529411764706), 'white'):
        head.color("#6d28ae", "white")
        SnakeHeadColor.color("#6d28ae", "white")
    elif SnakeHeadColor.color() == ((0.42745098039215684, 0.1568627450980392, 0.6823529411764706), 'white'):
        head.color("#ae2828", "white")
        SnakeHeadColor.color("#ae2828", "white")
    elif SnakeHeadColor.color() == ((0.6823529411764706, 0.1568627450980392, 0.1568627450980392), 'white'):
        head.color("#cec609", "white")
        SnakeHeadColor.color("#cec609", "white")
    elif SnakeHeadColor.color() == ((0.807843137254902, 0.7764705882352941, 0.03529411764705882), 'white'):
        head.color("#eb62b7", "white")
        SnakeHeadColor.color("#eb62b7", "white")
    elif SnakeHeadColor.color() == ((0.9215686274509803, 0.3843137254901961, 0.7176470588235294), 'white'):
        head.color("#a6d601", "white")
        SnakeHeadColor.color("#a6d601", "white")

#Updates the goal readout on the top
def updategoal():
    pen.clear()
    pen.write("{} : {} / {} ".format(fruit_type[Current_level], score, goal), align="center",
              font=("LLPixel", 24, 'normal'))

#The name of these two are self explanatory..
def gameover():
    global Current_level
    global retryActive
    global tail
    global tails
    global x
    global y
    global score
    global goal
    global soundSwitch
    global obstacle_count
    global obstacles
    global obstacle
    obstacle_count = 0
    for obstacle in obstacles:
        obstacle.goto(1000, 1000)
    for tail in tails:
        tail.goto(1000, 1000)
    obstacles.clear()
    if retryActive == 0:
        turtle_screen.bgpic(resource_path('resources/levels/menuBG.gif'))
        Retry.showturtle()
        pygame.mixer.Channel(2).play(pygame.mixer.Sound(gameoversound))
        Exit.goto(0, -87)
        tails.clear()
        obstacles.clear()
        pygame.mixer.Channel(1).pause()
        pygame.mixer.Channel(0).pause()
        Current_level = 0
        head.direction = "stop"
        head.goto(1, -10)
        pen.clear()
        pen.write("GAME OVER", align="center", font=("LLPixel", 24, 'normal'))
        head.hideturtle()
        fruit.hideturtle()
        Exit.showturtle()
        MiniMenu.hideturtle()
        retryActive = 2
    # Checking if retry button is pressed
    if retryActive == 1:
        Exit.hideturtle()
        Retry.hideturtle()
        MiniMenu.showturtle()
        head.showturtle()
        fruit.showturtle()
        Exit.goto(0, -150)
        score = 0
        goal = 5
        soundSwitch = 0
        retryActive = 0
        movefood()
        updategoal()
        pygame.mixer.Channel(1).play(pygame.mixer.Sound(resource_path('resources/sound/level1.mp3')))
        levelsetup()

def YouWin():
    global Current_level
    global menuActive
    global winState
    global goal
    if Current_level == 4:
        winState = True
        menuScreen(0, 0)
        Win.showturtle()
        pen.clear()
        pen.write("YOU WON!!", align="center", font=("LLPixel", 24, 'normal'))
        Start.shape(startButton)
        Current_level = 0
        menuActive = 0
        goal = 5
        levelsetup()
        turtle_screen.bgpic(resource_path('resources/levels/menuBG.gif'))
        menuActive = 1

#Ah, this one decides which fruits appear on which level and increments the frame count
def animatefruit():
    global animationCounter
    if Current_level == 0 and menuActive == 0:
        fruit.shape(fruit_apple[animationCounter])
    elif Current_level == 1 and menuActive == 0:
        fruit.shape(fruit_grape[animationCounter])
    elif Current_level == 2 and menuActive == 0:
        fruit.shape(fruit_orange[animationCounter])
    elif Current_level == 3 and menuActive == 0:
        fruit.shape(fruit_banana[animationCounter])
    if animationCounter >= 7:
        animationCounter = 0
    animationCounter += 1

#Sets all the options for all the levels! (change stuff in here to change gameplay)
def levelsetup():
    global delay
    global soundSwitch
    global LevelSound
    global LevelBG
    global reduceScore
    global Current_level
    global goal
    global obstacle_count
    global obstacles
    global obstacle
    if Current_level == 0 and menuActive == 0 and retryActive != 2:
        LevelBG = 'resources/levels/level1.gif'
        obstacle_count = 0
        for obstacle in obstacles:
            obstacle.goto(1000, 1000)
        obstacles.clear()
        #!!TO CHANGE 1ST LEVEL SPEED ALSO CHANGE DELAY ON LINE 82!!
        delay = 0.12
        reduceScore = 1
    elif Current_level == 1 and menuActive == 0 and retryActive != 2:
        LevelBG = 'resources/levels/level2.gif'
        # OBSTACLE SETUP!!!!--------------------------------------------------
        while obstacle_count < 42:
            obstacle = RawTurtle(turtle_screen)
            obstacle.speed(0)
            obstacle.shape(obstacle_texture1)
            obstacle.penup()
            obstacle.goto(179, -130)
            obstacle.setheading(90)
            obstacles.append(obstacle)
            obstacle_count += 1
        for index in range(len(obstacles) - 1, 0, -1):
            g = obstacle.xcor()
            h = obstacle.ycor()
            obstacles[index].goto(g, h)
            obstacles[index].shape(obstacle_texture1)
        obstacles[0].goto(179, -150)
        obstacles[1].goto(159, -150)
        obstacles[2].goto(139, -150)
        obstacles[3].goto(119, -150)
        obstacles[4].goto(99, -150)
        obstacles[5].goto(79, -150)
        obstacles[6].goto(59, -150)
        obstacles[7].goto(39, -150)
        obstacles[8].goto(19, -150)
        obstacles[9].goto(-1, -150)
        obstacles[10].goto(-21, -150)
        obstacles[11].goto(-41, -150)
        obstacles[12].goto(-61, -150)
        obstacles[13].goto(-81, -150)
        obstacles[14].goto(-101, -150)
        obstacles[15].goto(-121, -150)
        obstacles[16].goto(-141, -150)
        obstacles[17].goto(-161, -150)
        obstacles[18].goto(-181, -150)
        obstacles[19].goto(-181, -130)

        obstacles[20].goto(179, 50)
        obstacles[21].goto(159, 70)
        obstacles[22].goto(139, 70)
        obstacles[23].goto(119, 70)
        obstacles[24].goto(99, 70)
        obstacles[25].goto(79, 70)
        obstacles[26].goto(59, 70)
        obstacles[27].goto(39, 70)
        obstacles[28].goto(19, 70)
        obstacles[29].goto(-1, 70)
        obstacles[30].goto(-21, 70)
        obstacles[31].goto(-41, 70)
        obstacles[32].goto(-61, 70)
        obstacles[33].goto(-81, 70)
        obstacles[34].goto(-101, 70)
        obstacles[35].goto(-121, 70)
        obstacles[36].goto(-141, 70)
        obstacles[37].goto(-161, 70)
        obstacles[38].goto(-181, 70)
        obstacles[39].goto(-181, 50)
        obstacles[40].goto(179, 70)
        # OBSTACLE SETUP END!!!!----------------------------------------------
        delay = 0.1  #sets Level speed
        reduceScore = 2  #sets the penalty for hitting the snake's tail or obstacles
    elif Current_level == 2 and menuActive == 0 and retryActive != 2:
        LevelBG = 'resources/levels/level3.gif'
        # OBSTACLE SETUP!!!!--------------------------------------------------
        obstacle_count = 0
        for obstacle in obstacles:
            obstacle.goto(1000, 1000)
        obstacles.clear()
        while obstacle_count < 37:
            obstacle = RawTurtle(turtle_screen)
            obstacle.speed(0)
            obstacle.shape(obstacle_texture1)
            obstacle.penup()
            obstacle.goto(260, 190)
            obstacle.setheading(90)
            obstacles.append(obstacle)
            obstacle_count += 1
        for index in range(len(obstacles) - 1, 0, -1):
            g = obstacle.xcor()
            h = obstacle.ycor()
            obstacles[index].goto(g, h)
            obstacles[index].shape(obstacle_texture1)
        # Top right obstacle
        obstacles[1].goto(260, 210)
        obstacles[2].goto(260, 230)
        obstacles[3].goto(240, 230)
        obstacles[4].goto(220, 230)
        obstacles[5].goto(220, 210)
        obstacles[6].goto(220, 190)
        obstacles[7].goto(240, 190)
        obstacles[8].goto(240, 210)
        # Top left obstacle
        obstacles[9].goto(-260, 210)
        obstacles[10].goto(-260, 230)
        obstacles[11].goto(-240, 230)
        obstacles[12].goto(-220, 230)
        obstacles[13].goto(-220, 210)
        obstacles[14].goto(-220, 190)
        obstacles[15].goto(-240, 190)
        obstacles[16].goto(-240, 210)
        obstacles[17].goto(-260, 190)
        # Bottom right obstacle
        obstacles[18].goto(260, -290)
        obstacles[19].goto(260, -310)
        obstacles[20].goto(240, -310)
        obstacles[21].goto(220, -310)
        obstacles[22].goto(220, -290)
        obstacles[23].goto(220, -270)
        obstacles[24].goto(240, -270)
        obstacles[25].goto(240, -290)
        obstacles[26].goto(260, -270)
        # Bottom left obstacle
        obstacles[27].goto(-260, -290)
        obstacles[28].goto(-260, -310)
        obstacles[29].goto(-240, -310)
        obstacles[30].goto(-220, -310)
        obstacles[32].goto(-220, -290)
        obstacles[33].goto(-220, -270)
        obstacles[34].goto(-240, -270)
        obstacles[35].goto(-240, -290)
        obstacles[36].goto(-260, -270)
        # OBSTACLE SETUP END!!!!----------------------------------------------

        # Playing level 3-4 soundtrack
        if soundSwitch == 0:
            LevelSound = resource_path("resources/sound/level3.mp3")
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(LevelSound))
            soundSwitch = 1

        delay = 0.09 #sets Level speed
        reduceScore = 3 #sets the penalty for hitting the snake's tail or obstacles
    elif Current_level == 3 and menuActive == 0 and retryActive != 2:
        LevelBG = 'resources/levels/level4.gif'
        # OBSTACLE SETUP!!!!--------------------------------------------------
        for obstacle in obstacles:
            obstacle.goto(1000, 1000)
        obstacles.clear()
        obstacle_count = 0
        while obstacle_count < 78:
            obstacle = RawTurtle(turtle_screen)
            obstacle.speed(0)
            obstacle.shape(obstacle_texture1)
            obstacle.penup()
            obstacle.goto(179, -70)
            obstacles.append(obstacle)
            obstacle_count += 1
        for index in range(len(obstacles) - 1, 0, -1):
            g = obstacle.xcor()
            h = obstacle.ycor()
            obstacles[index].goto(g, h)
            obstacles[index].shape(obstacle_texture1)
        obstacles[0].goto(179, -150)
        obstacles[1].goto(159, -150)
        obstacles[2].goto(139, -150)
        obstacles[3].goto(119, -150)
        obstacles[4].goto(99, -150)
        obstacles[5].goto(79, -150)
        obstacles[6].goto(59, -150)
        obstacles[7].goto(39, -150)
        obstacles[8].goto(19, -150)
        obstacles[9].goto(-1, -150)
        obstacles[10].goto(-21, -150)
        obstacles[11].goto(-41, -150)
        obstacles[12].goto(-61, -150)
        obstacles[13].goto(-81, -150)
        obstacles[14].goto(-101, -150)
        obstacles[15].goto(-121, -150)
        obstacles[16].goto(-141, -150)
        obstacles[17].goto(-161, -150)
        obstacles[18].goto(-181, -150)
        obstacles[19].goto(-181, -130)
        obstacles[77].goto(179, -130)  # 78 is here because I was really lazy to rewrite all the indexes...

        obstacles[20].goto(179, 50)
        obstacles[21].goto(159, 70)
        obstacles[22].goto(139, 70)
        obstacles[23].goto(119, 70)
        obstacles[24].goto(99, 70)
        obstacles[25].goto(79, 70)
        obstacles[26].goto(59, 70)
        obstacles[27].goto(39, 70)
        obstacles[28].goto(19, 70)
        obstacles[29].goto(-1, 70)
        obstacles[30].goto(-21, 70)
        obstacles[31].goto(-41, 70)
        obstacles[32].goto(-61, 70)
        obstacles[33].goto(-81, 70)
        obstacles[34].goto(-101, 70)
        obstacles[35].goto(-121, 70)
        obstacles[36].goto(-141, 70)
        obstacles[37].goto(-161, 70)
        obstacles[38].goto(-181, 70)
        obstacles[39].goto(-181, 50)
        obstacles[40].goto(179, 70)

        # Top right obstacle
        obstacles[41].goto(260, 190)
        obstacles[42].goto(260, 210)
        obstacles[43].goto(260, 230)
        obstacles[44].goto(240, 230)
        obstacles[45].goto(220, 230)
        obstacles[46].goto(220, 210)
        obstacles[47].goto(220, 190)
        obstacles[48].goto(240, 190)
        obstacles[49].goto(240, 210)
        # Top left obstacle
        obstacles[50].goto(-260, 210)
        obstacles[51].goto(-260, 230)
        obstacles[52].goto(-240, 230)
        obstacles[53].goto(-220, 230)
        obstacles[54].goto(-220, 210)
        obstacles[55].goto(-220, 190)
        obstacles[56].goto(-240, 190)
        obstacles[57].goto(-240, 210)
        obstacles[58].goto(-260, 190)
        # Bottom right obstacle
        obstacles[59].goto(260, -290)
        obstacles[60].goto(260, -310)
        obstacles[61].goto(240, -310)
        obstacles[62].goto(220, -310)
        obstacles[63].goto(220, -290)
        obstacles[64].goto(220, -270)
        obstacles[65].goto(240, -270)
        obstacles[66].goto(240, -290)
        obstacles[67].goto(260, -270)
        # Bottom left obstacle
        obstacles[68].goto(-260, -290)
        obstacles[69].goto(-260, -310)
        obstacles[70].goto(-240, -310)
        obstacles[71].goto(-220, -310)
        obstacles[72].goto(-220, -290)
        obstacles[73].goto(-220, -270)
        obstacles[74].goto(-240, -270)
        obstacles[75].goto(-240, -290)
        obstacles[76].goto(-260, -270)
        # OBSTACLE SETUP END!!!!----------------------------------------------

        delay = 0.08 #sets Level speed
        reduceScore = 4 #sets the penalty for hitting the snake's tail or obstacles
    turtle_screen.bgpic(resource_path(LevelBG))

#Moves food to a new location (Precisely puts the fruits inside the grids)
def movefood():
    global x
    global y
    global tail
    global tails
    x = int(random.randrange(-290, 290, 20))
    y = int(random.randrange(-280, 280, 10))
    if x % 10 == 0:
        x -= 10
    if y % 20 == 0:
        y -= 10
    fruit.goto(x, y)

#warps all tail segments to the middle
def resettailposition():
    global tail
    global tails
    for tail in tails:
        tail.goto(1000, 1000)

#Descibes what happens if player hits a wall or their tail (some stuff is different for the two, check the main loop to see)
def hit():
    global lastDirection
    pygame.mixer.Channel(2).play(pygame.mixer.Sound(hitsound))
    lastDirection = "none"
    head.direction = "stop"
    head.goto(0, -10)
    time.sleep(1)
    resettailposition()

#Shows the customization screen
def customizeScreen(a, b):
    Logo.hideturtle()
    MiniMenu.hideturtle()
    pygame.mixer.Channel(2).play(pygame.mixer.Sound(popsound))
    fruit.hideturtle()
    Exit.hideturtle()
    Start.hideturtle()
    Customize.hideturtle()
    Help.hideturtle()
    Back.showturtle()
    CustomizePage.showturtle()
    SnakeTailColor.showturtle()
    SnakeHeadColor.showturtle()

#Shows the menu/pause screen
def menuScreen(a, b):
    global menuActive
    global tail
    global tails
    global obstacles
    global obstacle
    menuActive = 1
    pygame.mixer.Channel(1).pause()
    pygame.mixer.Sound.play(popsound)
    pygame.mixer.Channel(0).unpause()
    turtle_screen.bgpic(resource_path('resources/levels/menuBG.gif'))
    pen.clear()
    if winState == False:
        pen.write("PAUSED", align="center", font=("LLPixel", 24, 'normal'))
    else:
        pen.write("PRESS START", align="center", font=("LLPixel", 24, 'normal'))
    CustomizePage.hideturtle()
    MiniMenu.hideturtle()
    SnakeTailColor.hideturtle()
    Win.hideturtle()
    head.hideturtle()
    fruit.hideturtle()
    Help2.hideturtle()
    CreditsPage.hideturtle()
    CreditsButton.hideturtle()
    HelpPage.hideturtle()
    Back.hideturtle()
    HowToPage.hideturtle()
    SnakeHeadColor.hideturtle()
    for tail in tails:
        tail.hideturtle()
    for obstacle in obstacles:
        obstacle.hideturtle()
    Mute.showturtle()
    Start.showturtle()
    Exit.showturtle()
    Customize.showturtle()
    Help.showturtle()
    Logo.showturtle()
    head.direction = "Stop"

#Shows the credits page
def creditsScreen(a, b):
    Help2.showturtle()
    pygame.mixer.Sound.play(popsound)
    HelpPage.hideturtle()
    CreditsPage.showturtle()

# Detecting if the player pressed the retry button
def retry(a, b):
    global retryActive
    pygame.mixer.Sound.play(retrysound)
    retryActive = 1
    Retry.hideturtle()

# Detecting if the player pressed the start button and doing a heck more things
def StartBT(a, b):
    global menuActive
    global tail
    global tails
    global lastDirection
    turtle_screen.bgpic(resource_path(LevelBG))
    pygame.mixer.Channel(2).play(pygame.mixer.Sound(popsound))
    pygame.mixer.Channel(0).pause()
    updategoal()
    # starting music if sound is not muted
    if muteState == 0:
        pygame.mixer.Channel(1).unpause()
        pygame.mixer.Channel(1).set_volume(0.3)
    elif muteState == 1:
        pygame.mixer.Channel(1).unpause()
        pygame.mixer.Channel(1).set_volume(0)
    head.showturtle()
    for tail in tails:
        tail.showturtle()
    for obstacle in obstacles:
        obstacle.showturtle()
    Logo.hideturtle()
    fruit.showturtle()
    Exit.hideturtle()
    Start.hideturtle()
    if winState == False:
        Start.shape(continueButton)
    Customize.hideturtle()
    Help.hideturtle()
    MiniMenu.showturtle()
    head.direction = lastDirection
    menuActive = 0

#exit button...
def ExitBT(a, b):
    pygame.mixer.Channel(0).pause()
    pygame.mixer.Channel(2).play(pygame.mixer.Sound(exitsound))
    time.sleep(3)
    main_window.destroy()

#Shows the help page
def HelpPG(a, b):
    CreditsPage.hideturtle()
    Help2.hideturtle()
    Logo.hideturtle()
    MiniMenu.hideturtle()
    pygame.mixer.Channel(2).play(pygame.mixer.Sound(popsound))
    HelpPage.showturtle()
    fruit.hideturtle()
    Exit.hideturtle()
    Start.hideturtle()
    Customize.hideturtle()
    Help.hideturtle()
    Back.showturtle()
    CreditsButton.showturtle()

#detecting if the player hates the loud music or not.. (again, volume control under windows is still kinda broken..)
def MuteON(a, b):
    global muteState
    pygame.mixer.Channel(1).set_volume(0)
    pygame.mixer.Channel(0).set_volume(0)
    Mute.hideturtle()
    MuteOFFbutton.showturtle()
    muteState = 1

def MuteOFF(a, b):
    global muteState
    pygame.mixer.Channel(1).set_volume(0.3)
    pygame.mixer.Channel(0).set_volume(0.3)
    Mute.showturtle()
    MuteOFFbutton.hideturtle()
    muteState = 0

# assigning key directions
def goup():
    global lastDirection
    if menuActive == 0:
        if head.direction != "down" and lastDirection != 'up' and lastDirection != 'down':
            head.direction = "up"

def godown():
    global lastDirection
    if menuActive == 0 and lastDirection != 'up' and lastDirection != 'down':
        if head.direction != "up":
            head.direction = "down"

def goleft():
    global lastDirection
    if menuActive == 0 and lastDirection != 'left' and lastDirection != 'right':
        if head.direction != "right":
            head.direction = "left"

def goright():
    global lastDirection
    if menuActive == 0 and lastDirection != 'left' and lastDirection != 'right':
        if head.direction != "left":
            head.direction = "right"

def move():
    global lastDirection
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
        lastDirection = "up"
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
        lastDirection = "down"
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
        lastDirection = "left"
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)
        lastDirection = "right"

def testing(x,y):
    global score
    global goal
    score = goal

# Telling turtle to listen to key presses and button clicks and perform the assigned functions
turtle_screen.listen()
head.onclick(testing)
Win.onclick(menuScreen)
Help2.onclick(HelpPG)
SnakeHeadColor.onclick(snakeHeadColor)
SnakeTailColor.onclick(snakeTailColor)
Customize.onclick(customizeScreen)
CreditsButton.onclick(creditsScreen)
Back.onclick(menuScreen)
Retry.onclick(retry)
Help.onclick(HelpPG)
Start.onclick(StartBT)
Exit.onclick(ExitBT)
Mute.onclick(MuteON)
MuteOFFbutton.onclick(MuteOFF)
MiniMenu.onclick(menuScreen)
turtle_screen.onkeypress(goup, "Up")
turtle_screen.onkeypress(godown, "Down")
turtle_screen.onkeypress(goleft, "Left")
turtle_screen.onkeypress(goright, "Right")

# Main game loop starts here
# From here on my comments are not as important.. or useful... (mainly because I'm tired... send help..) -Fuzzky
while True:
    # Updating Game screen
    turtle_screen.update()

    # Obstacle collision detection and preventing fruits from spawning on obstacles
    for obstacle in obstacles:
        if obstacle.distance(head) < 18 and head.direction != "stop" and menuActive == 0 and lastDirection != 'none':
            hit()
            score -= reduceScore
            updategoal()
        if obstacle.distance(fruit) < 18:
            movefood()

# Checking for win case
    if Current_level == 4:
        YouWin()

# Animating fruits
    animatefruit()

# Looping music
    for event in pygame.event.get():
        if event.type == GAME_SONG_END and pygame.mixer.Channel(1).get_busy() == False:
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(LevelSound))
        if event.type == MENU_SONG_END and pygame.mixer.Channel(0).get_busy() == False:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(resource_path('resources/sound/menuBG.mp3')))

# Wall collision detection
    if head.xcor() > 310 or head.xcor() < -310 or head.ycor() > 270 or head.ycor() < -350:
        hit()
        score = 0
        updategoal()

# detecting hitting food, moving new fruit to a different place on map, and adding new tail piece
    if head.distance(fruit) < 18:
        pygame.mixer.Channel(2).play(pygame.mixer.Sound(fruitsound))
        movefood()
        # Adding new tail piece
        new_tail = RawTurtle(turtle_screen)
        new_tail.speed(0)
        new_tail.shape(snake_tail)
        new_tail.penup()
        tails.append(new_tail)
        delay -= 0.001
        score += 1
        updategoal()

# Advancing to next level
    if score == goal:
        delay = 0
        pygame.mixer.Channel(2).play(pygame.mixer.Sound(nextlevelsound))
        Current_level += 1
        score = 0
        levelsetup()
        head.goto(0, -10)
        head.direction = "stop"
        lastDirection = "none"
        resettailposition()
        goal = goal + goal
        updategoal()

# Setting tails to follow head (tails pause while menu is shown)
    for index in range(len(tails) - 1, 0, -1):
        if menuActive == 0 and head.direction != 'stop':
            x = tails[index - 1].xcor()
            y = tails[index - 1].ycor()
            tails[index].goto(x, y)
            tails[index].shape(snake_tail)
    if len(tails) > 0 and menuActive == 0 and head.direction != 'stop':
        x = head.xcor()
        y = head.ycor()
        tails[0].goto(x, y)
    move()

# Checking if head collides with tail and preventing fruits from spawning on the tail
    for tail in tails:
        if tail.distance(head) < 19 and head.direction != "stop" and menuActive == 0 and lastDirection != 'none':
            hit()
            score -= reduceScore
            updategoal()
        if tail.distance(fruit) < 18:
            movefood()

# Game over case
    if score < 0:
        gameover()

    time.sleep(delay)