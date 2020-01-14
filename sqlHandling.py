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
    updateData = '''UPDATE games SET round = ?, activePlayer = ? WHERE id = ?'''
    data = (ZERO, ZERO, primaryKey)
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

def updateActivePlayer(player):
    with sqlite3.connect("./databases/balldart.db") as db:
        cursor = db.cursor()
    updateData = '''UPDATE games SET activePlayer = ? WHERE id = ?'''
    data = (player,  "board1")
    cursor.execute(updateData, data)
    db.commit()

def updateScore(activePlayer):
    with sqlite3.connect("./databases/balldart.db") as db:
        cursor = db.cursor()

    readData = '''SELECT pointsOne, pointsTwo FROM games;'''
    cursor.execute(readData)
    gameInfo = cursor.fetchall()
    if activePlayer == 1:
        updateData = '''UPDATE games SET pointsOne = ? WHERE id = ?'''
        data = ((gameInfo[0][0] + 1),  "board1")
    elif activePlayer == 2:
        updateData = '''UPDATE games SET pointsTwo = ? WHERE id = ?'''
        data = ((gameInfo[0][1] + 1), "board1")

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

def nextGameNumber():
    with sqlite3.connect("./databases/balldart.db") as db:
        cursor = db.cursor()
    readData = '''SELECT MAX(game_number) FROM gamestat;'''
    cursor.execute(readData)
    lastUnmber = cursor.fetchall()
    nextNumber = int(lastUnmber[0][0]) + 1

    return nextNumber

def pushGameStats(gameNumber, player, round, sequenceLength, timeInSec):
    with sqlite3.connect("./databases/balldart.db") as db:
        cursor = db.cursor()
    insertData = '''INSERT INTO gamestat (game_number, player, round, sequenceLength, timeInSec)
                    VALUES (?,?,?,?,?)'''
    Data = (gameNumber, player, round, sequenceLength, timeInSec)
    cursor.execute(insertData, Data)
    db.commit()

def resetTimeServo():
    with sqlite3.connect("./databases/balldart.db") as db:
        cursor = db.cursor()

    updateData = '''UPDATE employees SET  runtimeServoInSec = ? WHERE id = ?'''
    data = (0, 154162618071)
    cursor.execute(updateData, data)
    db.commit()

def setTestToZero():
    with sqlite3.connect("./databases/balldart.db") as db:
        cursor = db.cursor()

    updateData = '''UPDATE employees SET led = ?, servo = ? WHERE id = ?'''
    data = (0, 0, 154162618071)
    cursor.execute(updateData, data)
    db.commit()

def setEmployeesToZero():
    with sqlite3.connect("./databases/balldart.db") as db:
        cursor = db.cursor()

    updateData = '''UPDATE employees SET active = ?, led = ?, servo = ? WHERE id = ?'''
    data = (0, 0, 0, 154162618071)
    cursor.execute(updateData, data)
    db.commit()

def checkEmployees():
    with sqlite3.connect("./databases/balldart.db") as db:
        cursor = db.cursor()
    readData = '''SELECT active FROM employees;'''
    cursor.execute(readData)
    Data = cursor.fetchall()

    return int(Data[0][0])


def getTestData():
    with sqlite3.connect("./databases/balldart.db") as db:
        cursor = db.cursor()
    readData = '''SELECT led, servo FROM employees;'''
    cursor.execute(readData)
    testData = cursor.fetchall()

    return testData[0]

def checkScore():
    with sqlite3.connect("./databases/balldart.db") as db:
        cursor = db.cursor()

    readData = '''SELECT pointsOne, pointsTwo FROM games;'''
    cursor.execute(readData)
    scoreInfo = cursor.fetchall()
    if int(scoreInfo[0][0]) == int(scoreInfo[0][1]):
        return 1
    if int(scoreInfo[0][0]) > int(scoreInfo[0][1]):
        return 2
    if int(scoreInfo[0][0]) < int(scoreInfo[0][1]):
        return 3