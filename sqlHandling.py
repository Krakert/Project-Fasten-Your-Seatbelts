#!/usr/bin/env python3

#import installed libraries
import sqlite3

#defines
ZERO = 0                        # Just a 0, used to update databases info.

def setGameModeToZero():
    with sqlite3.connect("./databases/balldart.db") as db:
        cursor = db.cursor()
    readData = '''SELECT * FROM games;'''
    cursor.execute(readData)
    gameInfo = cursor.fetchall()
    primaryKey = gameInfo[0][0]
    updateDate = '''UPDATE games SET mode = ?, round = ?, pointsOne = ?, pointstwo = ?, activePlayer = ? 
                                 WHERE id = ?'''
    cursor.execute(updateDate, (ZERO, ZERO, ZERO, ZERO, ZERO, primaryKey))
    db.commit()

def checkGameMode():
    # defines
    NO_GAME = 0
    SINGLE_PLAYER = 1
    MULTI_PLAYER = 2
    with sqlite3.connect("./databases/balldart.db") as db:
        cursor = db.cursor()
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
