import argparse
from werkzeug.security import generate_password_hash
import secrets
import string

from modules.Auth.auth import auth
from modules.Auth.user_db import UserDatabase
from app import app

def main():
    parser = argparse.ArgumentParser(description="Archive posters from impawards.com")
    parser.add_argument("--init",  help="Starting pages number", action="store_true")
    args = parser.parse_args()

    if args.init:
        print(app.config["USERS_DB"])
        db = UserDatabase(app.config["USERS_DB"])

        resp = db.create_tables()
        if resp:
            print("Created database tables")
        else:
            print("Failed to insert database tables")
            return False


        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(12))
        resp = db.insert_user(
            "admin", "admin", "user", "admin@ohas.com",
            generate_password_hash(password, method="sha256"), "", 24, 1
        )
        if resp:
            print(f"Inserted admin user with password {password}")
        else:
            print("Failed to insert admin user")

main()
