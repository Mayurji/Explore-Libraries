## Build your First MCP Server

### What problem does MCP Server solve?

If you've worked on LLM + tool + agents, then writing custom code to handle the integration, managing API schemas, or even authenticating with external services can be a daunting task. **MCP Server provides a standardized way to define and manage these interactions, allowing you to focus on building your application rather than dealing with the complexities of integration.**

### Simple MCP Architecture

<img src="image.png" alt="MCP Server" width="700"/>

### Three Building Blocks of MCP Server

**Server** — Exposes your tools. It’s a Python script that says “here are the functions an LLM can call.” You run it, and it listens for requests.

**Tool** — A function you want the LLM to use. Could be anything: fetch weather, query a database, send an email. You write it like a normal Python function, add a decorator, and MCP handles the rest.

**Client** — The thing that connects to your server and calls tools. In production, this is usually your LLM application. For testing, FastMCP gives you a client that works out of the box.

### Building Our First MCP Server

```bash
python -m venv deepagent-env
source deepagent-env/bin/activate
pip install fastmcp
```
**Implementation**

1. Create a server with a tool using FastMCP
2. Create a client to connect to the server
3. Run the server and client to see them in action
3. Adding more tools and testing them