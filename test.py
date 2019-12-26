import time

mode = 1
old_mode = mode
round_interval = 6
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
    mode = 1

  if mode == 0:
    if old_mode == mode:
      print("idle")
    else:
      old_mode = mode
      print("single/multi")
  else:
    if old_mode == mode:
      print("single")
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
    else:
      old_mode = mode
      round_counter = round_interval
      round = round_max
      print("start game single")
