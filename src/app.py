import sys
import os
import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS

# Dynamically adds the current directory to the system path to prevent import crashes
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# --- INTEGRATED PIPELINE IMPORTS & ML FALLBACK GUARD ---
from backend.clean_text import clean_text

try:
    from models.toxicity_model import predict_toxicity
except ModuleNotFoundError:
    print("\n⚠️  'transformers' or 'torch' package not found in this environment.")
    print("⚠️  Activating simulation mode for predict_toxicity() to prevent a crash and enable testing...\n")
    
    # Simulation fallback that matches your pipeline's exact dictionary structure
    def predict_toxicity(text):
        lower_text = text.lower()
        # Simulates flag detection using standard trigger contexts
        if any(word in lower_text for word in ["hate", "kharab", "gali", "bad", "fuck", "stupid"]):
            return {"label": "toxic", "score": 0.88}
        return {"label": "clean", "score": 0.12}

app = Flask(__name__)
CORS(app)  # Allows Manleen's Streamlit frontend to make API calls safely

# --- DYNAMIC DATABASE INTEGRATION FUNCTION ---
def get_db_connection():
    """Attempts connection properties so it works seamlessly on your MacBook and team servers."""
    try:
        # 1. Try standard production/team credentials
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="password123",  # Hamsika's / Team's local password
            database="project_sheild"
        )
    except mysql.connector.errors.ProgrammingError as err:
        if err.errno == 1045:
            # 2. Local MacBook Fallback (Handles your local empty password requirement)
            try:
                print("⚠️ System database access denied. Applying local MacBook configuration...")
                return mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="", 
                    database="project_sheild"
                )
            except Exception as e:
                print(f"❌ Database connection failed completely: {e}")
                return None
        raise err

# --- HAMSIKA'S SEVERITY & EXPLAINABILITY LAYER ---
def calculate_severity_and_reason(score, label, cleaned_text):
    """Classifies severity tiers and creates the explainability text."""
    if not label or label in ['clean', 'LABEL_0'] or score < 0.4:
        return "Safe", "Content is clean and safe for the platform."
    
    # Keyword extraction loop for UI explainability
    triggers = [word for word in ["hate", "kharab", "gali", "bad"] if word in cleaned_text.lower()]
    reason = f"Flagged due to toxicity pattern matching. Trigger elements: {', '.join(triggers) if triggers else 'High toxicity confidence'}"
    
    if 0.4 <= score < 0.6:
        return "Mild", reason
    elif 0.6 <= score < 0.8:
        return "Harsh", reason
    else:
        return "Extreme", reason

# --- CORE BACKEND INTEGRATION ENDPOINTS ---

@app.route('/analyze', methods=['POST'])
def analyze_endpoint():
    """Main Orchestration Route: Input Text -> Preprocess -> Model Run -> Severity Logic -> DB Log"""
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({"error": "Missing 'content' field"}), 400
    
    raw_content = data['content']
    username = data.get('username', 'Anonymous')

    # Step 1: Run your normalization/cleaning and DistilBERT inference pipeline
    cleaned_content = clean_text(raw_content)
    model_output = predict_toxicity(cleaned_content)
    
    # Handle dictionary structure from Hugging Face layouts
    if isinstance(model_output, dict):
        toxicity_score = float(model_output.get('score', 0.0))
        label = model_output.get('label', 'clean')
    else:
        toxicity_score = 0.0
        label = 'clean'

    # Step 2: Severity Assessment & Abuse Flags
    is_abuse = True if label in ['toxic', 'abuse', 'LABEL_1'] or toxicity_score > 0.5 else False
    severity, reason = calculate_severity_and_reason(toxicity_score, label, cleaned_content)

    # Step 3: MySQL Data Insertion
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            insert_query = """
                INSERT INTO flagged_posts (username, content, cleaned_content, toxicity_score, severity, is_abuse, reason, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            data_to_insert = (username, raw_content, cleaned_content, toxicity_score, severity, is_abuse, reason, "Pending")
            cursor.execute(insert_query, data_to_insert)
            db.commit()
            cursor.close()
            db.close()
        except Exception as e:
            print(f"⚠️ Failed to save entry to MySQL database: {e}")
    
    # Output payload for Manleen's Streamlit frontend rendering
    return jsonify({
        "username": username,
        "original_content": raw_content,
        "cleaned_content": cleaned_content,
        "toxicity_score": toxicity_score,
        "severity": severity,
        "is_abuse": is_abuse,
        "explainability": reason,
        "status": "Pending"
    }), 200

@app.route('/get_flagged_posts', methods=['GET'])
def get_flagged_posts():
    """Pulls moderation history rows to feed the Streamlit Moderator Dashboard."""
    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database unavailable"}), 500
    
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM flagged_posts ORDER BY id DESC")
        posts = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(posts), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update_status', methods=['POST'])
def update_status():
    """Processes explicit dashboard action updates (Approve / Remove)."""
    data = request.get_json()
    post_id = data.get('id')
    new_status = data.get('status') 
    
    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database unavailable"}), 500
        
    try:
        cursor = db.cursor()
        cursor.execute("UPDATE flagged_posts SET status = %s WHERE id = %s", (new_status, post_id))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"success": True, "message": f"Status updated to {new_status}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Project SHEild Fully Integrated Backend Engine Starting Up...")
    app.run(host="127.0.0.1", port=5000, debug=True)