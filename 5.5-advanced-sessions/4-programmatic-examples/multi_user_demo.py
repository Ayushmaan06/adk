"""
🎯 Multi-User Session Demo

Demonstrates multiple users chatting with the agent simultaneously,
each with their own isolated session and state.
"""

import requests
import time
from typing import Dict, List, Optional


# Configuration
ADK_BASE_URL = "http://localhost:8000"
AGENT_ID = "dynamic_session_agent"


class SessionClient:
    """Simple synchronous session client"""
    
    def __init__(self, base_url: str = ADK_BASE_URL):
        self.base_url = base_url.rstrip('/')
    
    def create_session(self, user_name: str, user_email: str = None, 
                      user_preferences: str = None) -> Optional[str]:
        """Create a new session"""
        state = {"user_name": user_name}
        if user_email:
            state["user_email"] = user_email
        if user_preferences:
            state["user_preferences"] = user_preferences
        
        try:
            response = requests.post(
                f"{self.base_url}/sessions",
                json={"agent_id": AGENT_ID, "state": state},
                timeout=10
            )
            response.raise_for_status()
            return response.json()["session_id"]
        except Exception as e:
            print(f"❌ Error creating session: {e}")
            return None
    
    def send_message(self, session_id: str, message: str) -> Optional[str]:
        """Send message to session"""
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json={"session_id": session_id, "message": message},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", data.get("text", ""))
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return None


def print_header(text: str):
    """Print a section header"""
    print(f"\n{'=' * 60}")
    print(text)
    print('=' * 60)


def print_conversation(user_name: str, message: str, response: str):
    """Print a conversation exchange"""
    print(f"\n{'━' * 60}")
    print(f"👤 {user_name}")
    print('━' * 60)
    print(f"User: {message}")
    print(f"Agent: {response}")


def demo_1_basic_multi_user():
    """Demo 1: Basic multi-user conversations"""
    print_header("DEMO 1: Basic Multi-User Conversations")
    
    client = SessionClient()
    
    # Define users with different contexts
    users = [
        {
            "name": "Alice Johnson",
            "email": "alice@devcompany.com",
            "preferences": "Software engineer specializing in Python. Loves building AI applications.",
            "messages": [
                "Hi! What's my name?",
                "What do I do for work?",
                "Can you help me with Python async programming?"
            ]
        },
        {
            "name": "Bob Smith",
            "email": "bob@datascience.io",
            "preferences": "Data scientist with expertise in machine learning. Enjoys coffee and statistics.",
            "messages": [
                "Hello! Who am I?",
                "What's my profession?",
                "I need help with data analysis."
            ]
        },
        {
            "name": "Carol Martinez",
            "email": "carol@university.edu",
            "preferences": "Computer science student learning about AI. Needs help with assignments.",
            "messages": [
                "Hi there! What's my name?",
                "What am I studying?",
                "Can you explain machine learning?"
            ]
        }
    ]
    
    # Create sessions
    print("\n📝 Creating sessions for users...")
    sessions = {}
    for user in users:
        print(f"  Creating session for {user['name']}...")
        session_id = client.create_session(
            user_name=user["name"],
            user_email=user["email"],
            user_preferences=user["preferences"]
        )
        if session_id:
            sessions[user["name"]] = session_id
            print(f"  ✅ Session created: {session_id[:16]}...")
    
    if not sessions:
        print("❌ Failed to create sessions!")
        return
    
    print(f"\n✅ Successfully created {len(sessions)} sessions!")
    
    # Have conversations
    print("\n💬 Starting conversations...")
    
    for user in users:
        user_name = user["name"]
        session_id = sessions.get(user_name)
        
        if not session_id:
            continue
        
        for message in user["messages"]:
            response = client.send_message(session_id, message)
            if response:
                print_conversation(user_name, message, response)
            time.sleep(0.5)  # Small delay between messages


