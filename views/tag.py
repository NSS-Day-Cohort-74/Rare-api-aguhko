import sqlite3
import json

class Tag():
    """class for interacting with Tags from database"""

    def get_all(self):
        """Gets tags in the database
    
        Args:
            None
    
        Returns:
            all tags
        """
        with sqlite3.connect('./db.sqlite3') as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
    
            db_cursor.execute("""
                SELECT id, label from Tags
                ORDER BY LOWER(label) ASC;
            """)
    
            tags_from_db = db_cursor.fetchall()

            tags = []

            for tag in tags_from_db:
                tag = {
                    "id": tag["id"],
                    "label": tag["label"]

                }
                tags.append(dict(tag))
    
    
            return json.dumps(tags)
    
    
    def create_tag(self, newTag):
        with sqlite3.connect("./db.sqlite3") as conn:
            db_cursor = conn.cursor()
            db_cursor.execute("""
               INSERT INTO 'Tags' (label)
               VALUES 
               (?)
               """, ( newTag["label"], ),
            )
            rows_affected = db_cursor.rowcount

            return True if rows_affected > 0 else False
