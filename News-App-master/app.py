import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import scrape_news

app = Flask(__name__)
CORS(app)

@app.route("/get_news", methods=["GET"])
def get_news():
    state = request.args.get("state", "").strip().lower()
    
    if not state:
        return jsonify({"error": "State parameter is required"}), 400

    try:
        news = scrape_news(state)
        return jsonify(news)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))  # Use Railway's PORT
    app.run(host="0.0.0.0", port=PORT)
