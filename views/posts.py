import sqlite3


class Post:
    def create_post(self, post):
        # Opens connection to database file
        with sqlite3.connect("./db.sqlite3") as conn:
            # Allows for Data Selecting Functionality
            db_cursor = conn.cursor()

            db_cursor.execute(
                """
                INSERT INTO Posts
                (user_id, category_id, title, publication_date, image_url, content, approved) VALUES (?, ?, ?, ?, ?, ?, ?)

            """,
                (
                    post["user_id"],
                    post["category_id"],
                    post["title"],
                    post["publication_date"],
                    post["image_url"],
                    post["content"],
                    post["approved"],
                ),
            )
