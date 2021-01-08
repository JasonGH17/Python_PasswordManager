import sqlite3
from hashlib import sha256

ADMINPASS = "88044088"
db = sqlite3.connect("db.sqlite")

connect = input("Enter admin password: \n")
while connect != ADMINPASS:
    connect = input("Enter admin password: \n")
    if connect == "q" or "quit":
        break

def createPassword(passKey, service, admin):
    return sha256(admin.encode('utf8') + service.lower().encode('utf8') + passKey.encode('utf8')).hexdigest()[:10]

def getHexKey(admin, service):
    return sha256(admin.encode('utf8') + service.lower().encode('utf8')).hexdigest()

def getPassword(admin, service):
    key = getHexKey(ADMINPASS, service)
    cursor = db.execute(f'SELECT * FROM KEYS WHERE PASS_KEY="{key}"')
    passKey = ""
    for row in cursor:
        passKey = row[0]
    
    return createPassword(passKey, service, ADMINPASS)

def addPassword(service, admin):
    key = getHexKey(admin, service)
    command = 'INSERT INTO KEYS (PASS_KEY) VALUES (%s);' %(f"'{key}'")
    db.execute(command)

    return createPassword(key, service, admin)

if connect == str(ADMINPASS):
    try:
        db.execute('''CREATE TABLE KEYS
            (PASS_KEY TEXT PRIMARY KEY NOT NULL);''')
        print("You safe has been created! What would you like to store in it today?")
    except:
        print("You have a safe, what would you like to store in it today?")

    while True:
        print(f'{"*"*15}\nCOMMANDS:\ns = Store password\ng = Get password\nq = Quit program\n{"*"*15}')
        cmd = input(": ")
        if cmd == "q":
            break
        elif cmd == "s":
            service = input("What is the name of the service\n")
            print(f'\n{service.capitalize()} password created:\n{addPassword(service, ADMINPASS)}')
        elif cmd == "g":
            service = input("What is the name of the service\n")
            print(f"\n{service.capitalize()} password:\n{getPassword(ADMINPASS, service)}")
        else:
            print("Invalid command...")
            continue
