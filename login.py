import sqlite3
import time


def login():
    while True:
        username = input("Geef u gebruikersnaam op: ")
        password = input("Geef u wachtwoord op: ")
        with sqlite3.connect("databaseBalldart.db") as db:  # create connection to database
            cursor = db.cursor()
        # Checks what username belongs to which password
        find_user = ("SELECT * FROM User WHERE username = ? AND  password = ?")  # Checks what username belogns to which

        cursor.execute(find_user, [(username),(password)])
        results = cursor.fetchall()

        if results:
            print("Welkom " + username)
            break
        else:
            print("Gebruikersnaam en/of wachtwoord onjuist!")
            again = input("Wilt u het opnieuw proberen(j/n): ")
            if again.lower() == "n":
                print("Tot ziens!")
                time.sleep(1)
                break
