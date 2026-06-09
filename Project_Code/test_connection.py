from database.db import get_connection


db = get_connection()

print("MySQL connected successfully")

db.close()