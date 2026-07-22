from weather_mcp.server import get_current_weather


def test_get_current_weather() -> None:
    result = get_current_weather("Tokyo")

    assert result["city"] == "Tokyo"
    assert result["temperature"] == 25
    assert result["condition"] == "sunny"