from fastmcp import FastMCP

mcp = FastMCP("Weather MCP")

@mcp.tool()
def get_current_weather(city: str) -> dict:
    """获取指定城市的天气"""
    return {
        "city":city,
        "temperature": 25,
        "condition": "sunny",
    }


if __name__ == "__main__":
    mcp.run()
