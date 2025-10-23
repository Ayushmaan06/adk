# 🚀 Quick Start Guide

Get up and running with dynamic session management in 5 minutes!

---

## ⚡ Step 1: Set Up Environment

```powershell
# Make sure you're in the right folder
cd d:\agentic\adk\5.5-advanced-sessions

# Create .env file with your API key (if not already done)
# Edit .env and add: GOOGLE_API_KEY=your_api_key_here
```

---

## ⚡ Step 2: Start ADK Web

```powershell
adk web
```

You should see:
```
🚀 Starting ADK Web...
✅ Server running at http://localhost:8000
```

**Keep this terminal open!**

---

## ⚡ Step 3: Choose Your Method

Open a **new terminal** and pick one:

### **Option A: Web UI (Easiest!)**

```powershell
cd 1-web-ui-creator
pip install streamlit
streamlit run app.py
```

Then:
1. Fill in the form (or use presets)
2. Click "Create Session"
3. Click "Chat with this session"
4. Start chatting!

---

### **Option B: REST API (Programmatic)**

```powershell
cd 2-rest-api-manager
python examples.py
```

Watch it:
- Create multiple sessions
- Send messages
- Manage sessions
- Show state isolation

---

### **Option C: Interactive CLI (Terminal)**

```powershell
cd 3-cli-interactive
python create_session.py
```

Follow the prompts:
- User ID: `alice`
- User Name: `Alice Johnson`
- Email: `alice@email.com`
- Preferences: `Software engineer`

Get a session ID and chat URL!

---

### **Option D: Programmatic Examples (Advanced)**

```powershell
cd 4-programmatic-examples

# Multi-user demo
python multi_user_demo.py

# OR async demo (faster!)
python async_sessions.py
```

---

## 🎯 What You'll See

### **Dynamic State**
Each session has unique user information:
```
Alice's Session:
  - user_name: "Alice Johnson"
  - user_preferences: "Software engineer"

Bob's Session:
  - user_name: "Bob Smith"  
  - user_preferences: "Data scientist"
```

### **State Isolation**
Alice's session knows nothing about Bob:
```
Alice: "What's my name?"
Agent: "Your name is Alice Johnson!"

Bob: "What's my name?"
Agent: "Your name is Bob Smith!"
```

### **Memory Persistence**
Context maintained across turns:
```
Turn 1: "I love Python"
Turn 2: "What language do I like?"
Agent: "You love Python!"
```

---

## 🎓 Learning Path

1. **Day 1**: Try Web UI (easiest)
2. **Day 2**: Run REST API examples
3. **Day 3**: Play with CLI creator
4. **Day 4**: Study programmatic examples
5. **Day 5**: Build your own integration!

---

## 💡 Common Tasks

### Create a Session
```python
from session_manager import SessionManager

manager = SessionManager()
session_id = manager.create_session(
    agent_id="dynamic_session_agent",
    user_name="Alice",
    user_email="alice@email.com"
)
```

### Send a Message
```python
response = manager.send_message(session_id, "Hello!")
print(response)
```

### Get Chat URL
```python
url = manager.get_chat_url(session_id)
print(f"Chat here: {url}")
```

---

## 🔧 Troubleshooting

### "Cannot connect to ADK Web"
**Solution**: Start ADK Web first!
```powershell
cd d:\agentic\adk\5.5-advanced-sessions
adk web
```

### "Context variable not found"
**Solution**: Make sure you're using the dynamic agent in this folder, not the old one in folder 5!

### "Module not found"
**Solution**: Install dependencies
```powershell
pip install streamlit  # For Web UI
pip install aiohttp    # For async examples (optional)
```

---

## 📚 Next Steps

After you're comfortable:

1. **Customize the agent** (`agent/agent.py`)
   - Add more state variables
   - Customize instructions
   - Add tools

2. **Build your app**
   - Discord bot with sessions
   - Web app with user accounts
   - Customer support system
   - Educational tutor

3. **Scale up**
   - Use async for performance
   - Add persistent storage
   - Implement session cleanup
   - Add authentication

---

## 🎉 You're Ready!

Pick a method and start creating sessions!

**Remember**: 
- Each session = unique state
- No hardcoded data
- Complete isolation
- Production-ready!

**Let's go! 🚀**
