import sys
import os

# Ensure Python can see the other modules inside the src folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Now the imports will clear up and find the right modules!
from models.toxicity_model import classify_text as predict_toxicity
from database.db import get_connection

def classify_text(text):
    """
    Integrates the DistilBERT model into the existing classify_text() function.
    Evaluates text and categorizes it.
    """
    # Call the integrated DistilBERT model function
    toxicity_score, is_abuse = predict_toxicity(text)

    if is_abuse:
        category = "abusive"
    else:
        category = "safe"

    return {
        "category": category,
        "toxicity_score": toxicity_score
    }

if __name__ == "__main__":
    text = input("Enter a post (Hinglish/English): ")
    output = classify_text(text)
    
    print("\n--- Model Output ---")
    print(output)

    # Save to database if flagged
    if output["category"] == "abusive":
        try:
            db = get_connection()
            cursor = db.cursor()
            
            insert_query = """
                INSERT INTO flagged_posts (content, cleaned_content, toxicity_score, is_abuse)
                VALUES (%s, %s, %s, %s)
            """
            # Using the text as both raw and clean for this standalone test script
            cursor.execute(insert_query, (text, text, output["toxicity_score"], True))
            db.commit()
            print("⚠️ Flagged post successfully logged to MySQL database!")
            
            cursor.close()
            db.close()
        except Exception as e:
            print(f"❌ Database logging failed: {e}")