// Import required modules
const express = require('express');
const cors = require('cors');
require('dotenv').config();
const { GoogleGenerativeAI } = require('@google/generative-ai');

// Create Express app
const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Initialize Gemini
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
const model = genAI.getGenerativeModel({ model: 'gemini-2.5-flash' });

// ==================== In-memory Storage ====================
let todos = [
    { id: 1, title: 'Learn WebMCP', completed: false },
    { id: 2, title: 'Build an app', completed: false }
];

let nextId = 3;

// ==================== WebMCP Tools Definition ====================

const webmcpTools = [
    {
        name: 'addTodo',
        description: 'Add a new todo item to the list. Returns the newly created todo with an ID.',
        inputSchema: {
            type: 'object',
            properties: {
                title: {
                    type: 'string',
                    description: 'The title or description of the todo item'
                }
            },
            required: ['title']
        }
    },
    {
        name: 'listTodos',
        description: 'Get all todo items. Optionally filter by completed status.',
        inputSchema: {
            type: 'object',
            properties: {
                filter: {
                    type: 'string',
                    enum: ['all', 'completed', 'pending'],
                    description: 'Filter todos by status. Default is "all".'
                }
            }
        }
    },
    {
        name: 'completeTodo',
        description: 'Mark a todo item as completed by its ID.',
        inputSchema: {
            type: 'object',
            properties: {
                id: {
                    type: 'number',
                    description: 'The ID of the todo to mark as completed'
                }
            },
            required: ['id']
        }
    },
    {
        name: 'deleteTodo',
        description: 'Delete a todo item by its ID.',
        inputSchema: {
            type: 'object',
            properties: {
                id: {
                    type: 'number',
                    description: 'The ID of the todo to delete'
                }
            },
            required: ['id']
        }
    }
];

// ==================== Tool Implementations ====================

function addTodo(title) {
    const newTodo = {
        id: nextId++,
        title: title,
        completed: false,
        createdAt: new Date().toISOString()
    };
    todos.push(newTodo);
    return {
        success: true,
        message: `Todo "${title}" added successfully`,
        todo: newTodo
    };
}

function listTodos(filter = 'all') {
    let filtered = todos;

    if (filter === 'completed') {
        filtered = todos.filter(t => t.completed);
    } else if (filter === 'pending') {
        filtered = todos.filter(t => !t.completed);
    }

    return {
        success: true,
        message: `Found ${filtered.length} ${filter} todo(s)`,
        total: filtered.length,
        todos: filtered
    };
}

function completeTodo(id) {
    // Find the todo by ID
    const todo = todos.find(t => t.id === id);

    // If todo is not found, return error
    if (!todo) {
        return {
            success: false,
            message: `Todo with ID ${id} not found`
        };
    }

    todo.completed = true;
    todo.completedAt = new Date().toISOString();

    return {
        success: true,
        message: `Todo "${todo.title}" marked as completed`,
        todo: todo
    };
}

function deleteTodo(id) {
    // Find the todo by ID
    const index = todos.findIndex(t => t.id === id);

    // If todo is not found, return error
    if (index === -1) {
        return {
            success: false,
            message: `Todo with ID ${id} not found`
        };
    }

    // Delete the todo
    const deleted = todos.splice(index, 1)[0];

    return {
        success: true,
        message: `Todo "${deleted.title}" deleted successfully`,
        deletedTodo: deleted
    };
}
// Map tool names to their implementations
const toolImplementations = {
    addTodo: (params) => addTodo(params.title),
    listTodos: (params) => listTodos(params.filter || 'all'),
    completeTodo: (params) => completeTodo(params.id),
    deleteTodo: (params) => deleteTodo(params.id)
};
// ==================== Execute Tool ====================

function executeTool(toolName, params) {
    // Execute the tool
    try {
        const implementation = toolImplementations[toolName];
        if (implementation) {
            return implementation(params);
        } else {
            return {
                success: false,
                message: `Unknown tool: ${toolName}`
            };
        }
    } catch (error) {
        return {
            success: false,
            message: error.message
        };
    }
}

// ==================== Gemini Integration ====================

/**
 * Create a system prompt for Gemini with tool descriptions
 */
