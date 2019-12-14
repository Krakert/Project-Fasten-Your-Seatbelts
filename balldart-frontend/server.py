# file backend/api.py
from flask import Flask
from flask import jsonify
from flask import request, send_from_directory
import json
import random
import sqlite3

app = Flask(__name__)

# this function returns an object for one user
def a(row):
    return {
        "type": "accounts",                      # It has to have type
        "id": row[0],                        # And some unique identifier
        "attributes": {                          # Here goes actual payload.
            "password": row[1],
            "total-points": row[2],
            "highest-points": row[3],
            "number-of-rounds": row[4],
            "latest-round": row[5],     # the only data we have for each user is "info" field
        },
    }

# routes for individual entities
@app.route('/api/accounts/<account_id>', methods=['GET','POST','SET'])
def accounts_by_id(account_id):
    print("singleAccount")
    return jsonify({"data": a(account_id)})


# route for all entities
@app.route('/api/accounts', methods=['GET','POST','SET'])
def accounts():
    if request.method == 'POST':
      pythonObject = json.loads(request.data)
      print(pythonObject["data"]["id"])
      return jsonify({"data": a(pythonObject["data"]["id"])})
    else:
      with sqlite3.connect("/dev/sqlite3/balldart.db") as db:
          cursor = db.cursor()
      readData = '''SELECT * FROM account;'''
      cursor.execute(readData)
      accountRecord = cursor.fetchall()
      print(accountRecord)
      return jsonify({
          "data": [a(row) for row in accountRecord]
          })

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
