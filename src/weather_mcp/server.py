from fastmcp import FastMCP

import httpx

mcp = FastMCP("Weather MCP")

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

@mcp.tool()
def get_current_weather(city: str) -> dict:
    """获取指定城市的天气"""

    """1.获取指定地理坐标"""
    location = get_coordinates(city)

    """2.获取指定城市的天气"""
    response = httpx.get(
        FORECAST_URL,
        params={
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": "temperature_2m,weather_code",
        },
        timeout= 10,
    )

    response.raise_for_status()
    data = response.json()
    current = data["current"]
        
    
    return {
        "city":location["name"],
        "temperature": current["temperature_2m"],
        "weather_code": current["weather_code"],
    }


def get_coordinates(city: str) -> dict:
    response = httpx.get(
        GEOCODING_URL,
        params={
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
        },
        timeout=10.0,
    )

    response.raise_for_status()
    data = response.json()

    result = data["results"][0]

    return {
        "name": result["name"],
        "latitude": result["latitude"],
        "longitude": result["longitude"],
    }


if __name__ == "__main__":
    mcp.run()
