# ⌨️ Interactive CLI Session Creator

**Create ADK sessions from your terminal!**

An interactive command-line tool for creating and managing ADK sessions.

---

## 🚀 Quick Start

### **Step 1: Start ADK Web**

```powershell
cd d:\agentic\adk\5.5-advanced-sessions
adk web
```

### **Step 2: Run the CLI**

```powershell
cd 3-cli-interactive
python create_session.py
```

---

## 🎯 Features

### ✨ **Interactive Prompts**
Step-by-step guided session creation with helpful prompts.

### 🎨 **Colorful Output**
Beautiful terminal output with colors and emojis (optional).

### 📋 **Session History**
View all sessions created in the current CLI session.

### 🔗 **Direct Links**
Get clickable links to chat with created sessions.

### 🔄 **Loop Mode**
Create multiple sessions without restarting the script.

---

## 💻 Example Session

```
🎯 ADK Session Creator
====================================

Let's create a new session!

👤 User ID: alice
📧 User Name: Alice Johnson
📨 Email (optional): alice@email.com
ℹ️  Preferences (optional): Software engineer, loves Python

Creating session...
✅ Session created successfully!

📋 Session Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Session ID: abc-123-def-456-ghi
User: Alice Johnson (alice)
State:
  - user_name: Alice Johnson
  - user_email: alice@email.com
  - user_preferences: Software engineer, loves Python

🔗 Chat URL:
http://localhost:8000/?session=abc-123-def-456-ghi

Create another session? (y/n): y
```

---

## 🎓 Use Cases

### **1. Quick Testing**
Create test sessions quickly without writing code.

### **2. Demo Setup**
Set up demo sessions before presentations.

### **3. User Onboarding**
Create sessions for new users during onboarding calls.

### **4. Development**
Create sessions for testing different scenarios.

---

## 💡 Input Options

### **Required Fields**
- **User ID**: Unique identifier (username, employee ID, etc.)
- **User Name**: Full name of the user

### **Optional Fields**
- **Email**: User's email address
- **Preferences**: Any additional context about the user
- **Conversation Context**: Initial conversation context

### **Tips**
- Press Enter to skip optional fields
- Use meaningful User IDs for easy identification
- Add detailed preferences for better personalization

---

## 🔧 Advanced Usage

### **Non-Interactive Mode**

```python
# Pass arguments directly
python create_session.py --user-id alice --user-name "Alice Johnson"
```

### **Batch Creation**

```python
# Create from CSV file
python create_session.py --from-csv users.csv
```

### **JSON Export**

```python
# Export session info as JSON
python create_session.py --export-json sessions.json
```

---

## 📦 No Dependencies

The CLI uses only Python standard library - no additional installs needed!

---

## 🎨 Customization

### **Disable Colors**

```python
# Edit create_session.py
USE_COLORS = False
```

### **Change Default Agent**

```python
# Edit create_session.py
DEFAULT_AGENT = "your_agent_name"
```

### **Custom Base URL**

```powershell
python create_session.py --base-url http://remote-server:8000
```

---

## 🔍 Session History

The CLI keeps track of sessions you create:

```
📊 Session History (3 sessions)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Alice Johnson (alice)
   Session: abc-123...
   Chat: http://localhost:8000/?session=abc-123...

2. Bob Smith (bob)
   Session: def-456...
   Chat: http://localhost:8000/?session=def-456...

3. Carol Martinez (carol)
   Session: ghi-789...
   Chat: http://localhost:8000/?session=ghi-789...
```

---

## 🛠️ Troubleshooting

### Can't Connect to ADK Web

```powershell
# Make sure ADK Web is running
cd d:\agentic\adk\5.5-advanced-sessions
adk web
```

### Colors Not Working

Some terminals don't support ANSI colors. Disable them:

```python
USE_COLORS = False  # In create_session.py
```

### Keyboard Interrupt

Press `Ctrl+C` to exit anytime:

```
^C
👋 Goodbye!
```

---

## 🚀 Next Steps

1. **Start ADK Web** if not already running
2. **Run the CLI**: `python create_session.py`
3. **Create sessions** interactively
4. **Click chat links** to test them
5. **Create multiple sessions** to see isolation

**Try it now! It's fun and easy! ⌨️**
