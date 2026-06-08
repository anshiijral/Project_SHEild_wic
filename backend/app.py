from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)


def classify_text(text):
    """
    Temporary rule-based classifier.
    Replace with DistilBERT later.
    """

    text = text.lower()

    harmful_phrases = [
        "women can't code",
        "girls can't code",
        "ladkiyan coding nahi kar sakti",
        "women belong in the kitchen",
        "rape",
        "acid attack",
        "kill her"
    ]

    for phrase in harmful_phrases:
        if phrase in text:
            return 92, "Gender-Based Abuse"

    return 10, "Safe"


def get_severity(score):
    if score >= 90:
        return "Extreme"
    elif score >= 70:
        return "Harsh"
    elif score >= 40:
        return "Offensive"
    else:
        return "Mild"


@app.route("/")
def home():
    return "Project SHEild Backend Running!"


@app.route("/analyze", methods=["GET", "POST"])
def analyze():

    if request.method == "GET":
        return jsonify({
            "message": "Analyze endpoint working"
        })

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No JSON data received"
        }), 400

    text = data.get("text", "")

    score, category = classify_text(text)

    severity = get_severity(score)

    warning = score >= 40

    return jsonify({
        "text": text,
        "score": score,
        "category": category,
        "severity": severity,
        "warning": warning,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


if __name__ == "__main__":
    app.run(debug=True)