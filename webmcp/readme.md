# WebMCP Todo App

A lightweight Todo application demonstrating the WebMCP (Web Model Context Protocol) architectural pattern, integrating Express.js with Google Gemini 2.5 Flash for intelligent tool execution.

## 🛠️ Project Setup

```bash
mkdir webmcp-todo-app
cd webmcp-todo-app

# Initialize project and install dependencies
npm init -y
npm install express cors @google/generative-ai dotenv

# Create project structure
mkdir public src
touch src/app.js public/index.html public/client.js
```

## 📂 Project Structure

```text
webmcp-todo-app/
├── public/
│   ├── index.html
│   └── client.js
├── src/
│   └── app.js
├── package.json
└── README.md
```

### Core Files Explanation

- **`src/app.js`**: The backend server (Express). It defines the WebMCP tools, integrates with Gemini AI for intelligent request processing, and provides API endpoints for the frontend.
- **`public/index.html`**: The frontend user interface. It provides the visual structure for the todo management dashboard and the AI chat interface.
- **`public/client.js`**: The client-side logic. It handles UI interactions, communicates with the backend APIs via fetch, and dynamically updates the todo list and chat messages.

## 🚀 Running the App

```bash
npm start 

# Server Output:
# 🚀 WebMCP Todo App running at http://localhost:3000
```

## 🌐 Browser Access

Open your browser and navigate to:
```text
http://localhost:3000
```

## 📡 API Usage & WebMCP Tools

### List Available Tools
```bash
curl http://localhost:3000/api/tools
```

### Add a New Todo
```bash
curl -X POST http://localhost:3000/api/call-tool \
  -H "Content-Type: application/json" \
  -d '{
    "toolName": "addTodo",
    "params": {"title": "Buy groceries"}
  }'
```

### List All Todos
```bash
curl -X POST http://localhost:3000/api/call-tool \
  -H "Content-Type: application/json" \
  -d '{
    "toolName": "listTodos",
    "params": {"filter": "all"}
  }'
```

### Mark a Todo as Completed
```bash
curl -X POST http://localhost:3000/api/call-tool \
  -H "Content-Type: application/json" \
  -d '{
    "toolName": "completeTodo",
    "params": {"id": 1}
  }'
```

## 🛠️ Configuration

Create a `.env` file in the root directory:
```text
GEMINI_API_KEY=your_api_key_here
PORT=3000
```