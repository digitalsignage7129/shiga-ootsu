import urllib.request
import json
import os
from datetime import datetime

def main():
    # 気象庁アメダス最新値（滋賀県全体）
    url = "https://www.jma.go.jp/bosai/amedas/data/latest_timeseries/250000.json"
    
    # デフォルト値（取得失敗時の表示）
    temp = 20.0
    wind_spd = 0.0
    wind_dir = "計測中"
    humidity = 50 

    try:
        with urllib.request.urlopen(url) as res:
            data = json.load(res)
            
            # 最新のタイムスタンプを取得
            times = sorted(data.keys(), reverse=True)
            
            # 直近の3件分くらいをループして大津(60131)のデータを探す（欠測対策）
            for t in times:
                otsu = data[t].get('60131')
                if otsu and 'temp' in otsu:
                    temp = otsu['temp'][0]
                    wind_spd = otsu.get('wind', [0])[0]
                    # 風向コードを変換
                    dirs = ["静穏","北北東","北東","東北東","東","東南東","南東","南南東","南","南南西","南西","西南西","西","西北西","北西","北北西","北"]
                    d_idx = otsu.get('windDirection', [0])[0]
                    wind_dir = dirs[d_idx] if d_idx < len(dirs) else "不明"
                    if 'humidity' in otsu:
                        humidity = otsu['humidity'][0]
                    break # データが見つかったらループ終了

        # WBGT近似計算
        wbgt = round(0.735 * temp + 0.0374 * humidity + 0.00292 * temp * humidity - 4.064, 1)
        
    except Exception as e:
        print(f"Error during extraction: {e}")
        temp, wbgt, wind_dir, wind_spd = 0, 0, "エラー", 0

    now = datetime.now().strftime('%Y/%m/%d %H:%M')
    
    result = {
        "location": "滋賀県大津市大石中",
        "wbgt": str(wbgt),
        "temp": str(temp),
        "weather": "晴れ/曇", # 天気予報JSONは構造がさらに複雑なため、一旦固定か簡易化
        "wind_dir": wind_dir,
        "wind_speed": str(wind_spd),
        "updated": now
    }

    os.makedirs('docs', exist_ok=True)
    with open('docs/data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
