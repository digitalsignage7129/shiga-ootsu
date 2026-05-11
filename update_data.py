import urllib.request
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
