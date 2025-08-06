from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
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

        # 레포지토리 이름 추출
        repo_name = latest.link.split("/")[4]

        # 날짜 포맷 변환
        updated_time = datetime.strptime(latest.updated, "%Y-%m-%dT%H:%M:%SZ")
        formatted_time = updated_time.strftime("%Y-%m-%d %H:%M")

        # 메시지 구성
        message = (
            f"📢 [{repo_name}] 새로운 버전이 나왔어요!💌\n"
            f"🔗 <{latest.link}>\n"
            f"📝 {latest.title}\n"
            f"📅 {formatted_time}"
        )

        # 디스코드 전송
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

scheduler = BackgroundScheduler()
scheduler.add_job(func=check_github_release, trigger="interval", minutes=5)
scheduler.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
