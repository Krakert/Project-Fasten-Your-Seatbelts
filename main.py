#!/usr/bin/env python3

#import installed libraries
import time
from rpi_ws281x import PixelStrip, Color
import RPi.GPIO as GPIO
import random

#import files from our own project
import panelDetection
import WS2812
import servo
import gyro
import Sonar

#defines
NUMBER_OF_BOARD_PANELS = 6
SEQUENCE_LED_ON_TIME = 1 #seconds
SEQUENCE_LED_OFF_TIME = 0.3 #seconds
MIN_DISTANCE = 50 #distance in cm
MULTI_PLAYER_ROUNDS = 3 # number of rounds played in multiplayer
CORRECT_SEQUENCE = 50
INVALID_SEQUENCE = 51
SHOW_HIT_ON_TIME = 0.2 # time in seconds

#enumeratie of 'switch case singleplayer'
#gameCase
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
player1score = 0
player2score = 0
numberOfRounds = MULTI_PLAYER_ROUNDS
distance = MIN_DISTANCE
gameCase = GEN_SEQUENCE
gameModeCase = MULTI_PLAYER # dit moet dus weg en vervangen worden door in de main loop uit de database de gamemodus op te halen!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# LED strip configuration:
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


def addToSequence(previousRandomNumber):
    global sequence

    randomPanel = random.randrange(1, NUMBER_OF_BOARD_PANELS + 1)

    while randomPanel == previousRandomNumber:
        randomPanel = random.randrange(1, NUMBER_OF_BOARD_PANELS + 1)

    print('new number: %d' % (randomPanel))
    sequence.append(randomPanel)

    return sequence, randomPanel

def waitIfPlayerTooClose(NUMBER_OF_BOARD_PANELS, strip, MIN_DISTANCE):
    global distance

    distance = (distance * 0.9) + (Sonar.distance() * 0.1)
    while WS2812.checkPlayerTooClose(NUMBER_OF_BOARD_PANELS, strip, distance, MIN_DISTANCE):
        distance = (distance * 0.9) + (Sonar.distance() * 0.1)
        panelDetection.clearInterrupts()


