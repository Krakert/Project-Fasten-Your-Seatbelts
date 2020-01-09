#!/usr/bin/env python3

#import installed libraries
from flask import Flask, jsonify, request, send_from_directory
import json
import random
import sqlite3

app = Flask(__name__)

# this function returns an object for one account
def a(row):
    return {
        "type": "accounts",                      # It has to have type
        "id": row[0],                            # And some unique identifier
        "attributes": {                          # Here goes actual payload.
            "password": row[1],
            "total-points": row[2],
            "highest-points": row[3],
            "number-of-rounds": row[4],
            "latest-round": row[5],
        },
    }

def e(row):
    return {
        "type": "employees",                       # It has to have type
        "id": row[0],                              # And some unique identifier
        "attributes": {                            # Here goes actual payload.
            "active": row[1],
            "led": row[2],
            "servo": row[3],
        },
    }

# this function returns an object for one game
def g(row):
    return {
        "type": "games",                         # It has to have type
        "id": row[0],                            # And some unique identifier
        "attributes": {                          # Here goes actual payload.
            "mode": row[1],
            "round": row[2],
            "points-one": row[3],
            "points-two": row[4],
            "active-player": row[5],
        },
    }

# routes for individual entities
@app.route('/api/accounts/<account_id>', methods=['DELETE','GET','PATCH'])
def accounts_by_id(account_id):
    if request.method == 'DELETE':
      print("singleAccount")
      with sqlite3.connect("../databases/balldart.db") as db:                      # create connection to database
          cursor = db.cursor()

      sql_deleteAccount = '''DELETE FROM accounts WHERE id = ?'''
      cursor.execute(sql_deleteAccount, (account_id, ))
      db.commit()
      return '', 204
    elif request.method == 'GET':
      with sqlite3.connect("../databases/balldart.db") as db:
          cursor = db.cursor()
      readData = '''SELECT * FROM accounts WHERE id = ?'''
      cursor.execute(readData, [(account_id)])
      accountRecord = cursor.fetchall()
      print(accountRecord)
      return jsonify({"data": a(accountRecord[0])})
    else:
      pythonObject = json.loads(request.data)
      with sqlite3.connect("../databases/balldart.db") as db:                      # create connection to database
          cursor = db.cursor()
      insertData = '''UPDATE accounts
                      SET
                        password = ?,
                        totalPoints = ?,
                        highestPoints = ?,
                        numberOfRounds = ?,
                        latestRound = ?
                      WHERE id = ?'''
      row = ((pythonObject["data"]["attributes"]["password"]),
      (pythonObject["data"]["attributes"]["total-points"]),
      (pythonObject["data"]["attributes"]["highest-points"]),
      (pythonObject["data"]["attributes"]["number-of-rounds"]),
      (pythonObject["data"]["attributes"]["latest-round"]),
      (pythonObject["data"]["id"]))
      cursor.execute(insertData, row)
      row = ((pythonObject["data"]["id"]),
      (pythonObject["data"]["attributes"]["password"]),
      (pythonObject["data"]["attributes"]["total-points"]),
      (pythonObject["data"]["attributes"]["highest-points"]),
      (pythonObject["data"]["attributes"]["number-of-rounds"]),
      (pythonObject["data"]["attributes"]["latest-round"]))
      db.commit()
      return jsonify({"data": a(row)})

# route for all entities
@app.route('/api/accounts', methods=['GET','POST'])
def accounts():
    if request.method == 'POST':
      pythonObject = json.loads(request.data)
      with sqlite3.connect("../databases/balldart.db") as db:                      # create connection to database
          cursor = db.cursor()
      print(pythonObject["data"])
      insertData = '''INSERT INTO accounts(id, password, totalPoints, highestPoints, numberOfRounds, latestRound)
      VALUES(?,?,?,?,?,?)'''
      row = ((pythonObject["data"]["id"]),
      (pythonObject["data"]["attributes"]["password"]),
      (pythonObject["data"]["attributes"]["total-points"]),
      (pythonObject["data"]["attributes"]["highest-points"]),
      (pythonObject["data"]["attributes"]["number-of-rounds"]),
      (pythonObject["data"]["attributes"]["latest-round"]))
      cursor.execute(insertData, row)
      db.commit()
      return jsonify({"data": a(row)})
    else:
      with sqlite3.connect("../databases/balldart.db") as db:
          cursor = db.cursor()
      readData = '''SELECT * FROM accounts'''
      cursor.execute(readData)
      accountRecord = cursor.fetchall()
      print(accountRecord)
      return jsonify({
          "data": [a(row) for row in accountRecord]
          })

