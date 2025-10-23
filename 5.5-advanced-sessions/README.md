# 🎯 Advanced Session Management

This folder demonstrates **dynamic session management** in Google ADK where each user has their own unique state and memory.

---

## 📁 Folder Structure

```
5.5-advanced-sessions/
├── agent/                          # The dynamic session agent
│   ├── agent.py                    # Agent with conditional state handling
│   └── __init__.py
│
├── 1-web-ui-creator/               # Method 1: Streamlit Web UI
│   ├── app.py                      # Beautiful web interface
│   ├── requirements.txt
│   └── README.md
│
├── 2-rest-api-manager/             # Method 2: REST API Manager
│   ├── session_manager.py          # Python API client
│   ├── examples.py                 # Usage examples
│   └── README.md
│
├── 3-cli-interactive/              # Method 3: Interactive CLI
│   ├── create_session.py           # Interactive session creator
│   └── README.md
│
├── 4-programmatic-examples/        # Method 4: Programmatic Examples
│   ├── multi_user_demo.py          # Multiple users chatting
│   ├── async_sessions.py           # Async concurrent sessions
│   └── README.md
│
└── README.md                       # This file

```

---

## 🚀 Quick Start

### **Step 1: Start ADK Web**

```powershell
cd d:\agentic\adk\5.5-advanced-sessions
adk web
```

### **Step 2: Choose Your Method**

#### **Method 1: Web UI Creator (Easiest)**
```powershell
cd 1-web-ui-creator
pip install -r requirements.txt
streamlit run app.py
```

#### **Method 2: REST API Manager**
```powershell
cd 2-rest-api-manager
python examples.py
```

#### **Method 3: Interactive CLI**
```powershell
cd 3-cli-interactive
python create_session.py
```

#### **Method 4: Programmatic Examples**
```powershell
cd 4-programmatic-examples
python multi_user_demo.py
```

---

## 🎯 Key Features

### ✅ **Dynamic State Management**
- No hardcoded user information
- Each session has unique state
- State persists across conversation turns

### ✅ **Multiple Session Creation Methods**
- Web UI (Streamlit)
- REST API (Python)
- Interactive CLI
- Programmatic (async/sync)

### ✅ **Session Isolation**
- Each user has completely separate state
- No data leakage between sessions
- UUID-based session identification

### ✅ **Memory Across Turns**
- Agent remembers what users tell it
- Conversation history maintained
- State updates dynamically

---

## 📖 How It Works

### **1. Agent Configuration**

```python
# agent/agent.py
Agent(
    name="dynamic_session_agent",
    instruction="""
    {%- if user_name %}
    User: {{user_name}}
    {%- endif %}
    
    {%- if user_preferences %}
    Info: {{user_preferences}}
    {%- endif %}
    
    If you don't know about the user, ask them!
    """
    # NO initial_state - starts empty!
)
```

### **2. Create Sessions Dynamically**

```python
# Any method can create unique sessions
session_manager.create_session(
    user_id="alice",
    user_name="Alice Johnson",
    user_preferences="Software engineer, loves Python"
)

session_manager.create_session(
    user_id="bob",
    user_name="Bob Smith",
    user_preferences="Data scientist, enjoys coffee"
)
```

### **3. Sessions Maintain State**

```
Alice's Session (UUID: abc123...)
├─ user_name: "Alice Johnson"
├─ user_preferences: "Software engineer..."
└─ conversation_history: [...]

Bob's Session (UUID: def456...)
├─ user_name: "Bob Smith"
├─ user_preferences: "Data scientist..."
└─ conversation_history: [...]
```

---

## 💡 Use Cases

### **1. Multi-User Chat Application**
Each user gets their own session with personalized context.

### **2. Customer Support Bot**
Each customer has a session with their order history and preferences.

### **3. Educational Tutor**
Each student has a session tracking their progress and learning style.

### **4. Personal Assistant**
Each person has a session with their tasks, preferences, and schedule.

---

## 📊 Comparison with Basic Sessions

| Feature | Basic (5-sessions-and-state) | Advanced (5.5-advanced-sessions) |
|---------|------------------------------|----------------------------------|
| **State** | Hardcoded initial_state | Dynamic, per-user |
| **Users** | Same info for all | Unique info per user |
| **Creation** | Manual script only | Web UI, API, CLI, Code |
| **Flexibility** | Low | High |
| **Production Ready** | Demo | Yes |

---

## 🎓 Learning Path

1. **Start Here:** `1-web-ui-creator` (easiest, visual)
2. **Then Try:** `2-rest-api-manager` (programmatic)
3. **Advanced:** `4-programmatic-examples` (async, concurrent)

---

## 🛠️ Requirements

```powershell
# Core requirements
pip install google-adk python-dotenv

# For Web UI Creator
pip install streamlit

# For REST API examples
pip install requests

# All already installed if you have ADK!
```

---

## 📚 Documentation

- **ADK Sessions Docs**: https://google.github.io/adk-docs/sessions/
- **Agent Development**: https://google.github.io/adk-docs/agents/
- **State Management**: https://google.github.io/adk-docs/state/

---

## 🎉 Get Started!

```powershell
# 1. Start ADK Web
cd d:\agentic\adk\5.5-advanced-sessions
adk web

# 2. Choose your favorite method and create sessions!

# 3. Open browser
http://localhost:8000
```

**Each method is fully documented in its own README!** 🚀
