"""
🚀 Async Session Management Demo

High-performance concurrent session management using asyncio.
Demonstrates how to create and manage multiple sessions efficiently.
"""

import asyncio
import time
from typing import List, Dict, Optional

# Try to use aiohttp for async HTTP, fall back to requests
try:
    import aiohttp
    USE_ASYNC = True
except ImportError:
    import requests
    USE_ASYNC = False
    print("⚠️  aiohttp not installed. Using synchronous requests.")
    print("   Install aiohttp for better performance: pip install aiohttp\n")


# Configuration
ADK_BASE_URL = "http://localhost:8000"
AGENT_ID = "dynamic_session_agent"


class AsyncSessionClient:
    """Async session client using aiohttp"""
    
    def __init__(self, base_url: str = ADK_BASE_URL):
        self.base_url = base_url.rstrip('/')
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def create_session(self, user_name: str, user_email: str = None,
                           user_preferences: str = None) -> Optional[str]:
        """Create a new session"""
        state = {"user_name": user_name}
        if user_email:
            state["user_email"] = user_email
        if user_preferences:
            state["user_preferences"] = user_preferences
        
        try:
            async with self.session.post(
                f"{self.base_url}/sessions",
                json={"agent_id": AGENT_ID, "state": state},
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return data["session_id"]
        except Exception as e:
            print(f"❌ Error creating session: {e}")
            return None
    
    async def send_message(self, session_id: str, message: str) -> Optional[str]:
        """Send message to session"""
        try:
            async with self.session.post(
                f"{self.base_url}/chat",
                json={"session_id": session_id, "message": message},
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return data.get("response", data.get("text", ""))
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return None


class SyncSessionClient:
    """Fallback synchronous client using requests"""
    
    def __init__(self, base_url: str = ADK_BASE_URL):
        self.base_url = base_url.rstrip('/')
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
    
    async def create_session(self, user_name: str, user_email: str = None,
                           user_preferences: str = None) -> Optional[str]:
        """Create a new session (sync wrapped in async)"""
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
    
    async def send_message(self, session_id: str, message: str) -> Optional[str]:
        """Send message (sync wrapped in async)"""
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


# Use appropriate client based on aiohttp availability
SessionClient = AsyncSessionClient if USE_ASYNC else SyncSessionClient


def print_header(text: str):
    """Print a section header"""
    print(f"\n{'=' * 60}")
    print(text)
    print('=' * 60)


async def demo_1_concurrent_creation():
    """Demo 1: Create multiple sessions concurrently"""
    print_header("DEMO 1: Concurrent Session Creation")
    
    # Define users
    users = [
        {"name": f"User {i}", "email": f"user{i}@example.com", 
         "preferences": f"Test user number {i}"}
        for i in range(1, 11)  # 10 users
    ]
    
    print(f"\n⚡ Creating {len(users)} sessions concurrently...")
    
    async with SessionClient() as client:
        # Start timer
        start_time = time.time()
        
        # Create all sessions concurrently
        tasks = [
            client.create_session(
                user_name=user["name"],
                user_email=user["email"],
                user_preferences=user["preferences"]
            )
            for user in users
        ]
        
        session_ids = await asyncio.gather(*tasks)
        
        # End timer
        elapsed = time.time() - start_time
        
        # Count successful creations
        successful = sum(1 for sid in session_ids if sid is not None)
        
        print(f"✅ Created {successful}/{len(users)} sessions in {elapsed:.2f} seconds")
        print(f"📊 Average: {elapsed/len(users)*1000:.0f}ms per session")
        
        return [sid for sid in session_ids if sid is not None]


async def demo_2_parallel_messaging():
    """Demo 2: Send messages to multiple sessions in parallel"""
    print_header("DEMO 2: Parallel Message Broadcasting")
    
    # Create some sessions first
    print("\n📝 Creating test sessions...")
    
    users = [
        {"name": "Alice", "preferences": "Software engineer"},
        {"name": "Bob", "preferences": "Data scientist"},
        {"name": "Carol", "preferences": "Student"}
    ]
    
    async with SessionClient() as client:
        # Create sessions
        create_tasks = [
            client.create_session(
                user_name=user["name"],
                user_preferences=user["preferences"]
            )
            for user in users
        ]
        
        session_ids = await asyncio.gather(*create_tasks)
        session_ids = [sid for sid in session_ids if sid is not None]
        
        if not session_ids:
            print("❌ Failed to create sessions!")
            return
        
        print(f"✅ Created {len(session_ids)} sessions")
        
        # Send same message to all sessions
        message = "What can you help me with?"
        
        print(f"\n💬 Broadcasting message to {len(session_ids)} sessions...")
        print(f"   Message: '{message}'")
        
        start_time = time.time()
        
        # Send messages in parallel
        message_tasks = [
            client.send_message(session_id, message)
            for session_id in session_ids
        ]
        
        responses = await asyncio.gather(*message_tasks)
        
        elapsed = time.time() - start_time
        
        print(f"\n✅ Received {len(responses)} responses in {elapsed:.2f} seconds")
        print(f"📊 Average: {elapsed/len(responses)*1000:.0f}ms per message")
        
        # Show some responses
        print("\n📥 Sample responses:")
        for i, (user, response) in enumerate(zip(users, responses), 1):
            if response:
                preview = response[:100] + "..." if len(response) > 100 else response
                print(f"\n{i}. {user['name']}:")
                print(f"   {preview}")


async def demo_3_load_test():
    """Demo 3: Load test with many concurrent operations"""
    print_header("DEMO 3: Load Test")
    
    num_sessions = 20
    messages_per_session = 3
    
    print(f"\n🔥 Load Test Configuration:")
    print(f"   Sessions: {num_sessions}")
    print(f"   Messages per session: {messages_per_session}")
    print(f"   Total operations: {num_sessions * messages_per_session}")
    
    async with SessionClient() as client:
        # Phase 1: Create sessions
        print(f"\n⚡ Phase 1: Creating {num_sessions} sessions...")
        start_time = time.time()
        
        create_tasks = [
            client.create_session(
                user_name=f"LoadTest{i}",
                user_preferences=f"Load test user {i}"
            )
            for i in range(num_sessions)
        ]
        
        session_ids = await asyncio.gather(*create_tasks)
        session_ids = [sid for sid in session_ids if sid is not None]
        
        create_time = time.time() - start_time
        print(f"✅ Created {len(session_ids)} sessions in {create_time:.2f}s")
        
        if not session_ids:
            print("❌ Failed to create sessions!")
            return
        
        # Phase 2: Send messages
        print(f"\n⚡ Phase 2: Sending {len(session_ids) * messages_per_session} messages...")
        start_time = time.time()
        
        # Generate all message tasks
        message_tasks = []
        for session_id in session_ids:
            for i in range(messages_per_session):
                message_tasks.append(
                    client.send_message(session_id, f"Test message {i+1}")
                )
        
        responses = await asyncio.gather(*message_tasks)
        
        message_time = time.time() - start_time
        successful = sum(1 for r in responses if r is not None)
        
        print(f"✅ Completed {successful}/{len(message_tasks)} messages in {message_time:.2f}s")
        print(f"📊 Average: {message_time/len(message_tasks)*1000:.0f}ms per message")
        
        # Summary
        total_time = create_time + message_time
        total_ops = len(session_ids) + len(message_tasks)
        
        print(f"\n📊 Load Test Summary:")
        print(f"   Total time: {total_time:.2f}s")
        print(f"   Total operations: {total_ops}")
        print(f"   Throughput: {total_ops/total_time:.1f} ops/second")


async def demo_4_concurrent_conversations():
    """Demo 4: Multiple users having concurrent conversations"""
    print_header("DEMO 4: Concurrent Conversations")
    
    conversations = {
        "Alice": [
            "Hi! I'm a software engineer.",
            "I love Python programming.",
            "What do I do for work?"
        ],
        "Bob": [
            "Hello! I'm a data scientist.",
            "I work with machine learning.",
            "What's my profession?"
        ],
        "Carol": [
            "Hey! I'm a student.",
            "I'm learning computer science.",
            "What am I studying?"
        ]
    }
    
    print("\n💬 Starting concurrent conversations...")
    
    async with SessionClient() as client:
        # Create sessions for all users
        print("\n📝 Creating sessions...")
        sessions = {}
        
        create_tasks = [
            client.create_session(user_name=name)
            for name in conversations.keys()
        ]
        
        session_ids = await asyncio.gather(*create_tasks)
        
        for name, session_id in zip(conversations.keys(), session_ids):
            if session_id:
                sessions[name] = session_id
                print(f"   ✅ {name}")
        
        if not sessions:
            print("❌ Failed to create sessions!")
            return
        
        # Send all messages concurrently
        print("\n⚡ Sending all messages concurrently...")
        
        all_tasks = []
        message_map = []  # Track which message belongs to which user
        
        for name, messages in conversations.items():
            session_id = sessions[name]
            for msg in messages:
                all_tasks.append(client.send_message(session_id, msg))
                message_map.append((name, msg))
        
        start_time = time.time()
        responses = await asyncio.gather(*all_tasks)
        elapsed = time.time() - start_time
        
        print(f"✅ Completed {len(responses)} messages in {elapsed:.2f}s\n")
        
        # Display conversations
        for name in conversations.keys():
            print(f"\n{'━' * 60}")
            print(f"👤 {name}'s Conversation")
            print('━' * 60)
            
            user_responses = [
                (msg, resp) for (n, msg), resp in zip(message_map, responses)
                if n == name
            ]
            
            for msg, resp in user_responses:
                print(f"\n  User: {msg}")
                if resp:
                    preview = resp[:80] + "..." if len(resp) > 80 else resp
                    print(f"  Agent: {preview}")


async def main():
    """Run all demos"""
    print("🚀 Async Session Management Demo")
    print("=" * 60)
    
    if USE_ASYNC:
        print("✅ Using aiohttp for high-performance async HTTP")
    else:
        print("⚠️  Using requests (synchronous fallback)")
        print("   Install aiohttp for better performance:")
        print("   pip install aiohttp")
    
    print("\nMake sure ADK Web is running:")
    print("  cd d:\\agentic\\adk\\5.5-advanced-sessions")
    print("  adk web")
    print("\nPress Enter to continue...")
    input()
    
    try:
        # Run demos
        await demo_1_concurrent_creation()
        
        await asyncio.sleep(2)
        await demo_2_parallel_messaging()
        
        await asyncio.sleep(2)
        await demo_3_load_test()
        
        await asyncio.sleep(2)
        await demo_4_concurrent_conversations()
        
        # Summary
        print_header("✅ All Demos Completed!")
        print("\n📋 Summary:")
        print("  ✅ Demonstrated concurrent session creation")
        print("  ✅ Showed parallel message broadcasting")
        print("  ✅ Performed load testing")
        print("  ✅ Ran concurrent conversations")
        print("\n💡 Key Takeaways:")
        print("  • Async operations are much faster than sync")
        print("  • Can handle many concurrent sessions efficiently")
        print("  • Perfect for high-traffic applications")
        print("  • Each session remains isolated and independent")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
