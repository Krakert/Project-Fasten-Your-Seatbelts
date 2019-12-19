# file backend/api.py
from flask import Flask
from flask import jsonify
from flask import request, send_from_directory
import json
import random
import sqlite3

app = Flask(__name__)

# this function returns an object for one account
def a(row):
    return {
        "type": "accounts",                      # It has to have type
        "id": row[0],                        # And some unique identifier
        "attributes": {                          # Here goes actual payload.
            "password": row[1],
            "total-points": row[2],
            "highest-points": row[3],
            "number-of-rounds": row[4],
            "latest-round": row[5],
        },
    }

# this function returns an object for one game
def g(row):
    return {
        "type": "games",                      # It has to have type
        "id": row[0],                        # And some unique identifier
        "attributes": {                          # Here goes actual payload.
            "mode": row[1],
        },
    }

# routes for individual entities
@app.route('/api/accounts/<account_id>', methods=['DELETE'])
def accounts_by_id(account_id):
    print("singleAccount")
    return '', 204


# route for all entities
@app.route('/api/accounts', methods=['GET','POST','SET'])
def accounts():
    if request.method == 'POST':
      pythonObject = json.loads(request.data)
      with sqlite3.connect("../databases/balldart.db") as db:                      # create connection to database
          cursor = db.cursor()
      print(pythonObject["data"])
      insertData = '''INSERT INTO account(id, password, totalPoints, highestPoints, numberOfRounds, latestRound)
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
      readData = '''SELECT * FROM account;'''
      cursor.execute(readData)
      accountRecord = cursor.fetchall()
      print(accountRecord)
      return jsonify({
          "data": [a(row) for row in accountRecord]
          })

@app.route('/api/games/<game_id>', methods=['GET','PATCH'])
def games_by_id(game_id):
    if request.method == 'PATCH':
      print("tomatensap/patch")
      pythonObject = json.loads(request.data)
      with sqlite3.connect("../databases/balldart.db") as db:                      # create connection to database
          cursor = db.cursor()
      print(pythonObject["data"])

      insertData = '''UPDATE game
                      SET mode = ?
                      WHERE id = ?'''
      row = ((pythonObject["data"]["attributes"]["mode"]),(pythonObject["data"]["id"]))
      cursor.execute(insertData, row)
      db.commit()
      return jsonify({"data": g(row)})
    else:
      with sqlite3.connect("../databases/balldart.db") as db:
          cursor = db.cursor()
      readData = '''SELECT * FROM game WHERE id = ?'''
      cursor.execute(readData, [(game_id)])
      accountRecord = cursor.fetchall()
      print(accountRecord)
      return jsonify({"data": g(accountRecord[0])})



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
