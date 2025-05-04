import os
import requests
from bs4 import BeautifulSoup

START_URL = "https://www.research-tree.com/newsfeed?keyAnnouncement=true&resultsTradingUpdate=true"
KEYWORDS = [
    "ahead of consensus expectations",
    "ahead of market expactations",
    "ahead of market",
    "guidance raised",
    "expected to exceed exp",
    "strong momentum into",
    "results ahead of expectations",
    "ahead of consensus expectations",
    "to deliver record underlying profits & earnings",
    "slightly ahead of boards expectations",
    "continued good momentum",
    "ahead of guidance",
    "guidance upgraded",
    "ahead of the market",
    "continued outperformance",
    "reiterates full year guidance",
    "following good start to the year",
    "full year performance ahead of market expectations",
    "record financial performance",
    "confidence in long term growth",
    "record revenue quarter",
]

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_to_discord(message: str):
    if not DISCORD_WEBHOOK_URL:
        print("❌ Webhook-URL fehlt!")
        return
    payload = {"content": message}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code != 204:
            print(f"⚠️ Discord-Fehler: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"❌ Fehler beim Senden an Discord: {e}")

def get_article_links():
    response = requests.get(START_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    return [
        "https://www.research-tree.com" + a["href"]
        for a in soup.find_all("a", href=True)
        if "/newsfeed/article/" in a["href"]
    ]

def check_articles():
    visited = set()
    found_any = False

    for url in get_article_links():
        if url in visited:
            continue
        visited.add(url)
        try:
            article = requests.get(url).text.lower()
            found = [kw for kw in KEYWORDS if kw in article]
            if found:
                found_any = True
                message = f"✅ Gefunden: {', '.join(found)}\n🔗 {url}"
                send_to_discord(message)
        except Exception as e:
            print(f"Fehler bei {url}: {e}")
    
    if not found_any:
        send_to_discord("🔍 Gesucht, aber keine passenden Keywords gefunden.")

if __name__ == "__main__":
    check_articles()
