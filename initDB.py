# This file only needs to run once
import sqlite3

def create_connection(db_file):
    """ Create a database connection to the SQLite database """
    conn = sqlite3.connect(db_file)
    return conn

def accounts(conn):
    cursor = conn.cursor()
    # Create Table
    sql_create_account_table = '''CREATE TABLE IF NOT EXISTS accounts (
                                        id varchar(255) PRIMARY KEY,
                                        password varchar(255),
                                        totalPoints integer,
                                        highestPoints integer,
                                        numberOfRounds integer,
                                        latestRound integer
                                    );'''
    cursor.execute(sql_create_account_table)

def games(conn):
    cursor = conn.cursor()
    # Create Table
    sql_create_game_table = '''CREATE TABLE IF NOT EXISTS games (
                                        id varchar(255) PRIMARY KEY,
                                        mode integer,
                                        round integer,
                                        pointsOne integer,
                                        pointsTwo integer,
                                        activePlayer integer
                                    );'''
    cursor.execute(sql_create_game_table)

    # Insert Record
    sql_insertData = '''INSERT INTO games(id, mode, round, pointsOne, pointsTwo, activePlayer) VALUES(?,?,?,?,?,?)'''
    cursor.execute(sql_insertData, [('board1'), (0), (0), (0), (0), (0)])
    conn.commit()

def employees(conn):
    cursor = conn.cursor()
    # Create Table
    sql_create_employee_table = '''CREATE TABLE IF NOT EXISTS employees (
                                        id varchar(255) PRIMARY KEY,
                                        active bit,
                                        led int,
                                        servo int
                                    );'''
    cursor.execute(sql_create_employee_table)

    # Insert Record
    sql_insertData = '''INSERT INTO employees(id, active,led,servo) VALUES(?,?)'''
    cursor.execute(sql_insertData, [('fakeID'), (0),(0),(0)])
    conn.commit()

if __name__ == '__main__':
    conn = create_connection("./databases/balldart.db")
    accounts(conn)
    games(conn)
    employees(conn)
