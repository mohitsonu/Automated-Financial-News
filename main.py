import feedparser
from urllib.parse import quote_plus
import requests
from datetime import datetime
import re
from flask import Flask

# ========== CONFIGURATION ==========
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"  # e.g. "-1002904181387"
stocks = ["Reliance", "IRFC", "IRCTC", "Suzlon", "IOB Bank", "Eternal"]
topics = ["Stock Market", "World Market", "Results", "Political", "Geopolitical", "Sector", "Economy"]
TOP_N = 3  # Top 3 news per category

app = Flask(__name__)

# ========== UTILITIES ==========
def escape_markdown(text):
    """Escape characters for Telegram MarkdownV2"""
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(r'([{}])'.format(re.escape(escape_chars)), r'\\\1', text)

def shorten_url(url):
    """Shorten URLs using TinyURL"""
    try:
        r = requests.get(f"http://tinyurl.com/api-create.php?url={url}", timeout=5)
        if r.status_code == 200:
            return r.text.strip()
    except:
        pass
    return url

def format_news_card(term, entries):
    """Format news for one topic/stock as a Telegram card"""
    now = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    card_lines = [f"📰 *{escape_markdown(term.upper())}* — *Top {TOP_N} Headlines*"]

    for i, entry in enumerate(entries[:TOP_N], 1):
        title = escape_markdown(entry.title)
        link = shorten_url(entry.link)
        published = ""
        if hasattr(entry, "published_parsed"):
            published_dt = datetime(*entry.published_parsed[:6])
            published = published_dt.strftime("%d-%m-%Y %I:%M %p")
        card_lines.append(f"\n{i}️⃣ *{title}*")
        card_lines.append(f"🔗 [Read More]({link})")
        if published:
            card_lines.append(f"🕒 _Published:_ {published}")

    card_lines.append(f"\n⏳ *Last Updated:* {now}")
    return "\n".join(card_lines)

# ========== CORE FUNCTIONS ==========
def fetch_news_for_term(term):
    """Fetch and format top headlines for a given term"""
    encoded_term = quote_plus(term)
    url = f"https://news.google.com/rss/search?q={encoded_term}+site:moneycontrol.com+OR+site:economictimes.indiatimes.com+OR+site:business-standard.com"
    feed = feedparser.parse(url)
    if not feed.entries:
        return None
    return format_news_card(term, feed.entries)

def send_to_telegram(message):
    """Send message to Telegram with MarkdownV2"""
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
            print("✅ Message sent to Telegram")
        else:
            print(f"⚠️ Telegram send failed: {resp.text}")
    except Exception as e:
        print(f"❌ Error sending to Telegram: {e}")

# ========== FLASK ROUTES ==========
@app.route('/')
def home():
    return "🚀 IKT Market News Bot is Running Successfully!"

@app.route('/fetch_news')
def fetch_news():
    """Render Cron endpoint — sends all news updates"""
    for term in stocks + topics:
        print(f"🕒 Fetching {term}...")
        msg = fetch_news_for_term(term)
        if msg:
            send_to_telegram(msg)
    return "✅ All news sent successfully to Telegram!"

# ========== ENTRY POINT ==========
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
