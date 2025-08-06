from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import feedparser
import requests
import os

app = Flask(__name__)

DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = os.environ.get("DISCORD_CHANNEL_ID")
RSS_URL = "https://github.com/roflmuffin/CounterStrikeSharp/releases.atom"

last_release_id = None

def check_github_release():
    global last_release_id
    feed = feedparser.parse(RSS_URL)
    latest = feed.entries[0]
    if latest.id != last_release_id:
        last_release_id = latest.id
        message = f"📢 **New Release**\n🔗 {latest.link}\n📝 {latest.title}"
        requests.post(
            f"https://discord.com/api/channels/{DISCORD_CHANNEL_ID}/messages",
            headers={
                "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
                "Content-Type": "application/json"
            },
            json={"content": message}
        )

@app.route('/')
def index():
    return "Bot is running!"

# 주기적인 작업 스케줄링
scheduler = BackgroundScheduler()
scheduler.add_job(func=check_github_release, trigger="interval", minutes=5)
scheduler.start()
