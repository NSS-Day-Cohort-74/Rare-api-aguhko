import sqlite3
import json
from datetime import datetime

class Subscription():
    """
    Class for interacting with the Subscriptions table in database. 
    """
    def get_subscriptions(self):
        """
        Gets a list of all subscriptions
        """
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute(
                """
                SELECT
                    s.id,
                    s.follower_id,
                    s.author_id,
                    created_on
                FROM Subscriptions s"""
            )

            query_results = db_cursor.fetchall()

            subscriptions = []

            for row in query_results:
                subscriptions.append(dict(row))
            
            subscriptions_as_json = json.dumps(subscriptions)

            return subscriptions_as_json
    
    def subscribe(self, subscription):
        """
        Creates a new relationship between a viewing user (follower) and another user (author)
        """
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            # Inserts new relationship into the database
            db_cursor.execute(
                """
                INSERT INTO Subscriptions (follower_id, author_id, created_on) VALUES (?, ?, ?)
                """,
                (
                    subscription["follower_id"],
                    subscription["author_id"],
                    datetime.now(),
                ),
            )