import asyncio
from fastmcp import Client

async def main():
    # Point the client at your server file
    client = Client("mcp_server.py")
    
    # Connect to the server
    async with client:
        # List available tools
        tools = await client.list_tools()
        print("Available tools:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        
        print("\n" + "="*50 + "\n")
        
        # Call the weather tool
        result = await client.call_tool(
            "get_weather", 
            {"city": "Tokyo"}
        )
        print(f"Weather result: {result}")

        # Call the time tool
        result = await client.call_tool(
            "get_time", 
            {"timezone": "Asia/Kolkata"}
        )
        print(f"Time result: {result}")

        # Call the calculate tool
        result = await client.call_tool(
            "calculate", 
            {"expression": "2 + 2"}
        )
        print(f"Calculate result: {result}")

if __name__ == "__main__":
    asyncio.run(main())