# Create NeoPixel object with appropriate configuration.
strip = PixelStrip(NUMBER_OF_BOARD_PANELS + 1, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

if gameModeCase == MULTI_PLAYER:
    WS2812.setCurrentPlayer(NUMBER_OF_BOARD_PANELS, strip, player)

try:
    while True:
        #get gamemode from database!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

###############################################################################################################################################################################################
        if gameModeCase == NO_GAME:
            sequence.clear()                                             # clear array
            player1score = 0
            player2score = 0
            numberOfRounds = MULTI_PLAYER_ROUNDS
            gameCase = GEN_SEQUENCE
            WS2812.rainbow(strip)


###############################################################################################################################################################################################
        if gameModeCase == SINGLE_PLAYER:
            if gameCase == GEN_SEQUENCE:
                sequence, randomPanel = addToSequence(previousRandomNumber)  # add random number (1 t/m 6) to sequence
                previousRandomNumber = randomPanel                              # prevents generating the same number
                gameCase = SHOW_SEQUENCE

            if gameCase == SHOW_SEQUENCE:
                WS2812.showSequence(strip, sequence, SEQUENCE_LED_ON_TIME, SEQUENCE_LED_OFF_TIME)                                       # show sequence to the player
                panelDetection.clearInterrupts()                                # clears the interrupts in case someone hit a panel during SHOW_SEQUENCE
                gameCase = DETECT_SEQUENCE

            if gameCase == DETECT_SEQUENCE:
                waitIfPlayerTooClose(NUMBER_OF_BOARD_PANELS, strip, MIN_DISTANCE)

                valid = panelDetection.guessSequence(sequence, CORRECT_SEQUENCE, INVALID_SEQUENCE)               # returns 1 if the sequence was correct, 2 if incorrect

                if valid == CORRECT_SEQUENCE:
                    gameCase = SHOW_CORRECT_SEQUENCE
                elif valid == INVALID_SEQUENCE:
                    gameCase = WRONG_SEQUENCE
                elif valid != 0:
                    WS2812.showPanelHit(strip, valid, SHOW_HIT_ON_TIME)

            if gameCase == SHOW_CORRECT_SEQUENCE:
                print("Correct!\n")
                WS2812.showCorrectSequence(NUMBER_OF_BOARD_PANELS, strip)
                time.sleep(3)                                                   # Needs fixing, dont use the sleep fuction!
                gameCase = GEN_SEQUENCE                                 # if the sequence was correct, add one to the sequence

            if gameCase == WRONG_SEQUENCE:
                score = len(sequence) - 1
                #send score to database !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                print("Incorrect! jammer joh... score= %d\n" %(score))
                sequence.clear()                                             # clear array
                WS2812.showWrongSequence(NUMBER_OF_BOARD_PANELS, strip)         # show blinking red LEDs                    
                gameCase = GEN_SEQUENCE                                             # if the sequence was incorrect, generate new sequence


###############################################################################################################################################################################################
        if gameModeCase == MULTI_PLAYER:
            if gameCase == GEN_SEQUENCE:
                sequence, randomPanel = addToSequence(previousRandomNumber)  # add random number (1 t/m 6) to sequence
                previousRandomNumber = randomPanel                              # prevents generating the same number
                gameCase = SHOW_SEQUENCE

            if gameCase == SHOW_SEQUENCE:
                WS2812.showSequence(strip, sequence, SEQUENCE_LED_ON_TIME, SEQUENCE_LED_OFF_TIME)                                       # show sequence to the player
                panelDetection.clearInterrupts()                                # clears the interrupts in case someone hit a panel during SHOW_SEQUENCE
                gameCase = DETECT_SEQUENCE

            if gameCase == DETECT_SEQUENCE:
                waitIfPlayerTooClose(NUMBER_OF_BOARD_PANELS, strip, MIN_DISTANCE)

                servo.rotateBoard(gyro.main())

                valid = panelDetection.guessSequence(sequence, CORRECT_SEQUENCE, INVALID_SEQUENCE)               # returns 1 if the sequence was correct, 2 if incorrect

                if valid == CORRECT_SEQUENCE:
                    gameCase = SHOW_CORRECT_SEQUENCE
                elif valid == INVALID_SEQUENCE:
                    gameCase = WRONG_SEQUENCE
                elif valid != 0:
                    WS2812.showPanelHit(strip, valid, SHOW_HIT_ON_TIME)

            if gameCase == SHOW_CORRECT_SEQUENCE:
                print("Correct!\n")
                servo.setBoardCenter()
                WS2812.showCorrectSequence(NUMBER_OF_BOARD_PANELS, strip)
                time.sleep(3)                                                   # Needs fixing, dont use the sleep fuction!
                gameCase = GEN_SEQUENCE                                         # if the sequence was correct, add one to the sequence

            if gameCase == WRONG_SEQUENCE:
                servo.setBoardCenter()
                if player == True:
                    player1score = player1score + (len(sequence) - 1)
                    print("Incorrect player1! jammer joh... score= %d\n" %(player1score))
                    
                else:
                    player2score = player2score + (len(sequence) - 1)
                    print("Incorrect player2! jammer joh... score= %d\n" %(player2score))
                    numberOfRounds = numberOfRounds - 1

                WS2812.showWrongSequence(NUMBER_OF_BOARD_PANELS, strip)         # show blinking red LEDs     
                sequence.clear()  

                if numberOfRounds == 0:
                    gameCase = SHOW_WINNER                                      # show the winner if there are no more rounds to play
                else:               
                    gameCase = GEN_SEQUENCE                                     # if the sequence was incorrect, generate new sequence
                    player ^= 1
                    print("player= %d\n" %(player)) 
                    WS2812.setCurrentPlayer(NUMBER_OF_BOARD_PANELS, strip, player)
                
            if gameCase == SHOW_WINNER:
                #if there is a tie there will be an extra round
                if player1score == player2score:
                    gameCase = GEN_SEQUENCE
                    numberOfRounds = 1
                    player ^= 1
                    WS2812.setCurrentPlayer(NUMBER_OF_BOARD_PANELS, strip, player)
                
                #show the winner    
                if player1score > player2score:
                    WS2812.showWinnerPlayer1(NUMBER_OF_BOARD_PANELS + 1, strip)
                if player1score < player2score:
                    WS2812.showWinnerPlayer2(NUMBER_OF_BOARD_PANELS + 1, strip)
                


except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
    WS2812.colorWipe(strip)
