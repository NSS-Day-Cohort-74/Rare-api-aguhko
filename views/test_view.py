import json, sqlite3


def test_list_posts():
    """Get all posts from the database"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            SELECT
                 p.id,
                 p.user_id,
                 CONCAT(u.first_name, " ", u.last_name) as full_name,
                 p.category_id,
                 t.id AS tag_id,
                 t.label tag_name,
                 p.title,
                 p.publication_date,
                 p.image_url,
                 p.content,
                 p.approved
        FROM Posts p
            JOIN Users u
                ON p.user_id = u.id                                  
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
            # Compares unique post ids in post tag relationships
            unique_posts_by_id = list(filter(lambda post: id == post["id"], posts))
            # appends the matching relationships' tag_names and tag_ids to a list
            tag_list = []
            for post in unique_posts_by_id:
                tag_list.append(post["tag_name"])
            # creates new key/value pair. Value of the key is a list of tags associated with one post
            new_posts.append({**dict(filtered[0]), "tags": tag_list})

        return json.dumps(new_posts)
