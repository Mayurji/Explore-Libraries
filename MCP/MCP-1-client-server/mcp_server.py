from fastmcp import FastMCP
from datetime import datetime


# Initialize the server with a name
mcp = FastMCP("my-first-server")

# Define a tool using the @mcp.tool decorator
@mcp.tool
def get_weather(city: str) -> dict:
    """Get the current weather for a city."""
    # In production, you'd call a real weather API
    # For now, we'll return mock data
    weather_data = {
        "new york": {"temp": 72, "condition": "sunny"},
        "london": {"temp": 59, "condition": "cloudy"},
        "tokyo": {"temp": 68, "condition": "rainy"},
    }
    
    city_lower = city.lower()
    if city_lower in weather_data:
        return {"city": city, **weather_data[city_lower]}
    else:
        return {"city": city, "temp": 70, "condition": "unknown"}

@mcp.tool
def get_time(timezone: str = "UTC") -> str:
    """Get the current time in a specified timezone."""
    # Simplified - in production use pytz or zoneinfo
    return f"Current time ({timezone}): {datetime.now().strftime('%H:%M:%S')}"

@mcp.tool
def calculate(expression: str) -> dict:
    """Safely evaluate a mathematical expression."""
    try:
        # Only allow safe math operations
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expression):
            return {"error": "Invalid characters in expression"}
        
        result = eval(expression)  # Safe because we validated input
        return {"expression": expression, "result": result}
    except Exception as e:
        return {"error": str(e)}

# Run the server
if __name__ == "__main__":
    mcp.run(transport="stdio")