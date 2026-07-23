from weather_mcp.server import get_weather_description,get_coordinates,get_current_weather

import pytest


def test_get_weather_description() -> None:
    assert get_weather_description(2) == "Partly cloudy"
    assert get_weather_description(999) == "Unknown weather"


class FakeResponse:
    def raise_for_status(self) -> None:
        pass

    def json(self) -> dict:
        return {
            "results": [
                {
                    "name": "Tokyo",
                    "latitude": 35.6762,
                    "longitude": 139.6503,
                }
            ]
        }


def test_get_coordinates_without_network(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_get(*args, **kwargs) -> FakeResponse:
        return FakeResponse()


    monkeypatch.setattr(
        "weather_mcp.server.httpx.get",
        fake_get,
    )

    result = get_coordinates("Tokyo")


    assert result == {
        "name": "Tokyo",
        "latitude": 35.6762,
        "longitude": 139.6503,
    }


def test_get_coordinate_city_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeResponse:
        def raise_for_status(self) -> None:
            pass
    
        def json(self) -> dict:
            return {}


    def fake_get(*args, **kwargs) -> FakeResponse:
        return FakeResponse()

    monkeypatch.setattr(
        "weather_mcp.server.httpx.get",
        fake_get,
    )

    with pytest.raises(ValueError, match="City not found"):
        get_coordinates("City not found")
