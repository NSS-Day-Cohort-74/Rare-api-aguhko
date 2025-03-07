import sqlite3
import json


class Post:
    def create_post(self, post):
        # Opens connection to database file
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            # Allows for Data Selecting Functionality
            db_cursor = conn.cursor()
            # Creates a list of fields that need to be sent in POST request body
            required_fields = [
                "user_id",
                "category_id",
                "title",
                "publication_date",
                "content",
            ]

            for field in required_fields:
                # Iterates the list of requirements with what was sent by client
                if not post.get(field):
                    # Stops POST command because not all required fields were met
                    return False

            db_cursor.execute(
                """
                INSERT INTO Posts
                (user_id, category_id, title, publication_date, image_url, content, approved) 
                VALUES (?, ?, ?, ?, ?, ?, ?)

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
            row_affected = db_cursor.rowcount

            return True if row_affected > 0 else False

    def list_posts(self):
        """Get all posts from the database"""
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT
                p.id,
                p.user_id,
                p.category_id,
                p.title,
                p.publication_date,
                p.image_url,
                p.content,
                p.approved
            FROM Posts p
            """)

            query_results = db_cursor.fetchall()

            # Convert rows to a list of dictionaries
            posts = [dict(row) for row in query_results]

        return posts

    def get_user_posts(self, query_params):
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            user_id = int(query_params["user_id"][0])
            db_cursor.execute(
                """
                SELECT
                    p.id,
                    p.user_id,
                    p.category_id,
                    p.title,
                    p.publication_date,
                    p.image_url,
                    p.content,
                    p.approved,
                    p.created_at
                FROM Posts p
                WHERE p.user_id = ?
                """,
                (user_id,),
            )

            query_results = db_cursor.fetchall()

            user_posts = []

            for result in query_results:
                user_posts.append(dict(result))

            user_posts_json = json.dumps(user_posts)

            return user_posts_json

