import sqlite3

def list_posts():
    """Get all posts from the database"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # SQL Query to fetch all posts
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

    return posts  # Returns a Python list, which will be converted to JSON in server.py
