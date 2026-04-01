import json
import ollama
from fastmcp import Client as MCPClient
import asyncio
import sys

# Configuration
OLLAMA_MODEL = "llama3.2"
MCP_SERVER_URL = "http://127.0.0.1:9090/mcp"

# ------------------------------------------------------------
# Step 1: Discover available tools from MCP server
# ------------------------------------------------------------
async def load_mcp_tools():
    """Connect to MCP server and get list of available tools"""
    try:
        async with MCPClient(MCP_SERVER_URL) as mcp:
            # Ask server: "What tools do you have?"
            tools_list = await mcp.list_tools()

            # Convert to format Ollama understands
            ollama_tools = []
            for tool in tools_list:
                ollama_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema,
                    },
                })
            return ollama_tools
    except Exception as e:
        print(f"❌ ERROR connecting to MCP server: {e}")
        print(f"\nMake sure the server is running:")
        print("  python mcp_server.py")
        sys.exit(1)

# ------------------------------------------------------------
# Step 2: Execute a tool when AI requests it
# ------------------------------------------------------------
async def execute_tool(tool_name: str, arguments: dict):
    """Call a tool on the MCP server with given arguments"""
    try:
        async with MCPClient(MCP_SERVER_URL) as mcp:
            result = await mcp.call_tool(tool_name, arguments)
            return result
    except Exception as e:
        print(f"❌ ERROR executing tool {tool_name}: {e}")
        return {"error": str(e)}

# ------------------------------------------------------------
# Step 3: Main conversation loop
# ------------------------------------------------------------
async def main():
    print("🔍 Loading MCP tools...")
    tools = await load_mcp_tools()
    print(f"✅ Loaded {len(tools)} tools:")
    for tool in tools:
        print(f"   - {tool['function']['name']}: {tool['function']['description']}")
    print()

    # The user's question
    user_msg = "Please greet John and then add 150 + 75."
    print(f"👤 User: {user_msg}\n")

    # Send to Ollama with tools available
    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": user_msg}],
            tools=tools,  # ← AI now knows these tools exist!
            stream=False,
        )
    except Exception as e:
        print(f"❌ ERROR calling Ollama: {e}")
        print(f"\nMake sure:")
        print(f"  1. Ollama is running (ollama serve)")
        print(f"  2. Model is installed (ollama pull {OLLAMA_MODEL})")
        sys.exit(1)

    # Check: Did AI want to use tools?
    if not response.get("message", {}).get("tool_calls"):
        print("🤖 AI answered directly (no tools needed):")
        print(response["message"]["content"])
        return

    # Process tool calls
    messages = [
        {"role": "user", "content": user_msg},
        response["message"]
    ]

    for tool_call in response["message"]["tool_calls"]:
        tool_name = tool_call["function"]["name"]
        args = tool_call["function"]["arguments"]

        # Parse if arguments are JSON string
        if isinstance(args, str):
            args = json.loads(args)

        print(f"🔧 Tool requested: {tool_name}")
        print(f"📝 Arguments: {args}")

        # Execute the tool
        tool_result = await execute_tool(tool_name, args)
        print(f"✅ Tool result: {tool_result}\n")

        # Add tool response to conversation
        messages.append({
            "role": "tool",
            "content": json.dumps(tool_result) if isinstance(tool_result, dict) else str(tool_result),
        })

    # Send tool results back to AI for final answer
    final = ollama.chat(
        model=OLLAMA_MODEL,
        messages=messages,
    )

    print("🤖 Final AI response:")
    print(final["message"]["content"])

if __name__ == "__main__":
    asyncio.run(main())