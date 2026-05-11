import urllib.request
import json
import os
import time
from datetime import datetime

def fetch_data(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as res:
            return json.load(res)
    except: return None

def main():
    # アメダス
    url = "https://www.jma.go.jp/bosai/amedas/data/latest_timeseries/250000.json"
    data = fetch_data(url)
    
    temp, wind_spd, humidity = 20.0, 0.0, 60
    wind_dir = "北" # デフォルト

    if data:
        times = sorted(data.keys(), reverse=True)
        found = False
        for t in times[:6]:
            # 大津(60131)を優先、なければ信楽(60236)などで補完
            target = data[t].get('60131') or data[t].get('60236')
            if target and 'temp' in target and target['temp'][0] is not None:
                temp = target['temp'][0]
                wind_spd = target.get('wind', [0])[0]
                d_idx = target.get('windDirection', [0])[0]
                # 0は静穏、1から時計回りに北、北北東...
                dirs = ["静穏","北","北北東","北東","東北東","東","東南東","南東","南南東","南","南南西","南西","西南西","西","西北西","北西","北北西"]
                wind_dir = dirs[d_idx] if d_idx < len(dirs) else "調査中"
                if 'humidity' in target: humidity = target['humidity'][0]
                found = True
                break

    wbgt = round(0.735 * temp + 0.0374 * humidity + 0.00292 * temp * humidity - 4.064, 1)
    now = datetime.now().strftime('%Y/%m/%d %H:%M')
    
    result = {
        "wbgt": str(wbgt), "temp": str(temp), "weather": "晴れ/曇",
        "wind_dir": wind_dir, "wind_speed": str(wind_spd), "updated": now
    }

    os.makedirs('docs', exist_ok=True)
    with open('docs/data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
