import time
import sqlite3
import random

mode = 0
old_mode = mode
round_interval = 10
round_counter = round_interval
round_max = 6
round = round_max
database_fetch_interval = 5
counter = database_fetch_interval
activePlayer = 1

while True:
  time.sleep(1)
  counter -= 1
  if counter == 0:
    counter = database_fetch_interval
    print("Hoi")
    with sqlite3.connect("./databases/balldart.db") as db:
      cursor = db.cursor()
    readData = '''SELECT * FROM games WHERE id = ?'''
    cursor.execute(readData, ["board1"])
    gameRecord = cursor.fetchall()
    print(gameRecord)
    mode = gameRecord[0][1]
    round = gameRecord[0][2]
    activePlayer = gameRecord[0][5]
    print(mode + round + activePlayer)

  if mode == 0:
    if old_mode == mode:
      print("idle")
    else:
      old_mode = mode
      print("single/multi")
  else:
    if old_mode == mode:
      print("active")
      if round != 0:
        round_counter -= 1
        if round_counter == 0:
          round_counter = round_interval
          if round != 0:
            print(activePlayer)
            print(round)
            if activePlayer == 1:
              activePlayer = 2
            else:
              activePlayer = 1
            round -= 1
            insertData = '''UPDATE games SET round = ?, activePlayer = ?, pointsOne = ?, pointsTwo = ? WHERE id = ?'''
            row = (round, activePlayer, random.randint(1, 10),random.randint(1, 10), "board1")
            cursor.execute(insertData, row)
            db.commit()
    else:
      old_mode = mode
      round_counter = round_interval
      round = round_max
      print("start game")
