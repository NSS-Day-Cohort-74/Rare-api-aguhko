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
            
