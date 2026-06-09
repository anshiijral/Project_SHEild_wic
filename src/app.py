import sys
from database.db import get_connection

# 1. Import your actual Hinglish cleaning function (aliased as clean_text)
from backend.clean_text import clean_text

# 2. Import your actual DistilBERT toxicity model function
from models.toxicity_model import predict_toxicity 

def flag_and_store_post(raw_content):
    # 1. Preprocess Hinglish text
    cleaned_content = clean_text(raw_content)
    
    # 2. Run through DistilBERT model
    model_output = predict_toxicity(cleaned_content)
    
    # Safely handle the model's output layout
    if isinstance(model_output, dict):
        toxicity_score = float(model_output.get('score', 0.0))
        # Checks if label is toxic/abuse, or if the confidence score is high
        is_abuse = True if model_output.get('label') in ['toxic', 'abuse', 'LABEL_1'] or toxicity_score > 0.5 else False
    elif isinstance(model_output, tuple) and len(model_output) == 2:
        toxicity_score, is_abuse = model_output
    else:
        # Fallback if it returns a list of dicts (common in Hugging Face pipelines)
        if isinstance(model_output, list) and len(model_output) > 0:
            item = model_output[0]
            toxicity_score = float(item.get('score', 0.0))
            is_abuse = True if item.get('label') in ['toxic', 'abuse', 'LABEL_1'] or toxicity_score > 0.5 else False
        else:
            # Absolute fallback if type is unknown
            toxicity_score = 0.0
            is_abuse = False

    # 3. Store the clean, extracted values into MySQL
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
        
        print(f"Successfully processed and stored post!")
        print(f"-> Original: {raw_content}")
        print(f"-> Cleaned:  {cleaned_content}")
        print(f"-> Score:    {toxicity_score} | Status: {'⚠️ Flagged' if is_abuse else '✅ Clean'}\n")
        
        cursor.close()
        db.close()
        
    except Exception as e:
        print(f"Error saving to database: {e}")

if __name__ == "__main__":
    # Test case with real Hinglish content to verify the complete loop
    sample_post = "Ye post bohot kharab hai and full of hate."
    print(f"Processing sample post: '{sample_post}'")
    flag_and_store_post(sample_post)