#!/usr/bin/env python3

# import installed libraries
import sqlite3
import config
# defines
ZERO = 0  # Just a 0, used to update databases info.

def setGameModeToZero():
    with sqlite3.connect("./databases/balldart.db") as db:
        cursor = db.cursor()

    readData = '''SELECT id FROM games;'''
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

    with sqlite3.connect("./databases/balldart.db") as db:
        cursor = db.cursor()

    readData = '''SELECT mode FROM games;'''
    cursor.execute(readData)
    gameInfo = cursor.fetchall()
    if gameInfo[0][0] == 0:
        config.gameModeCase = NO_GAME
    elif gameInfo[0][0] == 1:
        config.gameModeCase = SINGLE_PLAYER
    elif gameInfo[0][0] == 2:
        config.gameModeCase = MULTI_PLAYER

    return config.gameModeCase

def updateInfo(points, activePlayer):
    with sqlite3.connect("./databases/balldart.db") as db:
        cursor = db.cursor()

    readData = '''SELECT id FROM games;'''
    cursor.execute(readData)
    gameInfo = cursor.fetchall()
    primaryKey = gameInfo[0][0]
    if activePlayer == 1:
        updateData = '''UPDATE games SET pointsOne = ?, activePlayer = ? WHERE id = ?'''
        data = (points, activePlayer, primaryKey)
    elif activePlayer == 2:
        updateData = '''UPDATE games SET pointsTwo = ?, activePlayer = ? WHERE id = ?'''
        data = (points, activePlayer, primaryKey)

    cursor.execute(updateData, data)
    db.commit()

def updateEmployees(uidTag):
    with sqlite3.connect("./databases/balldart.db") as db:
        cursor = db.cursor()

    readData = '''SELECT id FROM employees WHERE id = ?'''
    cursor.execute(readData, [uidTag])
    databaseInfo = cursor.fetchall()
    if len(databaseInfo) != 0:
        if int(databaseInfo[0][0]) == int(uidTag):
            active = 1
        else:
            active = 0
        insertData = '''UPDATE employees SET active = ?, led = ?, servo = ? WHERE id = ?'''
        row = (active, 0, 0, int(uidTag))
        cursor.execute(insertData, row)
        db.commit()

def updateRuntime(toAddRuntime):
    with sqlite3.connect("./databases/balldart.db") as db:
        cursor = db.cursor()
    readData = '''SELECT runtimeSystemInSec FROM employees;'''
    cursor.execute(readData)
    runTimeInfo = cursor.fetchall()
    newRuntime = (runTimeInfo[0][0] + toAddRuntime)
    updateData = '''UPDATE employees SET  runtimeSystemInSec = ? WHERE id = ?'''
    data = (newRuntime, 154162618071)
    cursor.execute(updateData, data)
    db.commit()

def updateRuntimeServo(toAddRuntime):
    with sqlite3.connect("./databases/balldart.db") as db:
        cursor = db.cursor()
    readData = '''SELECT runtimeServoInSec FROM employees;'''
    cursor.execute(readData)
    runTimeInfo = cursor.fetchall()
    newRuntime = (runTimeInfo[0][0] + toAddRuntime)
    updateData = '''UPDATE employees SET  runtimeServoInSec = ? WHERE id = ?'''
    data = (newRuntime, 154162618071)
    cursor.execute(updateData, data)
    db.commit()