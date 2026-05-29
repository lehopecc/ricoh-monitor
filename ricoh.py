import requests
from bs4 import BeautifulSoup
import re
import os

URL = "https://ricohimagingstore.com/Page/Feature/FeaturePage009.aspx"

LINE_ACCESS_TOKEN = os.environ["LINE_ACCESS_TOKEN"]
USER_ID = os.environ["LINE_USER_ID"]

SAVE_FILE = "last_update.txt"


def send_line(message):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }

    data = {
        "to": USER_ID,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers=headers,
        json=data
    )


def get_update_text():

    response = requests.get(URL)

    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text()

    match = re.search(
        r"最終更新日：([0-9/ :]+)",
        text
    )

    if match:
        return match.group(1).strip()

    return None


latest = get_update_text()

old = ""

if os.path.exists(SAVE_FILE):

    with open(SAVE_FILE, "r") as f:
        old = f.read().strip()

if latest != old:

    msg = (
        "RICOH抽選ページ更新！\n\n"
        f"最終更新日:\n{latest}\n\n"
        f"{URL}"
    )

    send_line(msg)

    with open(SAVE_FILE, "w") as f:
        f.write(latest)

    print("LINE sent")

else:

    print("No change")
