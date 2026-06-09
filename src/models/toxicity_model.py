import os
from transformers import pipeline

# 1. Initialize the Hugging Face pipeline once when the module loads
# We use 'unitary/toxic-bert', which is fine-tuned specifically for detecting online toxicity/abuse
try:
    print("🤖 Loading DistilBERT classification model...")
    classifier = pipeline(
        "text-classification", 
        model="unitary/toxic-bert",
        framework="pt"  # Forces PyTorch usage
    )
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Failed to load model pipeline: {e}")
    classifier = None

def classify_text(text):
    """
    Integrates the DistilBERT model to evaluate and classify incoming text.
    
    Parameters:
    text (str): The preprocessed text string.
    
    Returns:
    tuple: (toxicity_score as float, is_abuse as bool)
    """
    # Fail-safe for empty or whitespace-only inputs
    if not text or not text.strip():
        return 0.0, False

    if classifier is None:
        print("⚠️ Model pipeline is unavailable. Returning fallback safe values.")
        return 0.0, False

    try:
        # 2. Feed the text to the model
        predictions = classifier(text)
        result = predictions[0]  # Grab the first output dictionary
        
        # 3. Extract the confidence score
        toxicity_score = float(result['score'])
        label = result['label'].lower()
        
        # 4. Apply evaluation logic to determine the abuse flag.
        # 'toxic-bert' uses labels like 'toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate'.
        # If the label indicates any toxic trait, or if confidence score passes a 0.5 threshold, we flag it.
        toxic_labels = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate', 'label_1']
        
        is_abuse = False
        if label in toxic_labels or toxicity_score > 0.5:
            is_abuse = True
            
        return toxicity_score, is_abuse

    except Exception as e:
        print(f"❌ Error during model execution: {e}")
        return 0.0, False