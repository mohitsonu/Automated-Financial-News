import feedparser
from urllib.parse import quote_plus
import requests
from datetime import datetime
import time
from flask import Flask
import re
import threading
import os

# ------------------ Configuration ------------------
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # set as Render environment variable
CHAT_ID = os.environ.get("CHAT_ID")      # set as Render environment variable
stocks = ["Reliance", "IRFC", "IRCTC", "Suzlon", "IOB Bank", "Eternal"]
topics = ["Stock Market", "World Market", "Results", "Political", "Geopolitical", "Sector", "Economy"]
TOP_N = 3  # top 3 news
UPDATE_INTERVAL = 60*60  # 1 hour

app = Flask(__name__)

# ------------------ Helper Functions ------------------
def escape_markdown(text):
    """Escape characters for Telegram MarkdownV2"""
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(r'([{}])'.format(re.escape(escape_chars)), r'\\\1', text)

def shorten_url(url):
    """Use tinyurl.com to shorten URLs"""
    try:
        resp = requests.get(f"http://tinyurl.com/api-create.php?url={url}", timeout=5)
        if resp.status_code == 200:
            return resp.text
    except:
        pass
    return url

def fetch_news_for_term(term):
    """Fetch top N news for a single stock/topic"""
    encoded_term = quote_plus(term)
    url = f"https://news.google.com/rss/search?q={encoded_term}+site:moneycontrol.com+OR+site:economictimes.indiatimes.com+OR+site:business-standard.com"
    feed = feedparser.parse(url)
    if not feed.entries:
        return None

    message_lines = [f"📰 *{escape_markdown(term.upper())}* — Top {TOP_N} news:"]
    for i, entry in enumerate(feed.entries[:TOP_N], 1):
        title = escape_markdown(entry.title)
        source = escape_markdown(entry.get("source", {}).get("title", ""))
        link = shorten_url(entry.link)
        published = entry.get("published", "")
        try:
            published_dt = datetime(*entry.published_parsed[:6])
            published_str = published_dt.strftime("%d-%m-%Y %I:%M %p")
        except:
            published_str = ""
        message_lines.append(f"{i}️⃣ {title} — {source} — [Read more]({link})")
        if published_str:
            message_lines.append(f"   ⏰ Published: {published_str}")
    now = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    message_lines.append(f"⏳ Updated: {now}")
    return "\n".join(message_lines)

def send_to_telegram(message):
    """Send one message to Telegram"""
    try:
        resp = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": message,
                "parse_mode": "MarkdownV2",
                "disable_web_page_preview": False
            },
            timeout=10
        )
        if resp.status_code == 200:
            print("✅ Telegram message sent successfully!")
        else:
            print(f"⚠️ Telegram send failed: {resp.json()}")
    except Exception as e:
        print(f"⚠️ Exception sending to Telegram: {e}")

# ------------------ Main Loop ------------------
def run_bot():
    while True:
        print("🕒 Fetching live headlines from Google News...")
        for term in stocks + topics:
            message = fetch_news_for_term(term)
            if message:
                send_to_telegram(message)
                time.sleep(2)  # slight delay between messages
        print(f"⏳ Waiting {UPDATE_INTERVAL/60} minutes for next update...\n")
        time.sleep(UPDATE_INTERVAL)

# ------------------ Flask Routes ------------------
@app.route('/')
def home():
    return "IKT News Bot is running! 🚀"

@app.route('/run')
def run():
    thread = threading.Thread(target=run_bot)
    thread.start()
    return "Bot started! Fetching news every hour. 🕒"

# ------------------ Entry ------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
