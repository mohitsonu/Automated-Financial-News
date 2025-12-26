# 🤖 Automated Financial News Bot

> 📈 **Stay ahead of the market with automated financial news delivered straight to your Telegram!**

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-blue?logo=github-actions)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://python.org)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)](https://telegram.org)

---

## 🎯 What Does This Bot Do?

This intelligent bot automatically fetches and delivers **curated financial news** from top Indian business sources every few hours. No more manually checking multiple websites - get everything in one place!

### 📊 **News Categories**
| Category | Emoji | Description |
|----------|-------|-------------|
| Stock Market | 💹 | Latest market movements and trends |
| World Market | 🌎 | Global financial updates |
| Results | 📝 | Company earnings and quarterly results |
| Political | 🏛️ | Political news affecting markets |
| Geopolitical | 🗺️ | International events impacting economy |
| Sector | 🏢 | Industry-specific developments |
| Economy | 📊 | Economic indicators and policy changes |

---

## 🚀 Quick Start

### 1️⃣ **Clone & Setup**
```bash
git clone https://github.com/mohitsonu/Automated-Financial-News.git
cd Automated-Financial-News
pip install -r requirements.txt
```

### 2️⃣ **Configure Your Watchlist**
Edit `config.json` to customize your stocks and topics:

```json
{
  "stocks": [
    "Reliance",
    "TCS", 
    "HDFC Bank",
    "Infosys"
  ],
  "topics": [
    "Stock Market",
    "Results",
    "Economy"
  ]
}
```

### 3️⃣ **Setup Telegram Bot**
1. 💬 Message [@BotFather](https://t.me/botfather) on Telegram
2. 🆕 Create new bot with `/newbot`
3. 📝 Copy your bot token
4. 🆔 Get your chat ID from [@userinfobot](https://t.me/userinfobot)

### 4️⃣ **Configure GitHub Secrets**
Go to your repo → Settings → Secrets and variables → Actions

Add these secrets:
- `BOT_TOKEN`: Your Telegram bot token
- `CHAT_ID`: Your Telegram chat/group ID

---

## ⚙️ Configuration Options

### 🕐 **Schedule Settings**
Edit `.github/workflows/news-bot.yml` to change frequency:

| Frequency | Cron Expression | Description |
|-----------|----------------|-------------|
| Every 2 hours | `0 */2 * * *` | 🕐 12 times per day |
| Every 4 hours | `0 */4 * * *` | 🕓 6 times per day |
| Every 6 hours | `0 */6 * * *` | 🕕 4 times per day |
| Twice daily | `0 9,21 * * *` | 🌅🌙 9 AM & 9 PM |

### 📰 **News Sources**
The bot fetches from these trusted sources:
- 📊 **MoneyControl** - Market analysis and stock updates
- 💼 **Economic Times** - Business and economic news  
- 📈 **Business Standard** - Financial market coverage

---

## 🎨 Sample Output

```
💹 STOCK MARKET — Top 3 News

1️⃣ Sensex hits record high as IT stocks surge — Economic Times
Read more: https://tinyurl.com/xyz123
🕒 Published: 18-10-2025 02:30 PM

2️⃣ FII inflows boost market sentiment — MoneyControl  
Read more: https://tinyurl.com/abc456
🕒 Published: 18-10-2025 01:45 PM

3️⃣ Banking stocks show strong momentum — Business Standard
Read more: https://tinyurl.com/def789
🕒 Published: 18-10-2025 12:15 PM
```

---

## 🛠️ Advanced Features

### 🔧 **Customization Options**

<details>
<summary>📝 <strong>Modify News Count</strong></summary>

Change `top_n=3` in `main.py` to get more/fewer news items per topic:
```python
news_list = fetch_news(topic, top_n=5)  # Get 5 news items instead of 3
```
</details>

<details>
<summary>⏱️ <strong>Adjust Message Delays</strong></summary>

Modify the delay between messages in `main.py`:
```python
time.sleep(60)  # Wait 60 seconds instead of 30
```
</details>

<details>
<summary>🎯 <strong>Add Custom Topics</strong></summary>

Add your own search terms to `config.json`:
```json
{
  "topics": [
    "Cryptocurrency",
    "IPO",
    "Mutual Funds",
    "Gold Prices"
  ]
}
```
</details>

---

## 📱 Usage Examples

### 🏠 **Personal Use**
- Get morning market updates before work
- Stay informed about your portfolio stocks
- Receive evening market summaries

### 👥 **Group/Family Use**  
- Share financial news with investment club
- Keep family updated on market trends
- Discuss news in group chat alongside bot updates

### 💼 **Professional Use**
- Monitor sector-specific developments
- Track competitor company news
- Stay updated on regulatory changes

---

## 🔍 Troubleshooting

### ❌ **Common Issues**

<details>
<summary>🚫 <strong>Bot not sending messages</strong></summary>

**Check:**
1. ✅ BOT_TOKEN and CHAT_ID secrets are set correctly
2. ✅ Bot is added to your group/chat
3. ✅ GitHub Actions workflow is enabled
4. ✅ Check Actions tab for error logs
</details>

<details>
<summary>⏰ <strong>Messages not on schedule</strong></summary>

**Verify:**
1. ✅ Cron expression is correct in workflow file
2. ✅ GitHub Actions has proper permissions
3. ✅ Repository is not private (or has Actions enabled)
</details>

<details>
<summary>📰 <strong>No news found for topics</strong></summary>

**Try:**
1. ✅ Use broader search terms in config.json
2. ✅ Check if news sources are accessible
3. ✅ Verify internet connectivity in Actions logs
</details>

---

## 🤝 Contributing

Want to make this bot even better? Here's how:

### 🌟 **Feature Ideas**
- [ ] 📊 Add cryptocurrency news support
- [ ] 🌍 Include international markets
- [ ] 📈 Add price alerts functionality
- [ ] 🎨 Custom emoji themes
- [ ] 📅 Weekend/holiday scheduling
- [ ] 🔔 Breaking news notifications

### 🛠️ **How to Contribute**
1. 🍴 Fork the repository
2. 🌿 Create feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to branch (`git push origin feature/amazing-feature`)
5. 🔄 Open a Pull Request



## 🙏 Acknowledgments

- 🤖 **Telegram Bot API** - For seamless messaging
- 📰 **Google News RSS** - For news aggregation  
- ⚡ **GitHub Actions** - For free automation
- 🐍 **Python Community** - For amazing libraries

---

## 📞 Support

Having issues? Need help customizing? 

- 🐛 **Bug Reports**: [Open an Issue](https://github.com/mohitsonu/Automated-Financial-News/issues)
- 📧 **Direct Contact**: [mohitsonu33@gmail.com](mailto:mohitsonu33@gmail.com)
- 💬 **Join our Telegram Group**: [Financial News Discussion](https://t.me/+xdc0gly07a4xNzA1)

---

<div align="center">

### 🎉 **Happy Trading!** 📈

**Made with ❤️ for the financial community**

[![⭐ Star this repo](https://img.shields.io/github/stars/mohitsonu/Automated-Financial-News?style=social)](https://github.com/mohitsonu/Automated-Financial-News)
[![🍴 Fork this repo](https://img.shields.io/github/forks/mohitsonu/Automated-Financial-News?style=social)](https://github.com/mohitsonu/Automated-Financial-News/fork)

</div>

---

*💡 **Pro Tip**: Star this repo to stay updated with new features and improvements!*
