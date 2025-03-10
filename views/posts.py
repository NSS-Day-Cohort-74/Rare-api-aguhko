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
                CONCAT(u.first_name, " ", u.last_name) as full_name,
                p.category_id,
                p.title,
                p.publication_date,
                p.image_url,
                p.content,
                p.approved
            FROM Posts p
                JOIN Users u
                ON p.user_id = u.id                                  
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
                    CONCAT(u.first_name, " ", u.last_name) as full_name,
                    p.category_id,
                    p.title,
                    p.publication_date,
                    p.image_url,
                    p.content,
                    p.approved
                FROM Posts p
                JOIN Users u
                ON p.user_id = u.id                
                WHERE p.user_id = ?
                """, (user_id,)
            )

            query_results = db_cursor.fetchall()

            user_posts = []

            for result in query_results:
                user_posts.append(dict(result))

            user_posts_json = json.dumps(user_posts)

            return user_posts_json
    
    def get_post_by_id(self, query_params):
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            post_id = int(query_params["post_id"][0])
            db_cursor.execute(
                """
                SELECT 
                    p.id,
                    p.user_id,
                    CONCAT(u.first_name, " ", u.last_name) as full_name,
                    p.category_id,
                    c.label category_name,
                    p.title,
                    p.publication_date,
                    p.image_url,
                    p.content,
                    p.approved
                FROM Posts p
                    JOIN Users u
                    ON p.user_id = u.id
                    JOIN Categories c
                    ON p.category_id = c.id
                WHERE p.id = ?
                """, (post_id,)
                )

            query_result = db_cursor.fetchone()

            query_result_as_dict = dict(query_result)
            query_result_as_json = json.dumps(query_result_as_dict)
            return query_result_as_json