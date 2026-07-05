import os
import requests
from datetime import datetime

OPENWEATHER_API_KEY = os.environ["OPENWEATHER_API_KEY"]
PUSHBULLET_API_KEY = os.environ["PUSHBULLET_API_KEY"]
CITY = "Osaka"


def get_weather():
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": CITY,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "ja"
    }

    res = requests.get(url, params=params, timeout=10)
    res.raise_for_status()
    data = res.json()

    city = data["name"]
    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]

    return (
        f"📍 {city}\n"
        f"🌤 天気：{weather}\n"
        f"🌡 気温：{temp}℃（体感{feels_like}℃）\n"
        f"💧 湿度：{humidity}%"
    )


def send_pushbullet(title, body):
    url = "https://api.pushbullet.com/v2/pushes"
    headers = {
        "Access-Token": PUSHBULLET_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "type": "note",
        "title": title,
        "body": body
    }

    res = requests.post(url, headers=headers, json=payload, timeout=10)
    res.raise_for_status()


def main():
    today = datetime.now().strftime("%Y年%m月%d日")

    weather = get_weather()

    title = f"🌅 {today} の朝通知"
    body = (
        f"【☀ 今日の天気】\n{weather}\n\n"
        f"良い一日をお過ごしください！"
    )

    send_pushbullet(title, body)
    print("通知完了")


if __name__ == "__main__":
    main()
