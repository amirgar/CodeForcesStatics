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


def get_statics() -> list:
    global user_handle
    user_handle = 'gareeeeeeeeeeeeeeeev'
    l = 0
    r = 10000
    #  Будем использовать бинарный поиск для оптимизации процесса
    while (r - l) > 1:
        mid = (l + r) // 2
        link = f'https://codeforces.com/api/user.status?handle={user_handle}&from={mid}&count=25'
        response = requests.get(link)
        if response:
            info = response.json()
            if len(info["result"]) != 25:
                r = mid
            else:
                l = mid
        else:
            print("Ошибка выполнения запроса:")
            print(link)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            return None

    left = l
    link = f'https://codeforces.com/api/user.status?handle={user_handle}&from={left}&count=25'
    info = requests.get(link).json()
    tasks = info["result"]
    tasks_set = set()
    verdicts = dict()
    rating = dict()
    for task in tasks:
        tasks_set.add(task['problem']['name'])
        if task['verdict'] not in verdicts:
            verdicts[task['verdict']] = 1
        else:
            verdicts[task['verdict']] += 1
        try:
            if task['problem']['rating'] not in rating:
                rating[task['problem']['rating']] = 1
            else:
                rating[task['problem']['rating']] += 1
        except:
            continue
    return [tasks_set, verdicts, rating]


if __name__ == "__main__":
    pass
