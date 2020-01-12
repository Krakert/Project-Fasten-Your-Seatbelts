#!/usr/bin/env python3

#import installed libraries
import time
from rpi_ws281x import PixelStrip, Color
import RPi.GPIO as GPIO
import random
import threading

#import files from our own project
import panelDetection
import WS2812
import servo
import gyro
import sonar
import sqlHandling as SQL
import rfid
import config as C

#defines
NUMBER_OF_BOARD_PANELS = 6
SEQUENCE_LED_ON_TIME = 1        #seconds
SEQUENCE_LED_OFF_TIME = 0.3     #seconds
MIN_DISTANCE = 65               #distance in cm
MULTI_PLAYER_ROUNDS = 3         # number of rounds played in multiplayer
CORRECT_SEQUENCE = 50
INVALID_SEQUENCE = 51
SHOW_HIT_ON_TIME = 0.2          # time in seconds

#enumeratie of 'switch case singleplayer'
#gameCase
INIT = 0
GEN_SEQUENCE = 1
SHOW_SEQUENCE = 2
DETECT_SEQUENCE = 3
SHOW_CORRECT_SEQUENCE = 4
WRONG_SEQUENCE = 5
SHOW_WINNER = 6


#enumernatie of 'main switch case'
#gameModeCase
NO_GAME = 0
SINGLE_PLAYER = 1
MULTI_PLAYER = 2

#variables
sequence = []
sequenseSize = 0
previousRandomNumber = 0
player = True

points = [[0,0,0],
          [0,0,0]]

runtime = [[0,0,0],                                                                                 # Timer for total game time and
           [0,0,0]]                                                                                 # time the servo had turned.

numberOfRounds = MULTI_PLAYER_ROUNDS
distance = MIN_DISTANCE
gameCase = GEN_SEQUENCE
gameModeCase = 0

run = 0
gameStartTime = 0
totalGameTime = 0


def addToSequence(previousRandomNumber):
    global sequence

    randomPanel = random.randrange(1, NUMBER_OF_BOARD_PANELS + 1)

    while randomPanel == previousRandomNumber:
        randomPanel = random.randrange(1, NUMBER_OF_BOARD_PANELS + 1)

    print('new number: %d' % randomPanel)
    sequence.append(randomPanel)

    return sequence, randomPanel

def waitIfPlayerTooClose(NUMBER_OF_BOARD_PANELS, strip, MIN_DISTANCE):
    global distance

    distance = (distance * 0.9) + (sonar.distance() * 0.1)
    while WS2812.checkPlayerTooClose(NUMBER_OF_BOARD_PANELS, strip, distance, MIN_DISTANCE):
        distance = (distance * 0.9) + (sonar.distance() * 0.1)
        panelDetection.clearInterrupts()

def cleanPoints():
    for i in range(len(points)):
        for x in range(len(points[i])):
            points[i][x] = 0

def timers(clock):
    global timeNow
    if time.time() - timeNow > 1:
        runtime[clock][2] = runtime[0][2] + 1
        #print ("Runtime of the servo %d" % totalGameTime)
        timeNow = time.time()
    if runtime[clock][2] == 60:
        runtime[clock][1] = runtime[clock][1] + 1
        runtime[clock][2] = 0
    if runtime[clock][1] == 60:
        runtime[clock][0] = runtime[clock][0] + 1
        runtime[clock][1] = 0

# Create NeoPixel object with appropriate configuration.
strip = PixelStrip(NUMBER_OF_BOARD_PANELS + 1, C.L_PIN, C.L_HZ, C.L_DMA, C.L_INVERT, C.L_BRIGHTNESS, C.L_CHANNEL)
# Initialize the library (must be called once before other functions).
strip.begin()

if gameModeCase == MULTI_PLAYER:
    WS2812.setCurrentPlayer(NUMBER_OF_BOARD_PANELS, strip, player)

SQL.setGameModeToZero()

RFID = threading.Thread(target = rfid.main)
RFID.start()

timeNow = time.time()

