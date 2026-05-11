import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def get_weather():
    # 気象庁 JSON (滋賀県大津市付近: 250010)
    url = "https://www.jma.go.jp/bosai/forecast/data/forecast/250000.json"
    try:
        res = requests.get(url)
        data = res.json()
        # 大津市の予報・実況情報を抽出
        area_data = data[0]['timeSeries'][0]['areas'][0]
        weather_text = area_data['weathers'][0]
        return weather_text
    except:
        return "取得失敗"

def get_wbgt():
    # 環境省 熱中症予防情報サイト (大津地点: 60131)
    # 実際はAPIがないため、実況値をスクレイピングまたは近似値計算
    # ここでは計算用として気象庁の最新データから取得する例
    url = "https://www.jma.go.jp/bosai/amedas/data/latest_timeseries/250000.json" 
    try:
        res = requests.get(url)
        # 観測地点「大津」の最新気温と湿度を取得
        # ※簡易的に現在の気温を表示するロジック
        return "28.5" # 実際はここに抽出ロジックが入ります
    except:
        return "--"

def main():
    # データの統合
    now = datetime.now().strftime('%Y/%m/%d %H:%M')
    
    # 実際にはここで各APIから詳細を取得します
    # 今回はサイネージ側で使いやすいJSON形式で保存
    result = {
        "location": "滋賀県大津市大石中",
        "wbgt": "31.2",  # 危険レベルの例
        "temp": "33.5",
        "weather": "晴れ",
        "wind_dir": "北西",
        "wind_speed": "2.4",
        "updated": now
    }

    # docsフォルダがない場合は作成
    os.makedirs('docs', exist_ok=True)
    
    # JSONとして保存
    with open('docs/data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
