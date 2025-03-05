import sqlite3
import json

class Category():
    """class for interacting with Categories from database"""

    def get_all(self):
        """Gets categories in the database
    
        Args:
            None
    
        Returns:
            all categories
        """
        with sqlite3.connect('./db.sqlite3') as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
    
            db_cursor.execute("""
                SELECT id, label from Categories
                ORDER BY LOWER(label) ASC;
            """)
    
            categories_from_db = db_cursor.fetchall()

            categories = []

            for category in categories_from_db:
                category = {
                    "id": category["id"],
                    "label": category["label"]

                }
                categories.append(dict(category))
    
    
            return json.dumps(categories)
    
    
    def create_category(self, new_category ):
        with sqlite3.connect("./db.sqlite3") as conn:
            db_cursor = conn.cursor()
            db_cursor.execute("""
               INSERT INTO 'Categories' (label)
               VALUES 
               (?)
               """, ( new_category["label"], ),
            )
            rows_affected = db_cursor.rowcount

            return True if rows_affected > 0 else False
