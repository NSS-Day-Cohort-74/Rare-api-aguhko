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
            # row_affected = db_cursor.rowcount

            # return True if row_affected > 0 else False

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
                    p.approved
                FROM Posts p
                ORDER BY Id DESC
                LIMIT 1
                """
            )

            last_created_item = db_cursor.fetchone()

            last_created_item_as_dictionary = dict(last_created_item)
            last_created_item_as_json = json.dumps(last_created_item_as_dictionary)
            return last_created_item_as_json

    def list_posts(self):
        """Get all posts from the database"""
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute(
                """
                SELECT
                     p.id,
                     p.user_id,
                     CONCAT(u.first_name, " ", u.last_name) AS full_name,
                     p.category_id,
                     c.label AS category_name,
                     t.id AS tag_id,
                     t.label AS tag_name,
                     p.title,
                     p.publication_date,
                     p.image_url,
                     p.content,
                     p.approved
            FROM Posts p
                JOIN Users u
                    ON p.user_id = u.id                                  
                JOIN Categories c
                    ON c.id = p.category_id
                LEFT JOIN PostTags pt
                    ON p.id = pt.post_id
                LEFT JOIN Tags t
                    ON t.id = pt.tag_id
            """
            )

            query_results = db_cursor.fetchall()

            posts = []
            # Converting SQLite Rows to Python dictionaries, adding them to a list
            for result in query_results:
                post = dict(result)
                posts.append(post)

            new_set = set()

            for post in posts:
                # Destructuring dictionaries for their unique post ids, adding them to a set
                id, *_ = post.values()
                new_set.add(id)

            new_posts = []
            for id in new_set:
                # Compares unique post ids in posts, removes duplicate entries made by more than one tag
                unique_posts_by_id = list(filter(lambda post: id == post["id"], posts))
                tag_list = []
                # Appends the matching posts' multiple tag_names and tag_ids to a list, as a key in the response body
                for post in unique_posts_by_id:
                    tag = {"tag_name": post["tag_name"], "tag_id": post["tag_id"]}
                    tag_list.append(tag)
                # Some posts may not have tags, this will set their default value if this is the case
                if not tag_list[0]["tag_name"]:
                    tags = None
                else:
                    tags = tag_list

                # creates new key/value pair. Value of the key is a list of tags associated with one post
                new_posts.append({**dict(unique_posts_by_id[0]), "tags": tags})

            return json.dumps(new_posts)

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
                """,
                (user_id,),
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
                """,
                (post_id,),
            )

            query_result = db_cursor.fetchone()

            query_result_as_dict = dict(query_result)
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
                u.first_name || ' ' || u.last_name AS author_name

                FROM Posts p
                JOIN Subscriptions s ON p.user_id = s.author_id

                JOIN Categories c ON p.category_id = c.id

                JOIN Users u ON p.user_id = u.id

                WHERE s.follower_id = ?;

                """,
                (user_id,),
            )

            query_result = db_cursor.fetchall()
            sub_posts = [dict(row) for row in query_result]
            return json.dumps(sub_posts)
