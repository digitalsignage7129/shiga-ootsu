import urllib.requestimport urllib.request
import json
import os
from datetime import datetime

def main():
    # 気象庁アメダス 大津地点(60131) の最新10分値データ
    amedas_url = "https://www.jma.go.jp/bosai/amedas/data/latest_timeseries/250000.json"
    # 気象庁天気予報 滋賀県
    forecast_url = "https://www.jma.go.jp/bosai/forecast/data/forecast/250000.json"
    
    try:
        # 1. 気温・風速を取得
        with urllib.request.urlopen(amedas_url) as res:
            amedas_data = json.load(res)
            latest_time = list(amedas_data.keys())[-1]
            otsu_obs = amedas_data[latest_time].get('60131', {})
            temp = otsu_obs.get('temp', [0])[0]
            humidity = otsu_obs.get('humidity', [50])[0] # 湿度データがない場合は50%と仮定
            wind_spd = otsu_obs.get('wind', [0])[0]
            wind_dir_code = otsu_obs.get('windDirection', [0])[0]
            
            # 風向コードを日本語に変換
            dirs = ["静穏","北北東","北東","東北東","東","東南東","南東","南南東","南","南南西","南西","西南西","西","西北西","北西","北北西","北"]
            wind_dir = dirs[wind_dir_code] if wind_dir_code < len(dirs) else "不明"

        # 2. 天気を取得
        with urllib.request.urlopen(forecast_url) as res:
            forecast_data = json.load(res)
            weather = forecast_data[0]['timeSeries'][0]['areas'][0]['weathers'][0]

        # 3. WBGT（暑さ指数）の簡易計算式
        # 日本生気象学会の近似式：0.735×気温 + 0.0374×湿度 + 0.00292×気温×湿度 - 4.064
        wbgt = round(0.735 * temp + 0.0374 * humidity + 0.00292 * temp * humidity - 4.064, 1)
        
    except Exception as e:
        print(f"Error: {e}")
        temp, wbgt, weather, wind_dir, wind_spd = 0, 0, "データ更新中", "-", 0

    # 4. JSON保存
    now = datetime.now().strftime('%m/%d %H:%M')
    result = {
        "wbgt": str(wbgt),
        "temp": str(temp),
        "weather": weather.split('　')[0],
        "wind_dir": wind_dir,
        "wind_speed": str(wind_spd),
        "updated": now
    }

    os.makedirs('docs', exist_ok=True)
    with open('docs/data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
import json
import os
from datetime import datetime

def main():
    # 気象庁のアメダス最新値（滋賀県）
    # 大津地点のデータが含まれるJSON
    amedas_url = "https://www.jma.go.jp/bosai/amedas/data/latest_timeseries/250000.json"
    
    try:
        with urllib.request.urlopen(amedas_url) as res:
            amedas_data = json.load(res)
            # 大津地点(地点コード: 60131)の最新データを抽出
            # データの構造上、最新時刻のキーを取得
            latest_time = list(amedas_data.keys())[-1]
            otsu_data = amedas_data[latest_time].get('60131', {})
            
            # 気温を取得（データがない場合は20.0をデフォルトに）
            current_temp = otsu_data.get('temp', [20.0])[0]
            # 風速と風向
            current_wind_spd = otsu_data.get('wind', [0.0])[0]
            # WBGTの簡易計算 (気温から推測)
            calculated_wbgt = round(current_temp * 0.8, 1) 
    except Exception as e:
        print(f"Error: {e}")
        current_temp = "--"
        calculated_wbgt = "--"
        current_wind_spd = "--"

    now = datetime.now().strftime('%Y/%m/%d %H:%M')

    result = {
        "location": "滋賀県大津市大石中",
        "wbgt": str(calculated_wbgt),
        "temp": str(current_temp),
        "weather": "取得中",
        "wind_dir": "南西",
        "wind_speed": str(current_wind_spd),
        "updated": now
    }

    os.makedirs('docs', exist_ok=True)
    with open('docs/data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
