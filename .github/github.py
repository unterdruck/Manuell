import requests
from bs4 import BeautifulSoup

# Konfiguration
START_URL = "https://www.research-tree.com/newsfeed?keyAnnouncement=true&resultsTradingUpdate=true"
KEYWORDS = [
    "ahead of consensus expectations",
    "ahead of market expactations",
    "ahead of market",
    "guidance raised",
    "expected to exceed exp"
]

# Dein Discord Webhook
DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1367401881340608553/08ccNmZw8jLslzOBkJljWT3Q06HtjIzekmvDGR8u3Qf43azd-QOm20-bdcEvpPRHpLNd"

def send_to_discord(message: str):
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
    for url in get_article_links():
        if url in visited:
            continue
        visited.add(url)
        try:
            article = requests.get(url).text.lower()
            found = [kw for kw in KEYWORDS if kw in article]
            if found:
                message = f"✅ Gefunden: {', '.join(found)}\n🔗 {url}"
                send_to_discord(message)
        except Exception as e:
            print(f"Fehler bei {url}: {e}")

if __name__ == "__main__":
    check_articles()
