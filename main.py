#!/usr/bin/env python3

#import installed libraries
import time
import timeit
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
CHECK_WINNER = 6
END_GAME = 7

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
run = 0
stop = 0
points = [[0,0,0],
          [0,0,0]]
runTimeGame = [0,0,0]
roundTime = [0,0,0]
runTimeServo = 0

numberOfRounds = MULTI_PLAYER_ROUNDS
distance = MIN_DISTANCE
gameCase = GEN_SEQUENCE
gameModeCase = 0

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



# Create NeoPixel object with appropriate configuration.
strip = PixelStrip(NUMBER_OF_BOARD_PANELS + 1, C.L_PIN, C.L_HZ, C.L_DMA, C.L_INVERT, C.L_BRIGHTNESS, C.L_CHANNEL)
# Initialize the library (must be called once before other functions).
strip.begin()

if gameModeCase == MULTI_PLAYER:
    WS2812.setCurrentPlayer(NUMBER_OF_BOARD_PANELS, strip, player)

SQL.setGameModeToZero()

RFID = threading.Thread(target = rfid.main)
RFID.start()

try:
    while True:
        if gameModeCase == NO_GAME:
            gameModeCase = SQL.checkGameMode()
            sequence.clear()
            cleanPoints()
            numberOfRounds = MULTI_PLAYER_ROUNDS
            gameCase = INIT
            if SQL.getTestData()[0] == 0:
                WS2812.rainbow(strip)
            servo.setBoardCenter()

        elif gameModeCase == SINGLE_PLAYER:
            if gameCase == INIT:
                WS2812.colorWipe(strip)
                servo.setBoardCenter()
                time.sleep(2)
                runTimeGame[0] = timeit.default_timer()
                gameNumber = SQL.nextGameNumber()
                gameCase = GEN_SEQUENCE

            elif gameCase == GEN_SEQUENCE:
                gameModeCase = SQL.checkGameMode()
                sequence, randomPanel = addToSequence(previousRandomNumber)                         # Add random number (1 t/m 6) to sequence.
                previousRandomNumber = randomPanel                                                  # Prevents generating the same number.
                gameCase = SHOW_SEQUENCE

            elif gameCase == SHOW_SEQUENCE:
                WS2812.showSequence(strip, sequence, SEQUENCE_LED_ON_TIME, SEQUENCE_LED_OFF_TIME)   # Show sequence to the player.
                panelDetection.clearInterrupts()                                                    # Clears the interrupts in case someone hit a panel during SHOW_SEQUENCE.
                roundTime[0] = timeit.default_timer()                                               # Get time now.
                gameCase = DETECT_SEQUENCE

            elif gameCase == DETECT_SEQUENCE:

                gameModeCase = SQL.checkGameMode()                                                  # To be able to stop halfway.
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
                roundTime[1] = timeit.default_timer()                                               # get time now.
                roundTime[2] = int(roundTime[1] - roundTime[0])                                     # Time a sequence takes.
                print (roundTime[2])
                SQL.pushGameStats(gameNumber, player, 0, int(len(sequence)), roundTime[2])          # Push stats off round to the database.
                SQL.updateRuntime(runTimeGame[2])                                                   # Update Total game time.
                time.sleep(3)
                gameCase = GEN_SEQUENCE                                                             # If the sequence was correct, add one to the sequence.

            elif gameCase == WRONG_SEQUENCE:
                score = len(sequence) - 1
                SQL.updateInfo(score, gameModeCase)
                SQL.setGameModeToZero()
                print("Incorrect! jammer joh... score= %d\n" % score)
                sequence.clear()                                                                    # Clear array.
                WS2812.showWrongSequence(NUMBER_OF_BOARD_PANELS, strip)                             # Show blinking red LEDs.
                runTimeGame[1] = timeit.default_timer()                                             # Get time now.
                runTimeGame[2] = int(runTimeGame[1] - runTimeGame[0])                               # Calculate time of game.
                SQL.updateRuntime(runTimeGame[2])                                                   # Update Total game time.
                gameModeCase = NO_GAME


        elif gameModeCase == MULTI_PLAYER:

            if gameCase == INIT:
                player = True
                WS2812.colorWipe(strip)
                WS2812.setCurrentPlayer(NUMBER_OF_BOARD_PANELS, strip, player)
                servo.setBoardCenter()
                time.sleep(2)
                runTimeGame[0] = timeit.default_timer()                                             # Save time start game.
                gameNumber = SQL.nextGameNumber()                                                   # Get next record for database.
                gameCase = GEN_SEQUENCE                                                             # Continue.

            elif gameCase == GEN_SEQUENCE:
                gameModeCase = SQL.checkGameMode()
                sequence, randomPanel = addToSequence(previousRandomNumber)                         # Add random number (1 t/m 6) to sequence.
                previousRandomNumber = randomPanel                                                  # Prevents generating the same number.
                gameCase = SHOW_SEQUENCE

            elif gameCase == SHOW_SEQUENCE:
                gameModeCase = SQL.checkGameMode()
                WS2812.showSequence(strip, sequence, SEQUENCE_LED_ON_TIME, SEQUENCE_LED_OFF_TIME)   # Show sequence to the player.
                panelDetection.clearInterrupts()                                                    # Clears the interrupts in case someone hit a panel during SHOW_SEQUENCE.
                roundTime[0] = timeit.default_timer()                                               # Get time now.
                gameCase = DETECT_SEQUENCE

            elif gameCase == DETECT_SEQUENCE:
                runTimeServo = servo.timerServo()
                gameModeCase = SQL.checkGameMode()
                waitIfPlayerTooClose(NUMBER_OF_BOARD_PANELS, strip, MIN_DISTANCE)
                servo.rotateBoard(gyro.main())                                                      # Rotate the board.
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
                    points[0][numberOfRounds - 1] = len(sequence)                                   # Push point of that round.
                    SQL.updateInfo(sum(points[0]), 1)                                               # And push overall to database.
                    roundTime[1] = timeit.default_timer()                                           # get time now.
                    roundTime[2] = int(roundTime[1] - roundTime[0])                                 # Time a sequence takes.
                    SQL.pushGameStats(gameNumber, player,                                           # Push stats of round to
                                      numberOfRounds, int(len(sequence)),                           # databases
                                      roundTime[2])
                    SQL.updateRuntimeServo(runTimeServo)                                            # Update run time of servo.

                else:
                    points[1][numberOfRounds - 1] = len(sequence)                                   # Push point of that round.
                    SQL.updateInfo(sum(points[1]), 2)                                               # And push overall to database.
                    roundTime[1] = timeit.default_timer()                                           # get time now.
                    roundTime[2] = int(roundTime[1] - roundTime[0])                                 # Time a sequence takes.
                    SQL.pushGameStats(gameNumber, player,                                           # Push stats of round to
                                      numberOfRounds, int(len(sequence)),                           # database.
                                      roundTime[2])
                    SQL.updateRuntimeServo(runTimeServo)                                            # Update run time of servo.

                time.sleep(3)
                gameCase = GEN_SEQUENCE                                                             # If the sequence was correct, add one to the sequence.

            elif gameCase == WRONG_SEQUENCE:
                gameModeCase = SQL.checkGameMode()                                                  # To be able to stop halfway.
                servo.setBoardCenter()                                                              # Servo back to center.
                if not player:
                   numberOfRounds = numberOfRounds - 1                                              # Next round.

                WS2812.showWrongSequence(NUMBER_OF_BOARD_PANELS, strip)                             # Show blinking red LEDs.
                sequence.clear()                                                                    # Clear the array.

                if numberOfRounds == 0:
                    gameCase = CHECK_WINNER                                                         # Show the winner if there are no more rounds to play.
                else:
                    gameCase = GEN_SEQUENCE                                                         # If the sequence was incorrect, generate new sequence.
                    player ^= 1
                    print("player= %d\n" % player)
                    WS2812.setCurrentPlayer(NUMBER_OF_BOARD_PANELS, strip, player)

            elif gameCase == CHECK_WINNER:

                if sum(points[0]) == sum(points[1]):                                                 # if there is a tie
                    gameCase = GEN_SEQUENCE                                                          # there will be an extra round.
                    numberOfRounds = 1
                    player ^= 1
                    WS2812.setCurrentPlayer(NUMBER_OF_BOARD_PANELS, strip, player)
                else:
                    gameCase = END_GAME                                                             # Else quit the game.

            elif gameCase == END_GAME:                                                              # Show the winner.
                if sum(points[0]) > sum(points[1]):
                    WS2812.showWinnerPlayer1(NUMBER_OF_BOARD_PANELS + 1, strip)
                if sum(points[0]) < sum(points[1]):
                    WS2812.showWinnerPlayer2(NUMBER_OF_BOARD_PANELS + 1, strip)

                runTimeGame[1] = timeit.default_timer()                                             # Get stop time game.
                runTimeGame[2] = int(runTimeGame[1] - runTimeGame[0])                               # Calculate runtime
                SQL.updateRuntime(runTimeGame[2])                                                   # and push that
                SQL.updateRuntimeServo(runTimeServo)                                                # same for servo.

                time.sleep(10)                                                                      # Show the winner for 10 sec.
                SQL.setGameModeToZero()                                                             # Reset everthing.
                gameModeCase = NO_GAME                                                              # Jump back op.

except KeyboardInterrupt:
    GPIO.cleanup()                                                                                  # Clean up GPIO on CTRL+C exit.
    WS2812.colorWipe(strip)                                                                         # Turn the LED`s of