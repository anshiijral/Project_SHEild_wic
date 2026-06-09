from database.db import get_connection


def save_post(username, text, category, score):

    db = get_connection()

    cursor = db.cursor()

    query = """
    INSERT INTO flagged_posts
    (username, post_text, category, toxicity_score)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (
            username,
            text,
            category,
            score
        )
    )

    db.commit()

    cursor.close()
    db.close()

    print("Post saved successfully")