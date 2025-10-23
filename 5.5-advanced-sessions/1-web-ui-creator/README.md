# 🎨 Web UI Session Creator

**The easiest way to create and manage ADK sessions!**

A beautiful Streamlit web interface for creating dynamic ADK sessions with custom user information.

---

## 🚀 Quick Start

### **Step 1: Start ADK Web**

```powershell
cd d:\agentic\adk\5.5-advanced-sessions
adk web
```

### **Step 2: Start the Web UI**

```powershell
cd 1-web-ui-creator
pip install -r requirements.txt
streamlit run app.py
```

### **Step 3: Create Sessions!**

1. Open the Streamlit UI (opens automatically)
2. Fill in user information:
   - User ID (unique identifier)
   - User Name
   - Email (optional)
   - Preferences (optional)
3. Click **"Create Session"**
4. Get session ID and direct link to ADK Web UI!

---

## ✨ Features

### 📋 **Quick Presets**
Click one button to create test sessions:
- **Alice (Developer)** - Software engineer, loves Python
- **Bob (Data Scientist)** - Data expert, enjoys coffee
- **Carol (Student)** - Learning AI, needs help with assignments

### 🎯 **Custom Sessions**
Create sessions with any user information:
- Personalized names
- Custom preferences
- Unique context

### 📊 **Session Management**
- View all active sessions
- See session details (ID, user, state)
- Direct links to chat with each session

### 🔗 **One-Click Access**
Click "Chat with this session" to open ADK Web UI directly to that session.

---

## 📖 How It Works

```
User fills form
    ↓
Streamlit app creates session via POST /sessions
    ↓
ADK Web creates new session with custom state
    ↓
Returns session UUID
    ↓
User clicks link to chat
    ↓
ADK Web loads session with personalized context
```

---

## 🎨 Screenshots

### Session Creator
```
┌─────────────────────────────────────┐
│  🎯 Dynamic Session Creator         │
├─────────────────────────────────────┤
│  User ID:     [alice           ]    │
│  User Name:   [Alice Johnson   ]    │
│  Email:       [alice@email.com ]    │
│  Preferences: [Software engineer]   │
│                                     │
│  [Create Session]                   │
└─────────────────────────────────────┘
```

### Session List
```
┌─────────────────────────────────────┐
│  📊 Active Sessions (3)             │
├─────────────────────────────────────┤
│  👤 Alice Johnson                   │
│     Session: abc123...              │
│     [Chat with this session]        │
├─────────────────────────────────────┤
│  👤 Bob Smith                       │
│     Session: def456...              │
│     [Chat with this session]        │
└─────────────────────────────────────┘
```

---

## 💻 Code Example

The Streamlit app uses this logic:

```python
import streamlit as st
import requests

# Create session with custom state
response = requests.post(
    "http://localhost:8000/sessions",
    json={
        "agent_id": "dynamic_session_agent",
        "state": {
            "user_name": "Alice Johnson",
            "user_email": "alice@email.com",
            "user_preferences": "Software engineer, loves Python"
        }
    }
)

session_id = response.json()["session_id"]

# Direct link to chat
chat_url = f"http://localhost:8000/chat/{session_id}"
```

---

## 🎓 Use Cases

### **1. Testing Multiple Users**
Quickly create test sessions for Alice, Bob, and Carol to see how the agent responds to different users.

### **2. Demo Presentations**
Create sessions with specific user profiles before a demo to show personalized responses.

### **3. User Research**
Create sessions for user testing with different personas and preferences.

### **4. Development**
Quickly create sessions with edge cases (empty preferences, long names, special characters).

---

## 🛠️ Customization

### Add Your Own Presets

Edit `app.py`:

```python
presets = {
    "Your Persona": {
        "user_id": "custom_id",
        "user_name": "Your Name",
        "user_email": "your@email.com",
        "user_preferences": "Your preferences here"
    }
}
```

### Add More Fields

```python
# In app.py form section
favorite_color = st.text_input("Favorite Color")

# In state dict
state = {
    "user_name": user_name,
    "favorite_color": favorite_color
}
```

### Change Agent

```python
# Point to different agent
"agent_id": "your_agent_name"
```

---

## 📦 Dependencies

```
streamlit>=1.28.0
requests>=2.31.0
```

Already included in `requirements.txt`!

---

## 🎉 Tips

1. **Create multiple sessions** to see state isolation
2. **Use presets** for quick testing
3. **Open multiple chat windows** to compare responses
4. **Refresh session list** to see all active sessions

---

## 🔧 Troubleshooting

### Port Already in Use
```powershell
# Kill Streamlit process
Get-Process | Where-Object {$_.ProcessName -like "*streamlit*"} | Stop-Process

# Restart
streamlit run app.py
```

### Can't Connect to ADK Web
```powershell
# Make sure ADK Web is running
cd d:\agentic\adk\5.5-advanced-sessions
adk web
```

### Sessions Not Showing
- Refresh the session list
- Make sure you created sessions through the UI
- Check ADK Web terminal for errors

---

## 🚀 Next Steps

After creating sessions:
1. Click **"Chat with this session"** to open ADK Web UI
2. Send messages to see personalized responses
3. Create another session with different info
4. See how each session maintains its own state!

**Try it now! Start the UI and create your first session! 🎉**
