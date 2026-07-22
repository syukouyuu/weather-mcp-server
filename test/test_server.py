from weather_mcp.server import get_current_weather


def test_get_current_weather() -> None:
    result = get_current_weather("Tokyo")

    assert result["city"] == "Tokyo"
    assert isinstance(result["temperature"], int | float) 
    assert isinstance(result["weather_code"], int) 