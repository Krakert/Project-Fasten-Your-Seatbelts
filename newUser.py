import sqlite3


def new_user():
    found = 0
    while found == 0:
        username = input("Gebruikersnaam: ")
        with sqlite3.connect("databaseBalldart.db") as db:  # create connection to database
            cursor = db.cursor()
        findUser = ("SELECT * FROM user WHERE username = ?")
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
    insertData = '''INSERT INTO user(username, password)
    VALUES(?,?)'''
    cursor.execute(insertData, [(username), (password)])
    db.commit()



def main():
    new_user()


if __name__ == '__main__':
    main()
