import feedparser
import requests
from urllib.parse import quote_plus
from datetime import datetime, timedelta
import pytz
import os
import time
import json

# Bot credentials
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def load_config():
    # Load my custom stocks and topics
    try:
        with open('config.json', 'r') as file:
            data = json.load(file)
        stocks = data.get('stocks', [])
        topics = data.get('topics', [])
        return stocks, topics
    except FileNotFoundError:
        print("Config file missing! Using defaults...")
        return [], []
    except:
        print("Error reading config file")
        return [], []

my_stocks, my_topics = load_config()

# Different emojis for different news categories
emojis = {
    "Stock Market": "💹",
    "World Market": "🌎", 
    "Results": "📝",
    "Political": "🏛️",
    "Geopolitical": "🗺️",
    "Sector": "🏢",
    "Economy": "📊"
}

def make_url_short(url):
    # Using tinyurl to make links shorter
    try:
        response = requests.get(f"http://tinyurl.com/api-create.php?url={url}", timeout=10)
        if response.status_code == 200:
            return response.text
    except:
        pass
    return url


def convert_to_ist(entry):
    # Convert published time to IST
    try:
        utc_dt = datetime(*entry.published_parsed[:6])
        ist_tz = pytz.timezone("Asia/Kolkata")
        ist_dt = utc_dt.astimezone(ist_tz)
        return ist_dt.strftime("%d-%m-%Y %I:%M %p")
    except:
        return "Time not available"

def check_if_recent(entry, days=2):
    # Only show news from last 2 days
    try:
        if not entry.published_parsed:
            return False
        
        news_time = datetime(*entry.published_parsed[:6])
        now = datetime.now()
        cutoff = now - timedelta(days=days)
        
        return news_time >= cutoff
    except:
        return False


def get_news_for_topic(search_term, count=3):
    # Get news from Google RSS feed
    search_query = quote_plus(search_term)
    rss_url = f"https://news.google.com/rss/search?q={search_query}+site:moneycontrol.com+OR+site:economictimes.indiatimes.com+OR+site:business-standard.com"
    
    feed = feedparser.parse(rss_url)
    news_list = []
    
    # Filter recent news only
    recent_news = [item for item in feed.entries if check_if_recent(item)]
    
    for idx, item in enumerate(recent_news[:count]):
        headline = item.title
        url = make_url_short(item.link)
        source = item.get("source", {}).get("title", "")
        pub_time = convert_to_ist(item)
        
        news_item = f"{idx+1}️⃣ {headline} — {source or item.link.split('/')[2]}\n_Read more:_ {url}\n🕒 Published: {pub_time}\n"
        news_list.append(news_item)

    return news_list


def send_to_telegram(msg):
    # Send message to my telegram chat
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    
    try:
        response = requests.post(api_url, data=data, timeout=10)
        if response.ok:
            print("Message sent successfully!")
        else:
            print(f"Telegram API error: {response.json()}")
    except Exception as e:
        print(f"Failed to send message: {e}")

def run_bot():
    print("Starting financial news bot...\n")

    all_topics = my_stocks + my_topics
    
    for topic in all_topics:
        topic_emoji = emojis.get(topic, "�")
        news_items = get_news_for_topic(topic)
        
        if news_items:
            header = f"{topic_emoji} <b>{topic.upper()}</b> — Top 3 News\n"
            full_message = header + "\n".join(news_items)
        else:
            full_message = f"⚠️ No recent news found for <b>{topic.upper()}</b>\n"

        send_to_telegram(full_message)
        print(f"Sent news for {topic}, waiting 30 seconds...")
        time.sleep(30)  # Wait between messages

if __name__ == "__main__":
    run_bot()
    
