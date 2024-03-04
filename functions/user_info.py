import json
import requests
import logging
import time
from config import BOT_TOKEN
import os

channel = "@codeforces_official"

def get_base_information(handle):
    """ Ответ полчуим в формате:
            {
        "status": "OK",
        "result": [
            {
                "lastName": "Gareev",
                "country": "Россия",
                "lastOnlineTimeSeconds": 1709322224,
                "city": "Набережные Челны",
                "rating": 1027,
                "friendOfCount": 7,
                "titlePhoto": "https://userpic.codeforces.org/2128075/title/3130227c20c51c60.jpg",
                "handle": "gareeeeeeeeeeeeeeeev",
                "avatar": "https://userpic.codeforces.org/2128075/avatar/70c33308f7adddc1.jpg",
                "firstName": "Amir",
                "contribution": 0,
                "organization": "МАОУ Лицей № 78",
                "rank": "новичок",
                "maxRating": 1027,
                "registrationTimeSeconds": 1626624570,
                "maxRank": "новичок"
            }
        ]
    }
    """
    link = f'https://codeforces.com/api/user.info?handles={handle}'
    response = requests.get(link)
    if response:
        return response.json()
    else:
        print("Ошибка выполнения запроса:")
        print(link)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return None


def check_posts(TOKEN, CHANNEL_ID, limit=2) -> None:
    print(f"https://api.telegram.org/bot{TOKEN}/getChatHistory?chat_id={CHANNEL_ID}&limit={limit}")
    response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getChatHistory?chat_id={CHANNEL_ID}&limit={limit}")
    data = response.json()
    for message in data["result"]["messages"]:
        if "will take place" in message.get("message", ""):
            print(message.get("message", ""))


if __name__ == "__main__":
    check_posts(BOT_TOKEN, channel)
