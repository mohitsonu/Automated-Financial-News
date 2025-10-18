from flask import Flask, jsonify
import feedparser
import requests
from urllib.parse import quote_plus
import os

app = Flask(__name__)

# ---------- CONFIG ----------
BOT_TOKEN = os.getenv("BOT_TOKEN", "8379848942:AAE09WVTLDwa85CYSl5BvEGtYhyB4QTGYhU")
CHAT_ID = os.getenv("CHAT_ID", "-1002904181387")
STOCKS = ["Saatvik Green Energy", "Avantel", "Suzlon", "IOB Bank", "Eternal"]
TOPICS = ["Stock Market", "World Market", "Results", "Political", "Geopolitical", "Sector", "Economy"]

# ---------- HELPERS ----------
def shorten_url(url):
    """Shorten URLs using TinyURL API"""
    try:
        resp = requests.get(f"http://tinyurl.com/api-create.php?url={url}")
        if resp.ok:
            return resp.text
        return url
    except:
        return url

def fetch_news(term, top_n=3):
    """Fetch top N news headlines for a given search term"""
    encoded_term = quote_plus(term)
    url = f"https://news.google.com/rss/search?q={encoded_term}+site:moneycontrol.com+OR+site:economictimes.indiatimes.com+OR+site:business-standard.com"
    feed = feedparser.parse(url)
    news_list = []
    for entry in feed.entries[:top_n]:
        title = entry.title
        link = shorten_url(entry.link)
        news_list.append(f"• {title}\n{link}")
    return news_list

def send_telegram_message(message):
    """Send message to Telegram group with previews enabled"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    resp = requests.post(url, data=data)
    return resp.status_code, resp.text

# ---------- ROUTES ----------
@app.route('/')
def home():
    return "✅ Automated Financial News Bot is Live on Render!"

@app.route('/fetch_news')
def fetch_and_send_news():
    final_message = ""
    for term in STOCKS + TOPICS:
        news = fetch_news(term)
        if news:
            final_message += f"📰 <b>{term.upper()}</b> — Top news:\n" + "\n".join(news) + "\n\n"
        else:
            final_message += f"⚠️ <b>{term.upper()}</b>: No news found\n\n"

    MAX_LEN = 4000
    for i in range(0, len(final_message), MAX_LEN):
        chunk = final_message[i:i+MAX_LEN]
        status, resp_text = send_telegram_message(chunk)
        print(f"Sent chunk ({status}): {resp_text}")

    return jsonify({"status": "success", "message": "News sent to Telegram"})

@app.route('/test_telegram')
def test_telegram():
    """Send a simple test message to verify Telegram connection"""
    msg = "🚀 Test message from Render deployed Financial News Bot!"
    status, resp = send_telegram_message(msg)
    return jsonify({"status": status, "response": resp})

# ---------- ENTRY POINT ----------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