function createSystemPrompt() {
    // Create tool descriptions
    const toolDescriptions = webmcpTools
        .map(tool => {
            const params = tool.inputSchema.properties;
            const paramsList = Object.keys(params)
                .map(key => `  - ${key} (${params[key].type}): ${params[key].description}`)
                .join('\n');

            return `- ${tool.name}: ${tool.description}\n${paramsList}`;
        })
        .join('\n\n');

    return `You are a helpful AI assistant with access to a Todo Management system via WebMCP tools.

AVAILABLE TOOLS:
${toolDescriptions}

INSTRUCTIONS:
1. When the user asks you to perform an action, use the appropriate tool(s)
2. Format your tool calls as JSON like this: {"tool": "toolName", "params": {"param1": "value1"}}
3. When you need to call multiple tools, call them sequentially
4. Always confirm what actions you've taken
5. Be helpful and provide summaries of the results

USER INTENT: Understand what the user wants and use the tools to help them achieve it.`;
}

/**
 * Parse AI response to extract tool calls
 */
function extractToolCalls(text) {
    const toolCalls = [];

    // Find all potential JSON objects start points
    let pos = 0;
    while ((pos = text.indexOf('{', pos)) !== -1) {
        let braceCount = 0;
        let endPos = -1;
        let inString = false;
        let escaped = false;

        // Try to find the matching closing brace
        for (let i = pos; i < text.length; i++) {
            const char = text[i];

            if (escaped) {
                escaped = false;
                continue;
            }

            if (char === '\\') {
                escaped = true;
                continue;
            }

            if (char === '"') {
                inString = !inString;
                continue;
            }

            if (!inString) {
                if (char === '{') braceCount++;
                if (char === '}') braceCount--;

                if (braceCount === 0) {
                    endPos = i + 1;
                    break;
                }
            }
        }

        if (endPos !== -1) {
            const potentialJson = text.substring(pos, endPos);
            try {
                const parsed = JSON.parse(potentialJson);
                if (parsed && parsed.tool) {
                    toolCalls.push({
                        tool: parsed.tool,
                        params: parsed.params || {}
                    });
                }
            } catch (e) {
                // Not valid JSON, or not a tool call, just continue
            }
            pos = endPos;
        } else {
            pos++;
        }
    }

    return toolCalls;
}

/**
 * Process user message with Gemini
 * Returns: { response, toolsExecuted, results }
 */
async function processWithGemini(userMessage) {
    try {
        const systemPrompt = createSystemPrompt();

        // Send message to Gemini
        const result = await model.generateContent({
            contents: [
                {
                    role: 'user',
                    parts: [
                        {
                            text: `${systemPrompt}\n\nUser: ${userMessage}`
                        }
                    ]
                }
            ]
        });

        const aiResponse = result.response.text();

        // Extract and execute tools from response
        const toolCalls = extractToolCalls(aiResponse);
        const executedTools = [];

        for (const call of toolCalls) {
            const toolResult = executeTool(call.tool, call.params);
            executedTools.push({
                tool: call.tool,
                params: call.params,
                result: toolResult
            });
        }

        return {
            success: true,
            aiResponse: aiResponse,
            toolsExecuted: executedTools,
            toolCount: toolCalls.length
        };
    } catch (error) {
        return {
            success: false,
            error: error.message,
            aiResponse: `Error processing request: ${error.message}`
        };
    }
}

// ==================== API Routes ====================

/**
 * GET /api/tools
 * Returns all available WebMCP tools
 */
app.get('/api/tools', (req, res) => {
    res.json({
        tools: webmcpTools
    });
});

/**
 * POST /api/call-tool
 * Execute a tool directly
 */
app.post('/api/call-tool', (req, res) => {
    const { toolName, params } = req.body;
    const result = executeTool(toolName, params);
    res.json(result);
});

/**
 * POST /api/chat
 * Send a message to Gemini AI (NEW!)
 */
app.post('/api/chat', async (req, res) => {
    const { message } = req.body;

    if (!message) {
        return res.status(400).json({
            success: false,
            error: 'Message is required'
        });
    }

    const result = await processWithGemini(message);
    res.json(result);
});

/**
 * GET /api/todos
 * Get all todos
 */
app.get('/api/todos', (req, res) => {
    res.json(todos);
});

/**
 * GET /health
 * Health check endpoint
 */
app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        gemini: process.env.GEMINI_API_KEY ? 'configured' : 'not configured'
    });
});

// ==================== Start Server ====================

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`🚀 WebMCP Todo App with Gemini running at http://localhost:${PORT}`);
    console.log(`📡 Gemini API: ${process.env.GEMINI_API_KEY ? '✅ Connected' : '❌ Not configured'}`);
});