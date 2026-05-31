import os
import re
import requests
from bs4 import BeautifulSoup

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

    response = requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers=headers,
        json=data,
        timeout=30
    )

    print(f"LINE status = {response.status_code}")
    print(response.text)

    response.raise_for_status()


def get_update_text():

    response = requests.get(
        URL,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    text = soup.get_text()

    match = re.search(
        r"最終更新日：([0-9/ :]+)",
        text
    )

    if match:
        return match.group(1).strip()

    return None


latest = get_update_text()

if latest is None:
    raise Exception("Không tìm thấy 最終更新日 trên website")

old = ""

if os.path.exists(SAVE_FILE):

    with open(
        SAVE_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        old = f.read().strip()

print(f"latest = [{latest}]")
print(f"old    = [{old}]")

if latest != old:

    message = (
        "RICOH抽選ページ更新！\n\n"
        f"最終更新日: {latest}\n\n"
        f"{URL}"
    )

    send_line(message)

    with open(
        SAVE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(latest)

    print("LINE sent")
    print(f"saved = {latest}")

else:

    print("No change")
