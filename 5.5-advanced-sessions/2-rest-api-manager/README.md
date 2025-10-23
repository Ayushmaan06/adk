# 🔌 REST API Session Manager

**Programmatic session management with Python!**

A clean Python client for creating and managing ADK sessions via REST API.

---

## 🚀 Quick Start

### **Step 1: Start ADK Web**

```powershell
cd d:\agentic\adk\5.5-advanced-sessions
adk web
```

### **Step 2: Run Examples**

```powershell
cd 2-rest-api-manager
python examples.py
```

---

## 📖 How It Works

The `SessionManager` class provides a clean interface to ADK Web's REST API:

```python
from session_manager import SessionManager

# Create manager
manager = SessionManager()

# Create session with custom state
session_id = manager.create_session(
    agent_id="dynamic_session_agent",
    user_name="Alice Johnson",
    user_email="alice@email.com",
    user_preferences="Software engineer, loves Python"
)

# Send messages
response = manager.send_message(session_id, "Hello!")
print(response)

# List all sessions
sessions = manager.list_sessions()

# Get session details
details = manager.get_session(session_id)
```

---

## 🎯 SessionManager API

### **Create Session**

```python
session_id = manager.create_session(
    agent_id="dynamic_session_agent",
    user_name="Alice",           # Required
    user_email="alice@email.com", # Optional
    user_preferences="...",       # Optional
    **kwargs                      # Any additional state variables
)
```

Returns: `str` - Session UUID

### **Send Message**

```python
response = manager.send_message(
    session_id="abc-123-def-456",
    message="What can you help me with?"
)
```

Returns: `str` - Agent's response

### **List Sessions**

```python
sessions = manager.list_sessions(agent_id="dynamic_session_agent")
```

Returns: `List[Dict]` - List of session objects

### **Get Session Details**

```python
details = manager.get_session(session_id="abc-123-def-456")
```

Returns: `Dict` - Session object with state and metadata

### **Delete Session**

```python
success = manager.delete_session(session_id="abc-123-def-456")
```

Returns: `bool` - True if deleted successfully

---

## 💻 Example Scripts

### **Example 1: Simple Chat**

```python
from session_manager import SessionManager

manager = SessionManager()

# Create session for Alice
alice_session = manager.create_session(
    agent_id="dynamic_session_agent",
    user_name="Alice Johnson",
    user_preferences="Software engineer"
)

# Chat
print(manager.send_message(alice_session, "Hi!"))
print(manager.send_message(alice_session, "What's my name?"))
print(manager.send_message(alice_session, "What do I do?"))
```

### **Example 2: Multiple Users**

```python
# Create sessions for multiple users
users = [
    {"name": "Alice", "email": "alice@email.com", "info": "Developer"},
    {"name": "Bob", "email": "bob@email.com", "info": "Data scientist"},
    {"name": "Carol", "email": "carol@email.com", "info": "Student"}
]

sessions = {}
for user in users:
    session_id = manager.create_session(
        agent_id="dynamic_session_agent",
        user_name=user["name"],
        user_email=user["email"],
        user_preferences=user["info"]
    )
    sessions[user["name"]] = session_id

# Send same question to all
question = "What can you help me with?"
for name, session_id in sessions.items():
    print(f"\n{name}'s response:")
    print(manager.send_message(session_id, question))
```

### **Example 3: Session Management**

```python
# List all active sessions
all_sessions = manager.list_sessions()
print(f"Active sessions: {len(all_sessions)}")

for session in all_sessions:
    print(f"- {session['session_id']}: {session['state'].get('user_name', 'Unknown')}")

# Get specific session details
details = manager.get_session(session_id)
print(f"User: {details['state']['user_name']}")
print(f"State: {details['state']}")

# Delete old sessions
for session in all_sessions:
    manager.delete_session(session['session_id'])
```

---

## 🎓 Use Cases

### **1. Testing & QA**

```python
# Create test sessions programmatically
test_users = load_test_data()
for user in test_users:
    session = manager.create_session(
        agent_id="dynamic_session_agent",
        **user
    )
    run_test_scenarios(session)
```

### **2. Integration Testing**

```python
# Test agent behavior with different user types
def test_agent_personalization():
    # Create session
    session = manager.create_session(
        agent_id="dynamic_session_agent",
        user_name="Test User",
        user_preferences="Testing personalization"
    )
    
    # Send test messages
    response = manager.send_message(session, "What's my name?")
    assert "Test User" in response
    
    response = manager.send_message(session, "What do you know about me?")
    assert "Testing personalization" in response
```

### **3. Load Testing**

```python
import concurrent.futures

def create_and_chat(user_id):
    session = manager.create_session(
        agent_id="dynamic_session_agent",
        user_name=f"User {user_id}"
    )
    for i in range(10):
        manager.send_message(session, f"Message {i}")
    return session

# Create 100 concurrent sessions
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    sessions = list(executor.map(create_and_chat, range(100)))
```

### **4. Bot Integration**

```python
# Integrate with Discord/Slack bot
class ChatBot:
    def __init__(self):
        self.manager = SessionManager()
        self.user_sessions = {}
    
    def handle_message(self, user_id, user_name, message):
        # Get or create session for user
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = self.manager.create_session(
                agent_id="dynamic_session_agent",
                user_name=user_name,
                user_id=user_id
            )
        
        # Send message
        session_id = self.user_sessions[user_id]
        return self.manager.send_message(session_id, message)
```

---

## 🛠️ Implementation Details

### **API Endpoints Used**

```
POST   /sessions                 Create new session
GET    /sessions                 List all sessions
GET    /sessions/{session_id}    Get session details
DELETE /sessions/{session_id}    Delete session
POST   /chat                     Send message to session
```

### **Error Handling**

```python
try:
    session_id = manager.create_session(...)
except ConnectionError:
    print("ADK Web not running!")
except ValueError as e:
    print(f"Invalid parameters: {e}")
except Exception as e:
    print(f"Error: {e}")
```

### **Timeouts**

```python
# Default timeout: 30 seconds
manager = SessionManager(timeout=30)

# Custom timeout for long operations
manager = SessionManager(timeout=60)
```

---

## 📦 Dependencies

```python
import requests  # Already installed with ADK
```

No additional dependencies needed!

---

## 🎉 Tips

1. **Store session IDs**: Save them in database/cache for persistent user sessions
2. **Error handling**: Always wrap API calls in try-except blocks
3. **Concurrent sessions**: Use ThreadPoolExecutor for parallel operations
4. **Session cleanup**: Delete old sessions to free memory

---

## 🔧 Troubleshooting

### Connection Refused

```powershell
# Make sure ADK Web is running
cd d:\agentic\adk\5.5-advanced-sessions
adk web
```

### Timeout Errors

```python
# Increase timeout for slow operations
manager = SessionManager(timeout=60)
```

### Session Not Found

```python
# Check if session exists
sessions = manager.list_sessions()
session_ids = [s['session_id'] for s in sessions]
if my_session_id not in session_ids:
    print("Session doesn't exist!")
```

---

## 🚀 Next Steps

1. **Run examples.py** to see all features in action
2. **Modify examples** for your use case
3. **Integrate with your application** (web app, bot, API)
4. **Build custom session management** logic

**Start coding! The SessionManager makes it easy! 🎉**
