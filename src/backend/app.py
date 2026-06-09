import sys
from database.db import get_connection
from backend.clean_text import normalize_hinglish as clean_text

# Import your newly integrated function directly from the models package
from models.toxicity_model import classify_text 

def flag_and_store_post(raw_content):
    # 1. Run the text through your Hinglish cleaner
    cleaned_content = clean_text(raw_content)
    
    # 2. Run it through the newly integrated DistilBERT function
    toxicity_score, is_abuse = classify_text(cleaned_content)
    
    # 3. Commit the metrics directly to your MySQL database
    try:
        db = get_connection()
        cursor = db.cursor()
        
        insert_query = """
            INSERT INTO flagged_posts (content, cleaned_content, toxicity_score, is_abuse)
            VALUES (%s, %s, %s, %s)
        """
        data_to_insert = (raw_content, cleaned_content, toxicity_score, is_abuse)
        
        cursor.execute(insert_query, data_to_insert)
        db.commit()
        
        print(f"Successfully processed post!")
        print(f"-> Score: {toxicity_score:.4f} | Status: {'⚠️ Flagged' if is_abuse else '✅ Clean'}\n")
        
        cursor.close()
        db.close()
        
    except Exception as e:
        print(f"Error saving to database: {e}")

if __name__ == "__main__":
    sample_post = "Ye post bohot kharab hai and full of hate."
    print(f"Testing pipeline with sample text: '{sample_post}'")
    flag_and_store_post(sample_post)