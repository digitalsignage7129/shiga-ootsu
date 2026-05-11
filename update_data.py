import urllib.request
import json
import os
import time
from datetime import datetime

def fetch_data(url):
    # 気象庁サーバーに拒否されないよう、ブラウザのふりをする設定
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    for i in range(3):  # 失敗しても3回までリトライする
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as res:
                return json.load(res)
        except Exception as e:
            print(f"Retry {i+1}: {e}")
            time.sleep(2)
    return None

def main():
    # 1. 気象庁アメダス最新値（滋賀県全体）
    url = "https://www.jma.go.jp/bosai/amedas/data/latest_timeseries/250000.json"
    data = fetch_data(url)
    
    # 初期値
    temp, wind_spd, humidity = 20.0, 0.0, 60
    wind_dir = "取得不可"
    
    if data:
        times = sorted(data.keys(), reverse=True)
        found = False
        for t in times[:6]:  # 過去1時間分(6データ)遡って探す
            if '60131' in data[t]: # 大津地点
                d = data[t]['60131']
                if 'temp' in d and d['temp'][0] is not None:
                    temp = d['temp'][0]
                    wind_spd = d.get('wind', [0])[0]
                    dirs = ["静穏","北北東","北東","東北東","東","東南東","南東","南南東","南","南南西","南西","西南西","西","西北西","北西","北北西","北"]
                    d_idx = d.get('windDirection', [0])[0]
                    wind_dir = dirs[d_idx] if d_idx < len(dirs) else "不明"
                    if 'humidity' in d: humidity = d['humidity'][0]
                    found = True
                    break
    
    # WBGT計算
    wbgt = round(0.735 * temp + 0.0374 * humidity + 0.00292 * temp * humidity - 4.064, 1)
    now = datetime.now().strftime('%Y/%m/%d %H:%M')
    
    result = {
        "location": "滋賀県大津市大石中",
        "wbgt": str(wbgt),
        "temp": str(temp),
        "weather": "晴れ/曇",
        "wind_dir": wind_dir,
        "wind_speed": str(wind_spd),
        "updated": now
    }

    os.makedirs('docs', exist_ok=True)
    with open('docs/data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
