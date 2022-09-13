# login and authentication process
import hashlib
import sqlite3

db = sqlite3.connect("school.db")
cursor = db.cursor()


# sever logins
def login():
    email = input("Enter email: ")
    pwd = input("Enter password: ")
    return email, pwd


def signup_server():
    email = input("Enter email address: ")
    pwd = input("Enter password: ")
    conf_pwd = input("Confirm password: ")
    if conf_pwd == pwd:
        enc = conf_pwd.encode()
        hash1 = hashlib.md5(enc).hexdigest()
        cursor.execute(f"INSERT INTO login_auth ('email', 'pwd')VALUES ('{email}', '{hash1}') ")
        db.commit()
        print("You have registered successfully!")
    else:
        print("Password is not same as above! \n")


def auth_server(email, pwd):
    auth = pwd.encode()
    auth_hash = hashlib.md5(auth).hexdigest()
    cursor.execute(f"SELECT pwd FROM login_auth WHERE email = '{email}' ")
    data = cursor.fetchone()
    stored_pwd = data[0]
    if auth_hash == stored_pwd:
        print("Logged in successfully")
        print()
        return True
    else:
        print("Login failed! \n")


def auth_level(mail):
    cursor.execute(f"SELECT levelcode FROM login_auth WHERE email = '{mail}' ")
    auth_lvl = cursor.fetchone()
    return auth_lvl[0]


if __name__ == '__main__':
    pass
    # signup_server()

    cursor.close()
    db.close()
