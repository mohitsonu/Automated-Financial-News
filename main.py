import feedparser
import requests
from urllib.parse import quote_plus
import time
from datetime import datetime

# ---------- CONFIG ----------
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
STOCKS = ["Reliance", "Suzlon", "IOB Bank", "Eternal"]
TOPICS = ["Stock Market", "World Market", "Results", "Political", "Geopolitical", "Sector", "Economy"]
UPDATE_INTERVAL = 3600  # 1 hour in seconds
TOP_N = 3  # Top 3 news per stock/topic
MESSAGE_GAP = 30  # seconds between messages

# Emoji headings for topics
EMOJI_HEADINGS = {
    "Stock Market": "📈 STOCK MARKET",
    "World Market": "🌎 WORLD MARKET",
    "Results": "📝 RESULTS",
    "Political": "🏛️ POLITICAL",
    "Geopolitical": "🗺️ GEOPOLITICAL",
    "Sector": "🏢 SECTOR",
    "Economy": "💹 ECONOMY"
}

# ---------- FUNCTIONS ----------
def shorten_url(url):
    """Shorten URLs using TinyURL API"""
    try:
        resp = requests.get(f"http://tinyurl.com/api-create.php?url={url}")
        if resp.ok:
            return resp.text
        return url
    except:
        return url

def fetch_news(term, top_n=TOP_N):
    """Fetch top N news headlines for a given search term"""
    encoded_term = quote_plus(term)
    url = f"https://news.google.com/rss/search?q={encoded_term}+site:moneycontrol.com+OR+site:economictimes.indiatimes.com+OR+site:business-standard.com"
    feed = feedparser.parse(url)
    news_list = []

    for idx, entry in enumerate(feed.entries[:top_n], start=1):
        title = entry.title
        link = shorten_url(entry.link)
        # Detect source
        source_name = getattr(entry, "source", None)
        if source_name:
            source_name = source_name.title
        else:
            # fallback: detect from link
            if "moneycontrol" in entry.link:
                source_name = "Moneycontrol"
            elif "economictimes" in entry.link:
                source_name = "Economic Times"
            elif "business-standard" in entry.link:
                source_name = "Business Standard"
            else:
                source_name = "Unknown"

        # Published time
        published = getattr(entry, "published", None)
        if published and hasattr(entry, "published_parsed"):
            published_dt = datetime(*entry.published_parsed[:6])
            published_str = published_dt.strftime("%d-%m-%Y %I:%M %p")
        else:
            published_str = "Unknown"

        news_item = f"{idx}️⃣ {title} — {source_name}\n_Read more:_ {link}\n🕒 Published: {published_str}"
        news_list.append(news_item)

    return news_list

