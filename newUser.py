import sqlite3

def new_account():
    found = 0
    zero = 0
    while found == 0:
        username = input("Gebruikersnaam: ")

        with sqlite3.connect("/dev/sqlite3/balldart.db") as db:                      # create connection to database
            cursor = db.cursor()

        findUser = ("SELECT * FROM account WHERE id = ?")
        cursor.execute(findUser, [(username)])

        if cursor.fetchall():
            print("Gebruikersnaam al in gebruik, probeer het opnieuw")
        else:
            found = 1

    password = input("Geef een wachtwoord op: ")
    password1 = input("Geef uw wachtwoord opnieuw op: ")
    while password != password1:
        print("Uw wachtwoord komt niet overeen, probeer het opnieuw")
        password = input("Geef een wachtwoord op: ")
        password1 = input("Geef u wachtwoord opnieuw op: ")

    insertData = '''INSERT INTO account(id, password, totalPoints, highestPoints, numberOfRounds, latestRound)
    VALUES(?,?,?,?,?,?)'''
    cursor.execute(insertData, [(username), (password), (zero), (zero), (zero), (zero)])
    db.commit()

def main():
    new_account()

if __name__ == '__main__':
    main()
