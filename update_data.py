import urllib.request
import json
import os
from datetime import datetime

def main():
    # 気象庁アメダス最新値（滋賀県全体）
    url = "https://www.jma.go.jp/bosai/amedas/data/latest_timeseries/250000.json"
    
    # 初期値
    temp = 0.0
    wind_spd = 0.0
    wind_dir = "取得中"
    humidity = 60 # 滋賀県の平均的な湿度
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as res:
            data = json.load(res)
            
            # 時刻キーを新しい順に並べる
            times = sorted(data.keys(), reverse=True)
            
            # 直近30分（3データ分）をスキャンして大津のデータがある時刻を探す
            found = False
            for t in times[:3]:
                if '60131' in data[t]:
                    otsu = data[t]['60131']
                    # temp属性が存在するかチェック
                    if 'temp' in otsu and otsu['temp'][0] is not None:
                        temp = otsu['temp'][0]
                        wind_spd = otsu.get('wind', [0])[0]
                        # 風向コードの変換
                        dirs = ["静穏","北北東","北東","東北東","東","東南東","南東","南南東","南","南南西","南西","西南西","西","西北西","北西","北北西","北"]
                        d_idx = otsu.get('windDirection', [0])[0]
                        wind_dir = dirs[d_idx] if d_idx < len(dirs) else "不明"
                        if 'humidity' in otsu and otsu['humidity'][0] is not None:
                            humidity = otsu['humidity'][0]
                        found = True
                        break
            
            if not found:
                # 万が一大津が見つからない場合、滋賀県内の別の近い地点(信楽: 60236)を予備にする
                for t in times[:3]:
                    if '60236' in data[t]:
                        shigaraki = data[t]['60236']
                        temp = shigaraki.get('temp', [20])[0]
                        wind_dir = "予備地点データ"
                        break

        # WBGT近似計算（日本生気象学会式）
        wbgt = round(0.735 * temp + 0.0374 * humidity + 0.00292 * temp * humidity - 4.064, 1)
        
    except Exception as e:
        print(f"Error: {e}")
        temp, wbgt, wind_dir, wind_spd = 0, 0, "通信エラー", 0

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
