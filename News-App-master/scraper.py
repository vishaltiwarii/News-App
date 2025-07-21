import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

STATE_URLS = {
      "andhra-pradesh": "https://timesofindia.indiatimes.com/india/andhra-pradesh",
    "arunachal-pradesh": "https://timesofindia.indiatimes.com/india/arunachal-pradesh",
    "assam": "https://timesofindia.indiatimes.com/india/assam",
    "bihar": "https://timesofindia.indiatimes.com/india/bihar",
    "chhattisgarh": "https://timesofindia.indiatimes.com/india/chhattisgarh",
    "delhi": "https://timesofindia.indiatimes.com/india/delhi",
    "goa": "https://timesofindia.indiatimes.com/india/goa",
    "gujarat": "https://timesofindia.indiatimes.com/india/gujarat",
    "haryana": "https://timesofindia.indiatimes.com/india/haryana",
    "himachal-pradesh": "https://timesofindia.indiatimes.com/india/himachal-pradesh",
    "jharkhand": "https://timesofindia.indiatimes.com/india/jharkhand",
    "karnataka": "https://timesofindia.indiatimes.com/india/karnataka",
    "kerala": "https://timesofindia.indiatimes.com/india/kerala",
    "madhya-pradesh": "https://timesofindia.indiatimes.com/india/madhya-pradesh",
    "maharashtra": "https://timesofindia.indiatimes.com/india/maharashtra",
    "manipur": "https://timesofindia.indiatimes.com/india/manipur",
    "meghalaya": "https://timesofindia.indiatimes.com/india/meghalaya",
    "mizoram": "https://timesofindia.indiatimes.com/india/mizoram",
    "nagaland": "https://timesofindia.indiatimes.com/india/nagaland",
    "odisha": "https://timesofindia.indiatimes.com/india/odisha",
    "punjab": "https://timesofindia.indiatimes.com/india/punjab",
    "rajasthan": "https://timesofindia.indiatimes.com/india/rajasthan",
    "sikkim": "https://timesofindia.indiatimes.com/india/sikkim",
    "tamil-nadu": "https://timesofindia.indiatimes.com/india/tamil-nadu",
    "telangana": "https://timesofindia.indiatimes.com/india/telangana",
    "tripura": "https://timesofindia.indiatimes.com/india/tripura",
    "uttar-pradesh": "https://timesofindia.indiatimes.com/india/uttar-pradesh",
    "uttarakhand": "https://timesofindia.indiatimes.com/india/uttarakhand",
    "west-bengal": "https://timesofindia.indiatimes.com/india/west-bengal"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

def scrape_news(state):
    url = STATE_URLS.get(state.lower())
    if not url:
        return {"error": "State not found"}

    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        return {"error": f"Failed to fetch news, status code: {response.status_code}"}

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract titles and images
    articles = soup.find_all("span", class_="w_tle")
    images = soup.find_all("img")

    news_list = []
    for article, image in zip(articles[:12], images[:12]):
        news_item = {
            "title": article.text.strip(),
            "image": image["src"] if "src" in image.attrs else "https://via.placeholder.com/300"
        }
        news_list.append(news_item)

    return news_list

@app.route('/get_news', methods=['GET'])
def get_news():
    state = request.args.get("state", "").lower()
    news_data = scrape_news(state)
    return jsonify(news_data)

if __name__ == "__main__":
    app.run(debug=True)