try:
    while True:
        if gameModeCase == NO_GAME:
            gameModeCase = SQL.checkGameMode()
            sequence.clear()
            cleanPoints()
            numberOfRounds = MULTI_PLAYER_ROUNDS
            gameCase = INIT
            WS2812.rainbow(strip)
            servo.setBoardCenter()

        elif gameModeCase == SINGLE_PLAYER:
            if gameCase == INIT:
                WS2812.colorWipe(strip)
                servo.setBoardCenter()
                time.sleep(2)
                gameCase = GEN_SEQUENCE

            elif gameCase == GEN_SEQUENCE:
                gameModeCase = SQL.checkGameMode()
                sequence, randomPanel = addToSequence(previousRandomNumber)                         # Add random number (1 t/m 6) to sequence.
                previousRandomNumber = randomPanel                                                  # Prevents generating the same number.
                gameCase = SHOW_SEQUENCE

            elif gameCase == SHOW_SEQUENCE:
                gameModeCase = SQL.checkGameMode()
                WS2812.showSequence(strip, sequence, SEQUENCE_LED_ON_TIME, SEQUENCE_LED_OFF_TIME)   # Show sequence to the player.
                panelDetection.clearInterrupts()                                                    # Clears the interrupts in case someone hit a panel during SHOW_SEQUENCE.
                gameCase = DETECT_SEQUENCE

            elif gameCase == DETECT_SEQUENCE:
                gameModeCase = SQL.checkGameMode()
                waitIfPlayerTooClose(NUMBER_OF_BOARD_PANELS, strip, MIN_DISTANCE)

                valid = panelDetection.guessSequence(sequence, CORRECT_SEQUENCE, INVALID_SEQUENCE)  # Returns 1 if the sequence was correct, 2 if incorrect.

                if valid == CORRECT_SEQUENCE:
                    gameCase = SHOW_CORRECT_SEQUENCE
                elif valid == INVALID_SEQUENCE:
                    gameCase = WRONG_SEQUENCE
                elif valid != 0:
                    WS2812.showPanelHit(strip, valid, SHOW_HIT_ON_TIME)

            elif gameCase == SHOW_CORRECT_SEQUENCE:
                print("Correct!\n")
                score = len(sequence)
                SQL.updateInfo(score, gameModeCase)
                WS2812.showCorrectSequence(NUMBER_OF_BOARD_PANELS, strip)
                time.sleep(3)
                gameCase = GEN_SEQUENCE                                                             # If the sequence was correct, add one to the sequence.

            elif gameCase == WRONG_SEQUENCE:
                score = len(sequence) - 1
                SQL.updateInfo(score, gameModeCase)
                SQL.setGameModeToZero()
                print("Incorrect! jammer joh... score= %d\n" % score)
                sequence.clear()                                                                    # Clear array.
                WS2812.showWrongSequence(NUMBER_OF_BOARD_PANELS, strip)                             # Show blinking red LEDs.
                gameModeCase = NO_GAME


        elif gameModeCase == MULTI_PLAYER:

            if gameCase == INIT:
                player = True
                WS2812.colorWipe(strip)
                WS2812.setCurrentPlayer(NUMBER_OF_BOARD_PANELS, strip, player)
                servo.setBoardCenter()
                time.sleep(2)
                gameCase = GEN_SEQUENCE

            elif gameCase == GEN_SEQUENCE:
                gameModeCase = SQL.checkGameMode()
                sequence, randomPanel = addToSequence(previousRandomNumber)                         # Add random number (1 t/m 6) to sequence.
                previousRandomNumber = randomPanel                                                  # Prevents generating the same number.
                gameCase = SHOW_SEQUENCE

            elif gameCase == SHOW_SEQUENCE:
                gameModeCase = SQL.checkGameMode()
                WS2812.showSequence(strip, sequence, SEQUENCE_LED_ON_TIME, SEQUENCE_LED_OFF_TIME)   # Show sequence to the player.
                panelDetection.clearInterrupts()                                                    # Clears the interrupts in case someone hit a panel during SHOW_SEQUENCE.
                gameCase = DETECT_SEQUENCE

            elif gameCase == DETECT_SEQUENCE:
                timers()
                gameModeCase = SQL.checkGameMode()
                waitIfPlayerTooClose(NUMBER_OF_BOARD_PANELS, strip, MIN_DISTANCE)
                servo.rotateBoard(gyro.main())
                valid = panelDetection.guessSequence(sequence, CORRECT_SEQUENCE, INVALID_SEQUENCE)  # Returns 1 if the sequence was correct, 2 if incorrect.

                if valid == CORRECT_SEQUENCE:
                    gameCase = SHOW_CORRECT_SEQUENCE
                elif valid == INVALID_SEQUENCE:
                    gameCase = WRONG_SEQUENCE
                elif valid != 0:
                    WS2812.showPanelHit(strip, valid, SHOW_HIT_ON_TIME)

            elif gameCase == SHOW_CORRECT_SEQUENCE:
                print("Correct!\n")
                servo.setBoardCenter()
                WS2812.showCorrectSequence(NUMBER_OF_BOARD_PANELS, strip)
                if player:
                    points[0][numberOfRounds - 1] = len(sequence)
                    SQL.updateInfo(sum(points[0]), 1)
                else:
                    points[1][numberOfRounds - 1] = len(sequence)
                    SQL.updateInfo(sum(points[1]), 2)
                time.sleep(3)
                gameCase = GEN_SEQUENCE                                                             # If the sequence was correct, add one to the sequence.

            elif gameCase == WRONG_SEQUENCE:
                gameModeCase = SQL.checkGameMode()
                servo.setBoardCenter()
                if not player:
                   numberOfRounds = numberOfRounds - 1

                WS2812.showWrongSequence(NUMBER_OF_BOARD_PANELS, strip)                             # Show blinking red LEDs.
                sequence.clear()

                if numberOfRounds == 1:
                    gameCase = SHOW_WINNER                                                          # Show the winner if there are no more rounds to play.
                else:
                    gameCase = GEN_SEQUENCE                                                         # If the sequence was incorrect, generate new sequence.
                    player ^= 1
                    print("player= %d\n" % player)
                    WS2812.setCurrentPlayer(NUMBER_OF_BOARD_PANELS, strip, player)

            elif gameCase == SHOW_WINNER:
                #if there is a tie there will be an extra round
                if sum(points[0]) == sum(points[1]):
                    gameCase = GEN_SEQUENCE
                    numberOfRounds = 1
                    player ^= 1
                    WS2812.setCurrentPlayer(NUMBER_OF_BOARD_PANELS, strip, player)

                #show the winner
                if sum(points[0]) > sum(points[1]):
                    WS2812.showWinnerPlayer1(NUMBER_OF_BOARD_PANELS + 1, strip)
                if sum(points[0]) < sum(points[1]):
                    WS2812.showWinnerPlayer2(NUMBER_OF_BOARD_PANELS + 1, strip)
                time.sleep(10)
                SQL.setGameModeToZero()
                gameModeCase = NO_GAME

except KeyboardInterrupt:
    GPIO.cleanup()                                                                                  # Clean up GPIO on CTRL+C exit.
    WS2812.colorWipe(strip)                                                                         # Turn the LED`s of