"""
⌨️ Interactive CLI Session Creator

Create ADK sessions from your terminal with beautiful interactive prompts.
"""

import requests
import sys
from typing import Optional, Dict, List

# Configuration
ADK_BASE_URL = "http://localhost:8000"
AGENT_ID = "dynamic_session_agent"

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Session history
session_history: List[Dict] = []


def colored(text: str, color: str) -> str:
    """Add color to text (if supported)"""
    return f"{color}{text}{Colors.ENDC}"


def print_header(text: str):
    """Print a colored header"""
    print(f"\n{colored(text, Colors.HEADER + Colors.BOLD)}")
    print("=" * 50)


def print_success(text: str):
    """Print success message"""
    print(colored(f"✅ {text}", Colors.GREEN))


def print_error(text: str):
    """Print error message"""
    print(colored(f"❌ {text}", Colors.RED))


def print_info(text: str):
    """Print info message"""
    print(colored(f"ℹ️  {text}", Colors.CYAN))


def get_input(prompt: str, required: bool = True) -> Optional[str]:
    """Get user input with colored prompt"""
    try:
        while True:
            value = input(colored(f"{prompt}: ", Colors.BLUE)).strip()
            
            if value:
                return value
            elif not required:
                return None
            else:
                print_error("This field is required!")
    except KeyboardInterrupt:
        print(f"\n{colored('👋 Goodbye!', Colors.YELLOW)}")
        sys.exit(0)


def create_session(
    user_id: str,
    user_name: str,
    user_email: Optional[str] = None,
    user_preferences: Optional[str] = None,
    conversation_context: Optional[str] = None
) -> Optional[str]:
    """Create a session via ADK Web API"""
    
    # Build state
    state = {"user_name": user_name}
    if user_email:
        state["user_email"] = user_email
    if user_preferences:
        state["user_preferences"] = user_preferences
    if conversation_context:
        state["conversation_context"] = conversation_context
    
    # Make request
    try:
        print(colored("\n⏳ Creating session...", Colors.YELLOW))
        
        response = requests.post(
            f"{ADK_BASE_URL}/sessions",
            json={
                "agent_id": AGENT_ID,
                "state": state
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            session_id = data["session_id"]
            
            # Store in history
            session_history.append({
                "session_id": session_id,
                "user_id": user_id,
                "user_name": user_name,
                "state": state
            })
            
            return session_id
        else:
            print_error(f"Failed to create session: {response.status_code}")
            print(response.text)
            return None
    
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to ADK Web!")
        print_info("Make sure ADK Web is running:")
        print("  cd d:\\agentic\\adk\\5.5-advanced-sessions")
        print("  adk web")
        return None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None


def display_session_info(session_id: str, user_id: str, user_name: str, state: Dict):
    """Display session information beautifully"""
    print_success("Session created successfully!")
    
    print(f"\n{colored('📋 Session Details:', Colors.BOLD)}")
    print("━" * 50)
    print(f"{colored('Session ID:', Colors.CYAN)} {session_id}")
    print(f"{colored('User:', Colors.CYAN)} {user_name} ({user_id})")
    
    print(f"\n{colored('State:', Colors.CYAN)}")
    for key, value in state.items():
        print(f"  • {key}: {value}")
    
    chat_url = f"{ADK_BASE_URL}/?session={session_id}"
    print(f"\n{colored('🔗 Chat URL:', Colors.GREEN + Colors.BOLD)}")
    print(chat_url)


def display_session_history():
    """Display all created sessions"""
    if not session_history:
        print_info("No sessions created yet.")
        return
    
    print_header(f"📊 Session History ({len(session_history)} sessions)")
    
    for i, session in enumerate(session_history, 1):
        print(f"\n{colored(f'{i}. {session['user_name']} ({session['user_id']})', Colors.BOLD)}")
        print(f"   Session: {session['session_id'][:16]}...")
        chat_url = f"{ADK_BASE_URL}/?session={session['session_id']}"
        print(f"   Chat: {colored(chat_url, Colors.CYAN)}")


def interactive_session_creator():
    """Main interactive loop"""
    print_header("🎯 ADK Session Creator")
    print_info("Create dynamic sessions with custom user information\n")
    
    while True:
        # Get user input
        print(colored("\nLet's create a new session!", Colors.BOLD))
        print()
        
        user_id = get_input("👤 User ID", required=True)
        user_name = get_input("📧 User Name", required=True)
        user_email = get_input("📨 Email (optional, press Enter to skip)", required=False)
        user_preferences = get_input("ℹ️  Preferences (optional, press Enter to skip)", required=False)
        conversation_context = get_input("💬 Conversation Context (optional, press Enter to skip)", required=False)
        
        # Create session
        session_id = create_session(
            user_id=user_id,
            user_name=user_name,
            user_email=user_email,
            user_preferences=user_preferences,
            conversation_context=conversation_context
        )
        
        if session_id:
            # Build state dict for display
            state = {"user_name": user_name}
            if user_email:
                state["user_email"] = user_email
            if user_preferences:
                state["user_preferences"] = user_preferences
            if conversation_context:
                state["conversation_context"] = conversation_context
            
            display_session_info(session_id, user_id, user_name, state)
        
        # Ask if user wants to create another
        print()
        another = get_input(
            colored("Create another session? (y/n)", Colors.YELLOW),
            required=False
        )
        
        if not another or another.lower() != 'y':
            break
    
    # Show history before exiting
    if session_history:
        print()
        display_session_history()
    
    print(f"\n{colored('👋 Goodbye!', Colors.GREEN + Colors.BOLD)}\n")


def main():
    """Entry point"""
    try:
        interactive_session_creator()
    except KeyboardInterrupt:
        print(f"\n\n{colored('👋 Goodbye!', Colors.YELLOW)}\n")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
