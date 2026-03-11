# AI Software Engineer Agent - Backend

A production-ready **Multi-Agent AI System** built with Python and Flask that can autonomously plan, code, test, and debug software projects.

## 🌟 Features

### Multi-Agent Architecture
- **Planner Agent**: Analyzes requirements and creates step-by-step execution plans
- **Coder Agent**: Generates production-quality code in multiple languages
- **Tester Agent**: Creates comprehensive test suites automatically
- **Debugger Agent**: Identifies and fixes bugs with AI-powered analysis

### Core Capabilities
✅ **Autonomous Development Pipeline**: User prompt → Planning → Coding → Testing → Debugging → Output  
✅ **Multi-Language Support**: JavaScript, TypeScript, Python, Java, Go, Rust  
✅ **Code Execution**: Safe sandboxed environment for running generated code  
✅ **Memory System**: Vector database (Chroma) for learning from previous tasks  
✅ **GitHub Integration**: Create repos, push code, create pull requests  
✅ **Terminal Commands**: Execute system commands (git, npm, pip, etc.)  
✅ **Project Management**: Create, manage, and analyze project structures  
✅ **Session Tracking**: Maintain user sessions and task history  

## 🏗️ Architecture

```
User Request
    ↓
Planner Agent (Analyze & Break Down Task)
    ↓
Coder Agent (Generate Code)
    ↓
Tester Agent (Create Tests)
    ↓
Code Executor (Run & Validate)
    ↓
Debugger Agent (Fix Errors if Any)
    ↓
Output (Code + Tests + Docs)
```

## 📁 Project Structure

```
backend/
├── app.py                          # Main Flask application
├── config.py                       # Configuration management
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
│
├── agents/                         # AI Agents
│   ├── base_agent.py              # Base agent class
│   ├── planner_agent.py           # Planning agent
│   ├── coder_agent.py             # Code generation agent
│   ├── tester_agent.py            # Testing agent
│   └── debugger_agent.py          # Debugging agent
│
├── orchestrator/                   # Agent coordination
│   └── agent_orchestrator.py     # Manages multi-agent pipeline
│
├── memory/                         # Memory & persistence
│   ├── vector_store.py            # Chroma vector database
│   └── session_manager.py         # Session management
│
├── tools/                          # Utility tools
│   ├── code_executor.py           # Code execution sandbox
│   ├── file_manager.py            # File operations
│   ├── terminal_executor.py       # Terminal commands
│   └── github_integration.py      # GitHub API integration
│
├── api/                            # REST API
│   ├── routes.py                  # API endpoints
│   └── schemas.py                 # Request/response schemas
│
├── prompts/                        # Agent prompts
│   ├── planner_prompts.py
│   ├── coder_prompts.py
│   ├── tester_prompts.py
│   └── debugger_prompts.py
│
├── utils/                          # Utilities
│   ├── logger.py                  # Logging setup
│   ├── validators.py              # Input validation
│   └── helpers.py                 # Helper functions
│
└── data/                           # Data storage
    ├── chroma_db/                 # Vector database files
    └── projects/                  # Generated projects
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+ (for JavaScript execution)
- Git
- OpenAI API Key

### Installation

1. **Clone the repository**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\\Scripts\\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Copy example env file
copy .env.example .env

# Edit .env file and add your keys:
# - OPENAI_API_KEY
# - GITHUB_TOKEN (optional)
```

5. **Run the application**
```bash
python app.py
```

The API will be available at: `http://localhost:5000`

## 📡 API Endpoints

### Task Execution
```http
POST /api/task/execute
Content-Type: application/json

{
  "prompt": "Build a Todo App using React",
  "language": "javascript",
  "framework": "react",
  "execute_code": false,
  "auto_debug": true
}
```

