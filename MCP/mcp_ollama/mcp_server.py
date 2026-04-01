# mcp_server.py
from fastmcp import FastMCP

# Create the MCP server instance
mcp = FastMCP("MCP Server")

# Define Tool 1: Add two numbers
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

# Define Tool 2: Greet someone
@mcp.tool()
def greet(name: str) -> str:
    """Greet someone by name"""
    return f"Hello, {name}! Welcome!"

# Define Tool 3: Multiply numbers
@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b

# Define Tool 4: Get current time
@mcp.tool()
def get_time() -> str:
    """Get the current time"""
    from datetime import datetime
    return datetime.now().strftime("%I:%M %p")

@mcp.tool()
def get_weather(city: str) -> str:
    """Get the current weather for a city (mock implementation)"""
    # In a real implementation, you would call a weather API here
    return f"The current weather in {city} is sunny with a temperature of 25°C."

if __name__ == "__main__":
    # Start the server
    mcp.run(transport="http", port=9090)