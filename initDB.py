# This file only needs to run once
import sqlite3

def create_connection(db_file):
    """ Create a database connection to the SQLite database """
    conn = sqlite3.connect(db_file)
    return conn

def accounts(conn):
    cursor = conn.cursor()
    # Create Table
    sql_create_account_table = '''CREATE TABLE accounts (
    id             VARCHAR (255) PRIMARY KEY
                                 NOT NULL,
    password       VARCHAR (255) NOT NULL,
    totalPoints    INTEGER,
    highestPoints  INTEGER,
    numberOfRounds INTEGER,
    latestRound    INTEGER);'''
    cursor.execute(sql_create_account_table)

def games(conn):
    cursor = conn.cursor()
    # Create Table
    sql_create_game_table = '''CREATE TABLE games (
    id           VARCHAR (255) PRIMARY KEY,
    mode         INTEGER,
    round        INTEGER,
    pointsOne    INTEGER,
    pointsTwo    INTEGER,
    activePlayer INTEGER);'''
    cursor.execute(sql_create_game_table)

    # Insert Record
    sql_insertData = '''INSERT INTO games(id, mode, round, pointsOne, pointsTwo, activePlayer) VALUES(?,?,?,?,?,?)'''
    cursor.execute(sql_insertData, ['board1', 0, 0, 0, 0, 0])
    conn.commit()

def employees(conn):
    cursor = conn.cursor()
    # Create Table
    sql_create_employee_table = '''CREATE TABLE employees (
    id                 VARCHAR (255) PRIMARY KEY
                                     NOT NULL,
    active             INTEGER,
    led                INTEGER,
    servo              INTEGER,
    runtimeSystemInSec INTEGER       DEFAULT (0),
    runtimeServoInSec  INTEGER       DEFAULT (0));'''
    cursor.execute(sql_create_employee_table)

    # Insert Record
    sql_insertData = '''INSERT INTO employees(id, active, led, servo,runtimeSystemInSec,runtimeServoInSec) VALUES(?,?,?,?,?,?)'''
    cursor.execute(sql_insertData, [154162618071, 0, 0, 0, 0, 0])
    conn.commit()

def gameStats(conn):
    cursor = conn.cursor()
    # Create Table
    sql_create_gamestat_table = '''CREATE TABLE gamestat (
    game_number    INTEGER DEFAULT (0),
    player         INTEGER,
    round          INTEGER,
    sequenceLength INTEGER,
    timeInSec      INTEGER);'''
    cursor.execute(sql_create_gamestat_table)

    # Insert Record
    sql_insertData = '''INSERT INTO gamestat(game_number, player, round, sequenceLength, timeInSec) VALUES(?,?,?,?,?)'''
    cursor.execute(sql_insertData, [0, None, None, None, None])
    conn.commit()

if __name__ == '__main__':
    conn = create_connection("./databases/balldart.db")
    accounts(conn)
    games(conn)
    employees(conn)
    gameStats(conn)
