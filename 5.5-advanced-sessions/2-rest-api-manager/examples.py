"""
🎯 Session Manager Examples

Demonstrates all features of the SessionManager class.
"""

from session_manager import SessionManager
import time


def example_1_simple_chat():
    """Example 1: Simple chat with one user"""
    print("=" * 60)
    print("EXAMPLE 1: Simple Chat")
    print("=" * 60)
    
    manager = SessionManager()
    
    # Create session
    print("\n📝 Creating session for Alice...")
    session_id = manager.create_session(
        agent_id="dynamic_session_agent",
        user_name="Alice Johnson",
        user_email="alice@email.com",
        user_preferences="Software engineer, loves Python"
    )
    print(f"✅ Session ID: {session_id}")
    
    # Chat
    messages = [
        "Hi! What's my name?",
        "What do I do for work?",
        "Can you remember my email?"
    ]
    
    print("\n💬 Chatting...")
    for msg in messages:
        print(f"\n👤 User: {msg}")
        response = manager.send_message(session_id, msg)
        print(f"🤖 Agent: {response}")
    
    print(f"\n🔗 Chat URL: {manager.get_chat_url(session_id)}")


def example_2_multiple_users():
    """Example 2: Multiple users with different contexts"""
    print("\n\n" + "=" * 60)
    print("EXAMPLE 2: Multiple Users")
    print("=" * 60)
    
    manager = SessionManager()
    
    # Create sessions for multiple users
    users = [
        {
            "name": "Alice Johnson",
            "email": "alice@devcompany.com",
            "preferences": "Software engineer specializing in Python. Loves building AI applications."
        },
        {
            "name": "Bob Smith",
            "email": "bob@datascience.io",
            "preferences": "Data scientist with expertise in machine learning. Enjoys coffee."
        },
        {
            "name": "Carol Martinez",
            "email": "carol@university.edu",
            "preferences": "Computer science student learning about AI. Needs help with assignments."
        }
    ]
    
    sessions = {}
    
    print("\n📝 Creating sessions...")
    for user in users:
        session_id = manager.create_session(
            agent_id="dynamic_session_agent",
            user_name=user["name"],
            user_email=user["email"],
            user_preferences=user["preferences"]
        )
        sessions[user["name"]] = session_id
        print(f"✅ {user['name']}: {session_id}")
    
    # Send same question to all users
    question = "What can you help me with today?"
    
    print(f"\n💬 Sending to all users: '{question}'")
    print("-" * 60)
    
    for name, session_id in sessions.items():
        print(f"\n👤 {name}:")
        response = manager.send_message(session_id, question)
        print(f"🤖 {response}")
        time.sleep(0.5)  # Small delay between requests


def example_3_session_management():
    """Example 3: Session management operations"""
    print("\n\n" + "=" * 60)
    print("EXAMPLE 3: Session Management")
    print("=" * 60)
    
    manager = SessionManager()
    
    # Create a few test sessions
    print("\n📝 Creating test sessions...")
    test_users = ["Alice", "Bob", "Carol"]
    created_sessions = []
    
    for name in test_users:
        session_id = manager.create_session(
            agent_id="dynamic_session_agent",
            user_name=name,
            user_preferences=f"Test user {name}"
        )
        created_sessions.append(session_id)
        print(f"✅ Created session for {name}")
    
    # List all sessions
    print("\n📊 Listing all sessions...")
    all_sessions = manager.list_sessions()
    print(f"Total active sessions: {len(all_sessions)}")
    
    for session in all_sessions:
        user_name = session.get('state', {}).get('user_name', 'Unknown')
        session_id = session.get('session_id', 'Unknown')
        print(f"  - {user_name}: {session_id[:16]}...")
    
    # Get details for first session
    if created_sessions:
        print(f"\n🔍 Details for first session:")
        details = manager.get_session(created_sessions[0])
        print(f"  Session ID: {details.get('session_id', 'Unknown')}")
        print(f"  State: {details.get('state', {})}")
    
    # Clean up test sessions
    print(f"\n🗑️ Cleaning up test sessions...")
    for session_id in created_sessions:
        try:
            manager.delete_session(session_id)
            print(f"✅ Deleted session {session_id[:16]}...")
        except Exception as e:
            print(f"❌ Failed to delete: {e}")


def example_4_error_handling():
    """Example 4: Error handling"""
    print("\n\n" + "=" * 60)
    print("EXAMPLE 4: Error Handling")
    print("=" * 60)
    
    manager = SessionManager()
    
    # Test with invalid session ID
    print("\n🧪 Testing with invalid session ID...")
    try:
        response = manager.send_message("invalid-session-id", "Hello")
        print(f"Response: {response}")
    except ValueError as e:
        print(f"✅ Caught expected error: {e}")
    
    # Test connection error (wrong port)
    print("\n🧪 Testing connection to wrong port...")
    bad_manager = SessionManager(base_url="http://localhost:9999")
    try:
        bad_manager.create_session(
            agent_id="test",
            user_name="Test"
        )
    except ConnectionError as e:
        print(f"✅ Caught expected error: {e}")
    
    # Test timeout (very short timeout)
    print("\n🧪 Testing with short timeout...")
    timeout_manager = SessionManager(timeout=0.001)
    try:
        timeout_manager.list_sessions()
    except TimeoutError as e:
        print(f"✅ Caught expected error: {e}")


def example_5_state_persistence():
    """Example 5: State persistence across messages"""
    print("\n\n" + "=" * 60)
    print("EXAMPLE 5: State Persistence")
    print("=" * 60)
    
    manager = SessionManager()
    
    # Create session
    print("\n📝 Creating session...")
    session_id = manager.create_session(
        agent_id="dynamic_session_agent",
        user_name="Test User",
        user_email="test@email.com"
    )
    
    # Have a conversation that builds context
    conversation = [
        "Hi! I'm working on a Python project.",
        "I need help with async programming.",
        "Can you remind me what project I'm working on?",
        "And what topic did I need help with?"
    ]
    
    print("\n💬 Testing context persistence...")
    for i, msg in enumerate(conversation, 1):
        print(f"\n{i}. 👤 User: {msg}")
        response = manager.send_message(session_id, msg)
        print(f"   🤖 Agent: {response}")
        time.sleep(0.5)


def main():
    """Run all examples"""
    print("🚀 Session Manager Examples")
    print("=" * 60)
    print("\nMake sure ADK Web is running:")
    print("  cd d:\\agentic\\adk\\5.5-advanced-sessions")
    print("  adk web")
    print("\nPress Enter to continue...")
    input()
    
    try:
        # Run examples
        example_1_simple_chat()
        
        time.sleep(2)
        example_2_multiple_users()
        
        time.sleep(2)
        example_3_session_management()
        
        time.sleep(2)
        example_4_error_handling()
        
        time.sleep(2)
        example_5_state_persistence()
        
        print("\n\n" + "=" * 60)
        print("✅ All examples completed!")
        print("=" * 60)
        print("\n💡 Tips:")
        print("  - Use manager.create_session() to create unique sessions")
        print("  - Each session maintains its own state and context")
        print("  - Sessions are isolated - no data leakage")
        print("  - Use manager.get_chat_url() to chat in browser")
        
    except ConnectionError:
        print("\n❌ Cannot connect to ADK Web!")
        print("\nPlease start ADK Web:")
        print("  cd d:\\agentic\\adk\\5.5-advanced-sessions")
        print("  adk web")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
