from mcp.server.fastmcp import FastMCP
import httpx
import sys
import logging

# サーバー側で確実にログを残すための設定
logging.basicConfig(filename='/home/masaki/mcp/server.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Weather server initializing...")

# FastMCPサーバーの初期化
mcp = FastMCP("weather_server")

@mcp.tool()
async def get_weather(latitude: float, longitude: float) -> str:
    """指定された緯度経度の現在の天気を取得します。"""
    logging.info(f"get_weather called with lat={latitude}, lon={longitude}")
    
    # Open-Meteo APIのエンドポイント
    # current=temperature_2m,weather_code,wind_speed_10m で現在の気温、天気コード、風速を取得
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,weather_code,wind_speed_10m"

    
    # デバッグ用に標準エラー出力へURLを出力
    sys.stderr.write(f"[DEBUG] Requesting URL: {url}\n")
    sys.stderr.flush()
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPStatusError as e:
        sys.stderr.write(f"[ERROR] HTTPStatusError: {e.response.status_code} - {e.response.text}\n")
        sys.stderr.flush()
        return f"APIエラーが発生しました: {e.response.status_code} {e.response.text}"
    except Exception as e:
        sys.stderr.write(f"[ERROR] Exception: {str(e)}\n")
        sys.stderr.flush()
        return f"通信エラーが発生しました: {str(e)}"
        
    current = data.get("current", {})
    temp = current.get("temperature_2m")
    wind_speed = current.get("wind_speed_10m")
    weather_code = current.get("weather_code")
    
    # WMO（世界気象機関）の天気コードを日本語の簡単な説明に変換
    weather_desc = {
        0: "快晴",
        1: "晴れ", 2: "一部曇り", 3: "曇り",
        45: "霧", 48: "霧氷",
        51: "霧雨(軽)", 53: "霧雨(中)", 55: "霧雨(重)",
        61: "雨(軽)", 63: "雨(中)", 65: "雨(重)",
        71: "雪(軽)", 73: "雪(中)", 75: "雪(重)",
        95: "雷雨"
    }.get(weather_code, "不明")
    
    return f"[WSL版サーバーから取得] 現在の天気: {weather_desc}\n気温: {temp} °C\n風速: {wind_speed} km/h"

if __name__ == "__main__":
    # MCPサーバーを起動
    mcp.run()