# route for all entities
@app.route('/api/employees', methods=['GET'])
def employees():
    with sqlite3.connect("../databases/balldart.db") as db:
        cursor = db.cursor()
    employeeData = '''SELECT * FROM employees;'''
    cursor.execute(employeeData)
    employeeRecord = cursor.fetchall()
    return jsonify({
        "data": [e(row) for row in employeeRecord]
        })
@app.route('/api/employees/<employee_id>', methods=['PATCH','GET'])
def employees_by_id(employee_id):
    if request.method == 'PATCH':
      pythonObject = json.loads(request.data)
      with sqlite3.connect("../databases/balldart.db") as db:                      # create connection to database
          cursor = db.cursor()
      print(pythonObject["data"])

      insertData = '''UPDATE employees
                      SET
                        active = ?,
                        led = ?,
                        servo = ?
                      WHERE id = ?'''
      row = ((pythonObject["data"]["attributes"]["active"]),
      (pythonObject["data"]["attributes"]["led"]),
      (pythonObject["data"]["attributes"]["servo"]),
      (pythonObject["data"]["id"]))
      cursor.execute(insertData, row)
      row = ((pythonObject["data"]["id"]),
      (pythonObject["data"]["attributes"]["active"]),
      (pythonObject["data"]["attributes"]["led"]),
      (pythonObject["data"]["attributes"]["servo"]))
      db.commit()
      return jsonify({"data": e(row)})
    else:
      with sqlite3.connect("../databases/balldart.db") as db:
          cursor = db.cursor()
      readData = '''SELECT * FROM employees WHERE id = ?'''
      cursor.execute(readData, [(employee_id)])
      employeesRecord = cursor.fetchall()
      return jsonify({"data": e(employeesRecord[0])})

@app.route('/api/games/<game_id>', methods=['GET','PATCH'])
def games_by_id(game_id):
    if request.method == 'PATCH':
      pythonObject = json.loads(request.data)
      with sqlite3.connect("../databases/balldart.db") as db:                      # create connection to database
          cursor = db.cursor()
      print(pythonObject["data"])

      insertData = '''UPDATE games
                      SET
                        mode = ?,
                        round = ?,
                        pointsOne = ?,
                        pointsTwo = ?,
                        activePlayer = ?
                      WHERE id = ?'''

      row = ((pythonObject["data"]["attributes"]["mode"]),
      (pythonObject["data"]["attributes"]["round"]),
      (pythonObject["data"]["attributes"]["points-one"]),
      (pythonObject["data"]["attributes"]["points-two"]),
      (pythonObject["data"]["attributes"]["active-player"]),
      (pythonObject["data"]["id"]))
      cursor.execute(insertData, row)
      row = ((pythonObject["data"]["id"]),
      (pythonObject["data"]["attributes"]["mode"]),
      (pythonObject["data"]["attributes"]["round"]),
      (pythonObject["data"]["attributes"]["points-one"]),
      (pythonObject["data"]["attributes"]["points-two"]),
      (pythonObject["data"]["attributes"]["active-player"]))
      db.commit()
      return jsonify({"data": g(row)})
    else:
      with sqlite3.connect("../databases/balldart.db") as db:
          cursor = db.cursor()
      readData = '''SELECT * FROM games WHERE id = ?'''
      cursor.execute(readData, [(game_id)])
      gameRecord = cursor.fetchall()
      print(gameRecord)
      return jsonify({"data": g(gameRecord[0])})

# default route.
# flask has to serve a file that will be generated later with ember
# relative path is dist/index.html
@app.route('/')
def root():
    return send_from_directory('./dist/', "index.html")

# route for other static files
@app.route('/<path:path>')
def send_files(path):
    try:
      return send_from_directory('./dist/', path)
    except:
      return send_from_directory('./dist/', "index.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
