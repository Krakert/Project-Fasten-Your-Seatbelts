# file backend/api.py
from flask import Flask
from flask import jsonify
from flask import request, send_from_directory
import json


app = Flask(__name__)

# this function returns an object for one user
def a(account_id):
    return {
        "type": "accounts",                      # It has to have type
        "id": account_id,                        # And some unique identifier
        "attributes": {                          # Here goes actual payload.
            "password": "data" + str(account_id),
            "total-points": "total",
            "highest-points": "highest",
            "number-of-rounds": "rounds",
            "latest-round": "latest",     # the only data we have for each user is "info" field
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
    # pythonObject = json.loads(request.data)
    # print(pythonObject["data"]["id"])
    if request.method == 'POST':
      pythonObject = json.loads(request.data)
      print(pythonObject["data"]["id"])
      return jsonify({"data": a(pythonObject["data"]["id"])})
    else:
      return jsonify({
          "data": [a(i) for i in range(0,10)]
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
