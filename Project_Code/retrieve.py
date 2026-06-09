from db import get_connection

def get_flagged_posts():
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM flagged_posts")
    posts = cursor.fetchall()
    cursor.close()
    db.close()
    return posts

if __name__ == "__main__":
    data = get_flagged_posts()
    print("Database connection successful! Total posts found:", len(data))
    for post in data:
        print(post)