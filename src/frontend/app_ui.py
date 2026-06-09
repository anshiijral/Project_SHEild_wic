import streamlit as st
import sys
import os

# Allow importing from the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import flag_and_store_post
from database.db import get_connection

st.set_page_config(page_title="Project SHEild", page_icon="🛡️", layout="wide")

st.title("🛡️ Project SHEild — Hinglish Abuse Detection Pipeline")
st.markdown("Enter text below (English or Hinglish) to run it through the cleaning and DistilBERT classification pipeline.")

# Layout splits: Input on left, Live Database logs on right
col1, col2 = st.columns(2)

with col1:
    st.subheader("Analyze New Post")
    user_input = st.text_area("Post Content", placeholder="e.g., Ye post bohot kharab hai...")
    
    if st.button("Submit & Analyze", type="primary"):
        if user_input.strip():
            with st.spinner("Processing through DistilBERT..."):
                # Run the complete pipeline we built earlier
                flag_and_store_post(user_input)
            st.success("Post processed and recorded in database!")
        else:
            st.warning("Please enter some text first.")

with col2:
    st.subheader("📜 Live Moderation Database Logs")
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, content, cleaned_content, toxicity_score, is_abuse, created_at FROM flagged_posts ORDER BY id DESC LIMIT 5")
        records = cursor.fetchall()
        cursor.close()
        db.close()
        
        if records:
            for record in records:
                status_color = "🔴 Flagged" if record['is_abuse'] else "🟢 Clean"
                with st.expander(f"Post #{record['id']} - {status_color} (Score: {record['toxicity_score']:.2f})"):
                    st.write(f"**Original:** {record['content']}")
                    st.write(f"**Cleaned (Hinglish):** {record['cleaned_content']}")
                    st.caption(f"Timestamp: {record['created_at']}")
        else:
            st.info("No posts stored in the database yet.")
    except Exception as e:
        st.error(f"Could not load logs: {e}")