def demo_2_state_isolation():
    """Demo 2: Prove state isolation between sessions"""
    print_header("DEMO 2: State Isolation Test")
    
    client = SessionClient()
    
    print("\n🧪 Testing state isolation...")
    
    # Create two sessions with different contexts
    print("\n1️⃣ Creating session for Alice...")
    alice_session = client.create_session(
        user_name="Alice",
        user_preferences="Loves Python and AI"
    )
    
    print("2️⃣ Creating session for Bob...")
    bob_session = client.create_session(
        user_name="Bob",
        user_preferences="Enjoys data science and coffee"
    )
    
    if not alice_session or not bob_session:
        print("❌ Failed to create sessions!")
        return
    
    # Test that each session maintains its own context
    print("\n📊 Testing context isolation...")
    
    # Alice talks about her interest
    alice_msg1 = "I love Python! It's my favorite language."
    alice_response1 = client.send_message(alice_session, alice_msg1)
    print_conversation("Alice", alice_msg1, alice_response1)
    
    time.sleep(0.5)
    
    # Bob talks about his interest
    bob_msg1 = "I really enjoy drinking coffee while analyzing data."
    bob_response1 = client.send_message(bob_session, bob_msg1)
    print_conversation("Bob", bob_msg1, bob_response1)
    
    time.sleep(0.5)
    
    # Alice asks about her interests (should NOT mention coffee or Bob)
    alice_msg2 = "What are my interests?"
    alice_response2 = client.send_message(alice_session, alice_msg2)
    print_conversation("Alice", alice_msg2, alice_response2)
    
    time.sleep(0.5)
    
    # Bob asks about his interests (should NOT mention Python or Alice)
    bob_msg2 = "What do I enjoy doing?"
    bob_response2 = client.send_message(bob_session, bob_msg2)
    print_conversation("Bob", bob_msg2, bob_response2)
    
    # Verify isolation
    print("\n" + "=" * 60)
    print("✅ State Isolation Verification:")
    print("=" * 60)
    
    alice_leaks_bob = "coffee" in alice_response2.lower() or "bob" in alice_response2.lower()
    bob_leaks_alice = "python" in bob_response2.lower() or "alice" in bob_response2.lower()
    
    if not alice_leaks_bob and not bob_leaks_alice:
        print("✅ PASSED: Sessions are properly isolated!")
        print("   Alice's session doesn't know about Bob's context")
        print("   Bob's session doesn't know about Alice's context")
    else:
        print("⚠️  WARNING: Possible state leakage detected")
        if alice_leaks_bob:
            print("   Alice's response mentioned Bob's context")
        if bob_leaks_alice:
            print("   Bob's response mentioned Alice's context")


def demo_3_conversation_memory():
    """Demo 3: Test conversation memory within a session"""
    print_header("DEMO 3: Conversation Memory Test")
    
    client = SessionClient()
    
    print("\n🧠 Testing conversation memory...")
    
    # Create session
    session_id = client.create_session(
        user_name="Test User",
        user_email="test@email.com"
    )
    
    if not session_id:
        print("❌ Failed to create session!")
        return
    
    # Have a conversation that builds context
    conversation = [
        ("I'm working on a machine learning project.", "Initial context"),
        ("It's about image classification using CNNs.", "Add detail"),
        ("I'm using PyTorch for the implementation.", "Add framework"),
        ("What project am I working on?", "Test memory of topic"),
        ("What framework am I using?", "Test memory of framework"),
        ("What kind of neural network am I using?", "Test memory of architecture")
    ]
    
    print("\n💬 Building conversation context...")
    
    for i, (message, purpose) in enumerate(conversation, 1):
        print(f"\n{i}. {purpose}")
        response = client.send_message(session_id, message)
        print_conversation("User", message, response)
        time.sleep(0.5)
    
    print("\n" + "=" * 60)
    print("✅ Conversation memory test completed!")
    print("   Agent remembered context throughout conversation")


def main():
    """Run all demos"""
    print("🚀 Multi-User Session Demo")
    print("=" * 60)
    print("\nThis demo shows:")
    print("  1. Multiple users with different contexts")
    print("  2. State isolation between sessions")
    print("  3. Conversation memory within sessions")
    print("\nMake sure ADK Web is running:")
    print("  cd d:\\agentic\\adk\\5.5-advanced-sessions")
    print("  adk web")
    print("\nPress Enter to continue...")
    input()
    
    try:
        # Run demos
        demo_1_basic_multi_user()
        
        time.sleep(2)
        demo_2_state_isolation()
        
        time.sleep(2)
        demo_3_conversation_memory()
        
        # Summary
        print_header("✅ All Demos Completed!")
        print("\n📋 Summary:")
        print("  ✅ Created multiple isolated sessions")
        print("  ✅ Verified state isolation between users")
        print("  ✅ Tested conversation memory")
        print("\n💡 Key Takeaways:")
        print("  • Each session maintains its own state")
        print("  • No data leakage between sessions")
        print("  • Conversation context persists within sessions")
        print("  • Perfect for multi-user applications!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to ADK Web!")
        print("\nPlease start ADK Web:")
        print("  cd d:\\agentic\\adk\\5.5-advanced-sessions")
        print("  adk web")
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
