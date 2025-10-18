import feedparser
import requests
from urllib.parse import quote_plus
from datetime import datetime
import pytz
import os

# ---------- CONFIG ----------
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

STOCKS = [
    "Saatvik Green Energy",
    "Avantel",
    "Suzlon",
    "IOB Bank",
    "Eternal"
]

TOPICS = [
    "Stock Market",
    "World Market",
    "Results",
    "Political",
    "Geopolitical",
    "Sector",
    "Economy"
]

# ---------- EMOJIS FOR SECTIONS ----------
SECTION_EMOJIS = {
    "Stock Market": "💹",
    "World Market": "🌎",
    "Results": "📝",
    "Political": "🏛️",
    "Geopolitical": "🗺️",
    "Sector": "🏢",
    "Economy": "📊"
}

# ---------- HELPERS ----------
def shorten_url(url):
    """Shorten URLs using TinyURL API"""
    try:
        resp = requests.get(f"http://tinyurl.com/api-create.php?url={url}", timeout=10)
        if resp.ok:
            return resp.text
    except Exception:
        pass
    return url


def format_pub_date(entry):
    """Convert entry.published to readable IST format"""
    try:
        utc_time = datetime(*entry.published_parsed[:6])
        ist = pytz.timezone("Asia/Kolkata")
        return utc_time.astimezone(ist).strftime("%d-%m-%Y %I:%M %p")
    except Exception:
        return "Unknown time"


def fetch_news(term, top_n=3):
    """Fetch top N latest Google News headlines"""
    encoded_term = quote_plus(term)
    url = f"https://news.google.com/rss/search?q={encoded_term}+site:moneycontrol.com+OR+site:economictimes.indiatimes.com+OR+site:business-standard.com"
    feed = feedparser.parse(url)
    news_items = []

    for i, entry in enumerate(feed.entries[:top_n]):
        title = entry.title
        link = shorten_url(entry.link)
        source = entry.get("source", {}).get("title", "")
        published = format_pub_date(entry)
        news_items.append(f"{i+1}️⃣ {title} — {source or entry.link.split('/')[2]}\n_Read more:_ {link}\n🕒 Published: {published}\n")

    return news_items


def send_telegram_message(message):
    """Send formatted message to Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        r = requests.post(url, data=payload, timeout=10)
        if r.ok:
            print("✅ Message sent successfully!")
        else:
            print(f"⚠️ Telegram error: {r.json()}")
    except Exception as e:
        print(f"⚠️ Send error: {e}")


# ---------- MAIN ----------
# ---------- MAIN ----------
def main():
    print("🚀 Fetching live financial news...\n")

    for topic in STOCKS + TOPICS:
        emoji = SECTION_EMOJIS.get(topic, "📰")
        news_list = fetch_news(topic)
        if news_list:
            header = f"{emoji} <b>{topic.upper()}</b> — Top 3 News\n"
            message = header + "\n".join(news_list)
        else:
            message = f"⚠️ No recent news found for <b>{topic.upper()}</b>\n"

        send_telegram_message(message)
        print(f"⏳ Waiting 30 seconds before sending next topic...")
        time.sleep(30)  # <-- 30-second gap between messages



if __name__ == "__main__":
    main()
    
