from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": [
    "https://will11521.github.io",
    "https://will11521.github.io/dreamsynth-frontend"
]}})
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "🌙 DreamSynth backend is live."

@app.route("/generate", methods=["POST"])
def generate_dream():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "No prompt provided."}), 400

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a dream interpreter and creator. Based on what the user says, you describe a dream they might have had."
            },
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        dream = result["choices"][0]["message"]["content"].strip()
        return jsonify({"dream": dream})
    except Exception as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 500

# Run app on appropriate port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=False, host="0.0.0.0", port=port)