**Response:**
```json
{
  "task_id": "task_abc123",
  "session_id": "session_xyz789",
  "status": "completed",
  "phases": {
    "planning": { "success": true, "data": {...} },
    "coding": { "success": true, "data": {...} },
    "testing": { "success": true, "data": {...} }
  },
  "final_output": {
    "plan": {...},
    "code": {
      "files": {
        "App.js": "...",
        "Todo.js": "..."
      }
    },
    "tests": {...}
  },
  "execution_time": 45.3
}
```

### Code Execution
```http
POST /api/code/execute
Content-Type: application/json

{
  "code": "console.log('Hello World')",
  "language": "javascript",
  "timeout": 60
}
```

### Project Management
```http
POST /api/project/create
Content-Type: application/json

{
  "project_name": "my-todo-app",
  "files": {
    "index.js": "...",
    "package.json": "..."
  }
}
```

### GitHub Integration
```http
POST /api/github/action
Content-Type: application/json

{
  "action": "create_repo",
  "repo_name": "ai-generated-app",
  "description": "Generated by AI",
  "private": false
}
```

### Memory Search
```http
POST /api/memory/search
Content-Type: application/json

{
  "query": "how to build a REST API",
  "limit": 5
}
```

### Session Management
```http
POST /api/session/create
Content-Type: application/json

{
  "user_id": "optional_user_id"
}
```

## 🔧 Configuration

Edit `config.py` or `.env` file:

```python
# OpenAI
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4-turbo-preview

# GitHub (optional)
GITHUB_TOKEN=your_token_here

# Code Execution
ENABLE_CODE_EXECUTION=True
CODE_EXECUTION_TIMEOUT=300

# Flask
API_PORT=5000
API_HOST=0.0.0.0
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_agents.py
```

## 🛠️ Development

### Adding a New Agent

1. Create agent file in `agents/` directory:
```python
from agents.base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="MyAgent",
            system_prompt="You are...",
            temperature=0.7
        )
    
    async def execute(self, input_data):
        # Implementation
        pass
```

2. Add prompts in `prompts/` directory

3. Register in orchestrator

### Adding a New Tool

Create tool file in `tools/` directory following the existing pattern.

## 📊 Performance

- **Average Task Completion**: 30-60 seconds
- **Code Generation**: 10-20 seconds
- **Test Generation**: 5-10 seconds
- **Memory Search**: <1 second

## 🔐 Security

- ✅ Input validation on all endpoints
- ✅ Sandboxed code execution
- ✅ Whitelisted terminal commands
- ✅ Path traversal prevention
- ✅ API rate limiting (recommended to add)
- ✅ CORS configuration

## 🤝 Integration with Frontend

The backend is designed to work seamlessly with the React frontend:

```javascript
// Frontend API call example
const response = await fetch('http://localhost:5000/api/task/execute', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    prompt: 'Build a calculator app',
    language: 'javascript',
    execute_code: true
  })
});

const result = await response.json();
console.log(result.final_output.code);
```

## 🐛 Troubleshooting

### Common Issues

**1. OpenAI API Key Error**
```
Solution: Ensure OPENAI_API_KEY is set in .env file
```

**2. ChromaDB Permission Error**
```
Solution: Check data/chroma_db directory permissions
```

**3. Code Execution Fails**
```
Solution: Verify Python/Node.js are installed and in PATH
```

**4. GitHub Integration Not Working**
```
Solution: Generate GitHub personal access token with repo permissions
```

## 📈 Roadmap

- [ ] Docker containerization
- [ ] Kubernetes deployment configs
- [ ] Real-time WebSocket updates
- [ ] Support for more languages (C++, Swift, Kotlin)
- [ ] Code review agent
- [ ] Documentation generation agent
- [ ] Performance optimization agent
- [ ] CI/CD integration
- [ ] Metrics and analytics dashboard

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- OpenAI for GPT models
- LangChain for agent framework
- ChromaDB for vector storage
- Flask for web framework

## 📧 Support

For issues, questions, or contributions:
- GitHub Issues: [Create an issue]
- Email: support@example.com
- Documentation: [Full docs]

---

**Built with ❤️ using AI and Python**
