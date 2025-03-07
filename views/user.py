import sqlite3
import json
from datetime import datetime


class User:
    """class for interacting with Users from database"""

    def login_user(self, user):
        """Checks for the user in the database

        Args:
            user (dict): Contains the username and password of the user trying to login

        Returns:
            json string: If the user was found will return valid boolean of True and the user's id as the token
                         If the user was not found will return valid boolean False
        """
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute(
                """
                SELECT id, username
                from Users
                where username = ?
                and password = ?
            """,
                (user["username"], user["password"]),
            )

            user_from_db = db_cursor.fetchone()

            if user_from_db is not None:
                response = {"valid": True, "token": user_from_db["id"]}
            else:
                response = {"valid": False}

            return json.dumps(response)

    def create_user(self, user):
        """Adds a user to the database when they register

        Args:
            user (dictionary): The dictionary passed to the register post request

        Returns:
            json string: Contains the token of the newly created user
        """
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute(
                """
            Insert into Users (first_name, last_name, username, email, password, bio, created_on, active) values (?, ?, ?, ?, ?, ?, ?, 1)
            """,
                (
                    user["first_name"],
                    user["last_name"],
                    user["username"],
                    user["email"],
                    user["password"],
                    user["bio"],
                    datetime.now(),
                ),
            )

            id = db_cursor.lastrowid

            return json.dumps({"token": id, "valid": True})

    def get_user_full_name(self, user_id):
        """Checks for the user in the database

        Args:
            user_id (int):
        Returns:
            json string: of user name
        """
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute(
                """
                SELECT first_name, last_name 
                from Users
                where id = ?
            """,
                (user_id,),
            )

            user_full_name_from_db = db_cursor.fetchone()

            if user_full_name_from_db is not None:
                response = {
                    "full_name": f"{user_full_name_from_db['first_name']} {user_full_name_from_db['last_name']}"
                }
            else:
                response = {"full_name": "User not Found"}

            return json.dumps(response)

    def get_all_users(self):
        """gets all Users in the database

        Returns:
            json string: of users
        """
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute(
                """
                SELECT
                id,
                first_name,
                last_name,
                username,
                email,
                password,
                bio,
                created_on,
                active 
                from Users
            """
            )

            users_from_db = db_cursor.fetchall()
            all_users = []

            for user in users_from_db:
                user = {
                    "id": user["id"],
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "username": user["username"],
                    "email": user["email"],
                    "bio": user["bio"],
                    "created_on": user["created_on"],
                    "active": user["active"],
                }
                all_users.append(user)

            return json.dumps(all_users)
