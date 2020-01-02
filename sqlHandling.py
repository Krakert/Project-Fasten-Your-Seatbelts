#!/usr/bin/env python3

#import installed libraries
import sqlite3

#defines
ZERO = 0                        # Just a 0, used to update databases info.

def setupConnection():
    global cursor
    global db
    with sqlite3.connect("./databases/balldart.db") as db:
        cursor = db.cursor()
    print("Database connected")

def setGameModeToZero():
    readData = '''SELECT * FROM games;'''
    cursor.execute(readData)
    gameInfo = cursor.fetchall()
    primaryKey = gameInfo[0][0]
    updateData = '''UPDATE games SET mode = ?, round = ?, pointsOne = ?, pointstwo = ?, activePlayer = ? 
                                 WHERE id = ?'''
    data = (ZERO, ZERO, ZERO, ZERO, ZERO, primaryKey)
    cursor.execute(updateData, data)
    db.commit()

def checkGameMode():
    # defines
    NO_GAME = 0
    SINGLE_PLAYER = 1
    MULTI_PLAYER = 2

    readData = '''SELECT mode FROM games;'''
    cursor.execute(readData)
    gameInfo = cursor.fetchall()
    if gameInfo[0][0] == 0:
        gameModeCase = NO_GAME
    elif gameInfo[0][0] == 1:
        gameModeCase = SINGLE_PLAYER
    elif gameInfo[0][0] == 2:
        gameModeCase = MULTI_PLAYER

    return gameModeCase

def updateInfo(pointPlayerOne, pointPlayerTwo, activePlayer):
    readData = '''SELECT * FROM games;'''
    cursor.execute(readData)
    gameInfo = cursor.fetchall()
    primaryKey = gameInfo[0][0]
    if activePlayer == 1:
        updateData = '''UPDATE games SET pointsOne = ?, activePlayer = ? WHERE id = ?'''
        data = (pointPlayerOne, activePlayer, primaryKey)
    elif activePlayer == 2:
        updateData = '''UPDATE games SET pointsTwo = ?, activePlayer = ? WHERE id = ?'''
        data = (pointPlayerTwo, activePlayer, primaryKey)

    cursor.execute(updateData, data)
    db.commit()

    readData = '''SELECT * FROM games;'''
    cursor.execute(readData)
    gameInfo = cursor.fetchall()
    print(gameInfo)