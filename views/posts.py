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
            new_post_id = db_cursor.lastrowid

            return json.dumps(new_post_id)

    def list_posts(self):
        """Get all posts from the database"""
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute("""
                    SELECT 
                        p.id ,
                        p.title ,
                        p.user_id,
                        CONCAT(u.first_name, " ", u.last_name) as author_name,
                        p.content,
                        p.image_url,
                        p.category_id,
                        c.label AS category_name,
                        p.publication_date,
                        p.image_url,
                        p.approved,
                        GROUP_CONCAT( DISTINCT tg.label) AS tags
                    FROM 
                        Posts p

                        JOIN Users u ON u.id = p.user_id

                        JOIN Categories c ON c.id = p.category_id
                    LEFT JOIN 
                        PostTags ptg ON p.id = ptg.post_id
                    LEFT JOIN 
                        Tags tg ON ptg.tag_id = tg.id
                    GROUP BY 
                        p.id
                    
            """)

            query_results = db_cursor.fetchall()

            posts = []
            for row in query_results:
                post = dict(row)
                if post["tags"]:
                    post["tags"] = post["tags"].split(",")

                posts.append(post)

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
                    CONCAT(u.first_name, ' ', u.last_name) AS full_name,
                    p.category_id,
                    c.label AS category_name,
                    p.title,
                    p.publication_date,
                    p.image_url,
                    p.content,
                    p.approved,
                    GROUP_CONCAT( DISTINCT tg.label) AS tags

                FROM Posts p
                
                JOIN Users u
                ON p.user_id = u.id                

                JOIN Categories c
                ON c.id = p.category_id

                LEFT JOIN 
                    PostTags ptg ON p.id = ptg.post_id
                LEFT JOIN 
                    Tags tg ON ptg.tag_id = tg.id

                WHERE p.user_id = ?

                GROUP BY 
                    p.id

                """,
                (user_id,),
            )

            query_results = db_cursor.fetchall()

            user_posts = []

            for result in query_results:
                post = dict(result)
                if post["tags"]:
                    post["tags"] = post["tags"].split(",")
                user_posts.append(post)

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
                    CONCAT(u.first_name, ' ', u.last_name) as full_name,
                    p.category_id,
                    c.label category_name,
                    p.title,
                    p.publication_date,
                    p.image_url,
                    p.content,
                    p.approved,
                    GROUP_CONCAT( DISTINCT tg.label) AS tags
                FROM Posts p
                    JOIN Users u
                    ON p.user_id = u.id
                    JOIN Categories c
                    ON p.category_id = c.id

                LEFT JOIN 
                    PostTags ptg ON p.id = ptg.post_id
                LEFT JOIN 
                    Tags tg ON ptg.tag_id = tg.id
                WHERE p.id = ?

                GROUP BY 
                    p.id
                """,
                (post_id,),
            )

            query_result = db_cursor.fetchone()

            query_result_as_dict = dict(query_result)
            if query_result_as_dict["tags"]:
                query_result_as_dict["tags"] = query_result_as_dict["tags"].split(",")
            query_result_as_json = json.dumps(query_result_as_dict)
            return query_result_as_json

    def delete_a_post(self, primary_key):
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute(
                """
                DELETE FROM Posts
                WHERE id = ? 
                """,
                (primary_key,),
            )

            number_of_row_deleted = db_cursor.rowcount
            return True if number_of_row_deleted > 0 else False

    def get_subscribed_to_users_posts(self, user_id):
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute(
                """
                SELECT 
                p.*,
                c.label AS category_label,
               CONCAT( u.first_name,' ', u.last_name) AS author_name

                FROM Posts p
                JOIN Subscriptions s ON p.user_id = s.author_id

                JOIN Categories c ON p.category_id = c.id

                JOIN Users u ON p.user_id = u.id

                WHERE s.follower_id = ?

                """,
                (user_id,),
            )

            query_result = db_cursor.fetchall()
            sub_posts = [dict(row) for row in query_result]
            return json.dumps(sub_posts)
