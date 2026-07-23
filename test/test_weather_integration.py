from weather_mcp.server import get_current_weather,get_coordinates

import pytest

def test_get_current_weather() -> None:
    result = get_current_weather("Tokyo")

    assert result["city"] == "Tokyo"
    assert isinstance(result["temperature"], int | float) 
    assert isinstance(result["weather_code"], int) 

def test_get_coordinates() -> None:
    with pytest.raises(ValueError,match="City not found"):
        get_coordinates("abcdefg-not-a-city")

