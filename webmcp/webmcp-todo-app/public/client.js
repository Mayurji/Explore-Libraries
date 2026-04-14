// ==================== Global State ====================
let allTodos = [];
let currentFilter = 'all';
let isProcessing = false;

// ==================== Initialize ====================
document.addEventListener('DOMContentLoaded', () => {
    loadTodos();
    loadAvailableTools();

    // Allow Enter key to add todo
    document.getElementById('todoInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addTodoUI();
        }
    });

    // Allow Ctrl+Enter to send chat message
    document.getElementById('chatInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
            sendChatMessage();
        }
    });

    // Auto-scroll to bottom of chat
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.addEventListener('DOMNodeInserted', () => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    });
});

// ==================== Load Tools ====================
async function loadAvailableTools() {
    try {
        const response = await fetch('/api/tools');
        const data = await response.json();
        console.log('📡 Available WebMCP Tools:', data.tools);

        const list = document.getElementById('toolsDisplayList');
        if (data.tools && data.tools.length > 0) {
            list.innerHTML = data.tools.map(tool => {
                const params = Object.keys(tool.inputSchema.properties).join(', ');
                return `<li><code>${tool.name}(${params})</code></li>`;
            }).join('');
        } else {
            list.innerHTML = '<li><i>No tools available</i></li>';
        }
    } catch (error) {
        console.error('Error loading tools:', error);
        document.getElementById('toolsDisplayList').innerHTML = '<li><i style="color: red;">Error loading tools</i></li>';
    }
}

// ==================== Load Todos ====================
async function loadTodos() {
    try {
        const response = await fetch('/api/todos');
        allTodos = await response.json();
        renderTodos();
    } catch (error) {
        console.error('Error loading todos:', error);
    }
}

// ==================== Manual Todo Operations ====================

async function addTodoUI() {
    const input = document.getElementById('todoInput');
    const title = input.value.trim();

    if (!title) {
        alert('Please enter a todo title');
        return;
    }

    try {
        const response = await fetch('/api/call-tool', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                toolName: 'addTodo',
                params: { title }
            })
        });

        const result = await response.json();

        if (result.success) {
            console.log('✅ Tool executed:', result.message);
            input.value = '';
            loadTodos();
        } else {
            alert('Error: ' + result.message);
        }
    } catch (error) {
        console.error('Error adding todo:', error);
    }
}

async function completeTodoUI(id) {
    try {
        const response = await fetch('/api/call-tool', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                toolName: 'completeTodo',
                params: { id }
            })
        });

        const result = await response.json();

        if (result.success) {
            console.log('✅ Tool executed:', result.message);
            loadTodos();
        }
    } catch (error) {
        console.error('Error completing todo:', error);
    }
}

async function deleteTodoUI(id) {
    if (!confirm('Are you sure?')) return;

    try {
        const response = await fetch('/api/call-tool', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                toolName: 'deleteTodo',
                params: { id }
            })
        });

        const result = await response.json();

        if (result.success) {
            console.log('✅ Tool executed:', result.message);
            loadTodos();
        }
    } catch (error) {
        console.error('Error deleting todo:', error);
    }
}

function filterTodos(filter) {
    currentFilter = filter;

    document.querySelectorAll('.filter-buttons button').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');

    renderTodos();
}

function renderTodos() {
    const list = document.getElementById('todosList');

    let filtered = allTodos;
    if (currentFilter === 'completed') {
        filtered = allTodos.filter(t => t.completed);
    } else if (currentFilter === 'pending') {
        filtered = allTodos.filter(t => !t.completed);
    }

    if (filtered.length === 0) {
        list.innerHTML = '<div class="empty-state">No todos. Start by asking me to add one! 🚀</div>';
        return;
    }

    list.innerHTML = filtered.map(todo => `
    <li class="todo-item ${todo.completed ? 'completed' : ''}">
      <input 
        type="checkbox" 
        class="todo-checkbox" 
        ${todo.completed ? 'checked' : ''} 
        onchange="completeTodoUI(${todo.id})"
      >
      <span class="todo-text">${escapeHtml(todo.title)}</span>
      <div class="todo-actions">
        <button class="btn-small" onclick="deleteTodoUI(${todo.id})">Delete</button>
      </div>
    </li>
  `).join('');
}

// ==================== Gemini Chat ====================

async function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();

    if (!message || isProcessing) return;

    // Display user message
    addChatMessage(message, 'user');
    input.value = '';

    // Show loading
    isProcessing = true;
    document.getElementById('sendBtn').disabled = true;

    try {
        // Show thinking indicator
        const thinkingMsg = addChatMessage('Thinking...', 'system');

        // Send to backend
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const result = await response.json();

        // Remove thinking message
        thinkingMsg.remove();

        if (result.success) {
            // Display AI response
            const aiMsg = document.createElement('div');
            aiMsg.className = 'message ai';

            // Main response
            const responseText = document.createElement('div');
            responseText.textContent = result.aiResponse;
            aiMsg.appendChild(responseText);

            // Show executed tools
            if (result.toolsExecuted && result.toolsExecuted.length > 0) {
                const toolsDiv = document.createElement('div');
                toolsDiv.className = 'tools-executed';
                toolsDiv.innerHTML = `<strong>🔧 Executed ${result.toolsExecuted.length} tool(s):</strong><br>`;

                result.toolsExecuted.forEach(exec => {
                    const status = exec.result.success ? '✅' : '❌';
                    let message = exec.result.message || 'Success';
                    const toolItem = document.createElement('div');
                    toolItem.className = 'tool-item';

                    // Specialized display for tool results
                    if (exec.tool === 'listTodos' && exec.result.todos) {
                        const items = exec.result.todos.map(t => `<br>&nbsp;&nbsp;• ${t.title} [${t.completed ? '✅' : '⏳'}]`).join('');
                        toolItem.innerHTML = `<strong>${status} ${exec.tool}:</strong> ${message}${items}`;
                    } else if (exec.tool === 'addTodo' && exec.result.todo) {
                        toolItem.innerHTML = `<strong>${status} ${exec.tool}:</strong> ${message} (ID: ${exec.result.todo.id})`;
                    } else {
                        toolItem.innerHTML = `<strong>${status} ${exec.tool}:</strong> ${message}`;
                    }

                    toolsDiv.appendChild(toolItem);
                });

                aiMsg.appendChild(toolsDiv);
            }

            document.getElementById('chatMessages').appendChild(aiMsg);

            // Reload todos to show changes
            await loadTodos();
        } else {
            addChatMessage(
                `❌ Error: ${result.error || 'Unknown error'}`,
                'error'
            );
        }
    } catch (error) {
        addChatMessage(`❌ Error: ${error.message}`, 'error');
    } finally {
        isProcessing = false;
        document.getElementById('sendBtn').disabled = false;
        document.getElementById('chatInput').focus();
    }
}

function addChatMessage(text, sender = 'ai') {
    const container = document.getElementById('chatMessages');
    const message = document.createElement('div');
    message.className = `message ${sender}`;
    message.textContent = text;
    container.appendChild(message);
    return message;
}

// ==================== Utility Functions ====================

function escapeHtml(text) {
    // If any special characters are present in the text, replace them with their HTML entities
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}