import feedparser
from urllib.parse import quote_plus
import requests
from datetime import datetime
from flask import Flask
import re

# ------------------ Configuration ------------------
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"
stocks = ["Reliance", "IRFC", "IRCTC", "Suzlon", "IOB Bank", "Eternal"]
topics = ["Stock Market", "World Market", "Results", "Political", "Geopolitical", "Sector", "Economy"]
TOP_N = 3

app = Flask(__name__)

# ------------------ Helpers ------------------
def escape_markdown(text):
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(r'([{}])'.format(re.escape(escape_chars)), r'\\\1', text)

def shorten_url(url):
    try:
        resp = requests.get(f"http://tinyurl.com/api-create.php?url={url}")
        if resp.status_code == 200:
            return resp.text
    except:
        pass
    return url

def fetch_news_for_term(term):
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
        published_str = ""
        if entry.get("published_parsed"):
            published_dt = datetime(*entry.published_parsed[:6])
            published_str = published_dt.strftime("%d-%m-%Y %I:%M %p")
        message_lines.append(f"{i}️⃣ *{title}* — _{source}_\n🔗 [Read more]({link})")
        if published_str:
            message_lines.append(f"   ⏰ Published: {published_str}")
    now = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    message_lines.append(f"⏳ Updated: {now}")
    return "\n".join(message_lines)

def send_to_telegram(message):
    try:
        resp = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": message,
                "parse_mode": "MarkdownV2",
                "disable_web_page_preview": False
            }
        )
        if resp.status_code == 200:
            print("✅ Telegram message sent successfully!")
        else:
            print(f"⚠️ Telegram send failed: {resp.json()}")
    except Exception as e:
        print(f"⚠️ Exception sending to Telegram: {e}")

# ------------------ Routes ------------------
@app.route('/')
def home():
    return "IKT News Bot is running! 🚀"

@app.route('/fetch_news')
def fetch_news_route():
    for term in stocks + topics:
        message = fetch_news_for_term(term)
        if message:
            send_to_telegram(message)
    return "✅ News sent to Telegram!"

# ------------------ Entry ------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
