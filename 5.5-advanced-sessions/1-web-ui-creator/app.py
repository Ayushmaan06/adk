"""
🎨 Dynamic Session Creator - Web UI

A beautiful Streamlit interface for creating and managing ADK sessions.
"""

import streamlit as st
import requests
import json
from typing import Dict, Any

# Configuration
ADK_BASE_URL = "http://localhost:8000"
AGENT_ID = "dynamic_session_agent"

# Page config
st.set_page_config(
    page_title="ADK Session Creator",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .preset-button {
        margin: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🎯 Dynamic Session Creator")
st.markdown("**Create unique ADK sessions with custom user information**")

# Sidebar - Quick Presets
st.sidebar.header("⚡ Quick Presets")
st.sidebar.markdown("*Click to auto-fill form*")

presets = {
    "👩‍💻 Alice (Developer)": {
        "user_id": "alice",
        "user_name": "Alice Johnson",
        "user_email": "alice@devcompany.com",
        "user_preferences": "Software engineer specializing in Python. Loves building AI applications and enjoys learning about new technologies."
    },
    "👨‍🔬 Bob (Data Scientist)": {
        "user_id": "bob",
        "user_name": "Bob Smith",
        "user_email": "bob@datascience.io",
        "user_preferences": "Data scientist with expertise in machine learning and statistics. Enjoys coffee and solving complex problems."
    },
    "👩‍🎓 Carol (Student)": {
        "user_id": "carol",
        "user_name": "Carol Martinez",
        "user_email": "carol@university.edu",
        "user_preferences": "Computer science student learning about AI. Needs help understanding concepts and completing assignments."
    }
}

# Preset buttons
for preset_name, preset_data in presets.items():
    if st.sidebar.button(preset_name, key=preset_name):
        st.session_state.update(preset_data)
        st.rerun()

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Create New Session")
    
    with st.form("session_form"):
        user_id = st.text_input(
            "User ID *",
            value=st.session_state.get("user_id", ""),
            help="Unique identifier (e.g., username, employee_id)",
            placeholder="alice"
        )
        
        user_name = st.text_input(
            "User Name *",
            value=st.session_state.get("user_name", ""),
            help="Full name of the user",
            placeholder="Alice Johnson"
        )
        
        user_email = st.text_input(
            "Email",
            value=st.session_state.get("user_email", ""),
            help="Optional: User's email address",
            placeholder="alice@email.com"
        )
        
        user_preferences = st.text_area(
            "Preferences / Context",
            value=st.session_state.get("user_preferences", ""),
            help="Optional: Any additional context about the user",
            placeholder="Software engineer, loves Python, enjoys hiking on weekends",
            height=100
        )
        
        conversation_context = st.text_area(
            "Initial Conversation Context",
            value=st.session_state.get("conversation_context", ""),
            help="Optional: Set initial conversation context",
            placeholder="User is asking about project deadlines",
            height=60
        )
        
        submit_button = st.form_submit_button("🚀 Create Session", use_container_width=True)
        
        if submit_button:
            if not user_id or not user_name:
                st.error("❌ User ID and User Name are required!")
            else:
                # Build state dict (only include non-empty fields)
                state = {
                    "user_name": user_name
                }
                
                if user_email:
                    state["user_email"] = user_email
                if user_preferences:
                    state["user_preferences"] = user_preferences
                if conversation_context:
                    state["conversation_context"] = conversation_context
                
                # Create session
                try:
                    with st.spinner("Creating session..."):
                        response = requests.post(
                            f"{ADK_BASE_URL}/sessions",
                            json={
                                "agent_id": AGENT_ID,
                                "state": state
                            },
                            timeout=10
                        )
                    
                    if response.status_code == 200:
                        session_data = response.json()
                        session_id = session_data["session_id"]
                        
                        # Store in session state
                        if "created_sessions" not in st.session_state:
                            st.session_state.created_sessions = []
                        
                        st.session_state.created_sessions.append({
                            "session_id": session_id,
                            "user_id": user_id,
                            "user_name": user_name,
                            "state": state
                        })
                        
                        # Success message
                        st.success("✅ Session created successfully!")
                        st.markdown(f"""
                        <div class="success-box">
                            <strong>Session ID:</strong> <code>{session_id}</code><br>
                            <strong>User:</strong> {user_name} ({user_id})
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Direct link
                        chat_url = f"{ADK_BASE_URL}/?session={session_id}"
                        st.link_button(
                            "💬 Chat with this session",
                            chat_url,
                            use_container_width=True
                        )
                        
                        # Clear form
                        for key in ["user_id", "user_name", "user_email", "user_preferences", "conversation_context"]:
                            if key in st.session_state:
                                del st.session_state[key]
                    else:
                        st.error(f"❌ Failed to create session: {response.status_code}")
                        st.code(response.text)
                
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to ADK Web. Make sure it's running on port 8000!")
                    st.code("cd d:\\agentic\\adk\\5.5-advanced-sessions\nadk web")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

with col2:
    st.header("📊 Active Sessions")
    
    if "created_sessions" in st.session_state and st.session_state.created_sessions:
        st.markdown(f"**Total Sessions:** {len(st.session_state.created_sessions)}")
        
        for idx, session in enumerate(reversed(st.session_state.created_sessions)):
            with st.expander(f"👤 {session['user_name']} ({session['user_id']})"):
                st.markdown(f"**Session ID:** `{session['session_id']}`")
                
                # Display state
                st.markdown("**State:**")
                st.json(session['state'])
                
                # Chat link
                chat_url = f"{ADK_BASE_URL}/?session={session['session_id']}"
                st.link_button(
                    "💬 Chat with this session",
                    chat_url,
                    key=f"chat_{idx}",
                    use_container_width=True
                )
        
        # Clear all button
        if st.button("🗑️ Clear All Sessions", type="secondary"):
            st.session_state.created_sessions = []
            st.rerun()
    else:
        st.info("No sessions created yet. Create your first session using the form!")

# Footer
st.markdown("---")
st.markdown("""
### 💡 Tips
- Use **Quick Presets** (sidebar) for fast testing
- Create multiple sessions to see state isolation
- Each session has completely separate memory
- Session IDs are UUIDs (universally unique)

### 🔧 ADK Web Status
Make sure ADK Web is running:
```powershell
cd d:\\agentic\\adk\\5.5-advanced-sessions
adk web
```
""")
