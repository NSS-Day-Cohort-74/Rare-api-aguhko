import sqlite3
import json


class Comment:
    def get_all(self):
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute(
                """
                SELECT 
                    c.id,
                    c.post_id,
                    c.content,
                    u.username AS author_name
                FROM Comments c
                JOIN Users u ON c.author_id = u.id
                """
            )

        query_result = db_cursor.fetchall()  # Get all comments

        query_result_as_list = [
            dict(row) for row in query_result
        ]  # Convert to list of dictionaries
        return json.dumps(query_result_as_list)  # Convert to JSON

    def delete_a_comment(self, primary_key):
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute(
                """
                DELETE FROM Comments
                WHERE id = ? 
                """,
                (primary_key,),
            )

            number_of_row_deleted = db_cursor.rowcount
            return True if number_of_row_deleted > 0 else False

    def create(self, new_comment):
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute(
                """
                INSERT INTO Comments (author_id, post_id, content)
            
                VALUES (?,?,?)
                """,
                (
                    new_comment["author_id"],
                    new_comment["post_id"],
                    new_comment["content"],
                ),
            )
        rows_affected = db_cursor.rowcount

        return True if rows_affected > 0 else False
