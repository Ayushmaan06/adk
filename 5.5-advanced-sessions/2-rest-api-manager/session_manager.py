"""
🔌 Session Manager - REST API Client for ADK

A clean Python interface for managing ADK sessions programmatically.
"""

import requests
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin


class SessionManager:
    """
    Manages ADK sessions via REST API.
    
    Features:
    - Create sessions with custom state
    - Send messages to sessions
    - List and manage sessions
    - Clean error handling
    
    Example:
        >>> manager = SessionManager()
        >>> session_id = manager.create_session(
        ...     agent_id="dynamic_session_agent",
        ...     user_name="Alice",
        ...     user_email="alice@email.com"
        ... )
        >>> response = manager.send_message(session_id, "Hello!")
        >>> print(response)
    """
    
    def __init__(self, base_url: str = "http://localhost:8000", timeout: int = 30):
        """
        Initialize SessionManager.
        
        Args:
            base_url: ADK Web server URL (default: http://localhost:8000)
            timeout: Request timeout in seconds (default: 30)
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
    
    def create_session(
        self,
        agent_id: str,
        user_name: str,
        user_email: Optional[str] = None,
        user_preferences: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Create a new session with custom state.
        
        Args:
            agent_id: The agent to use (e.g., "dynamic_session_agent")
            user_name: User's full name (required)
            user_email: User's email (optional)
            user_preferences: User preferences/context (optional)
            **kwargs: Additional state variables
        
        Returns:
            str: Session UUID
        
        Raises:
            ConnectionError: If cannot connect to ADK Web
            ValueError: If request fails
        
        Example:
            >>> session_id = manager.create_session(
            ...     agent_id="dynamic_session_agent",
            ...     user_name="Alice Johnson",
            ...     user_email="alice@email.com",
            ...     user_preferences="Software engineer, loves Python",
            ...     custom_field="custom value"
            ... )
        """
        # Build state dict
        state = {"user_name": user_name}
        
        if user_email:
            state["user_email"] = user_email
        if user_preferences:
            state["user_preferences"] = user_preferences
        
        # Add any additional state variables
        state.update(kwargs)
        
        # Make request
        url = urljoin(self.base_url, "/sessions")
        payload = {
            "agent_id": agent_id,
            "state": state
        }
        
        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            return data["session_id"]
        
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Cannot connect to ADK Web at {self.base_url}. "
                "Make sure 'adk web' is running."
            )
        except requests.exceptions.Timeout:
            raise TimeoutError(f"Request timed out after {self.timeout} seconds")
        except requests.exceptions.HTTPError as e:
            raise ValueError(f"Failed to create session: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise ValueError(f"Unexpected error: {str(e)}")
    
    def send_message(self, session_id: str, message: str) -> str:
        """
        Send a message to a session and get the response.
        
        Args:
            session_id: Session UUID
            message: Message to send to the agent
        
        Returns:
            str: Agent's response text
        
        Raises:
            ConnectionError: If cannot connect to ADK Web
            ValueError: If session doesn't exist or request fails
        
        Example:
            >>> response = manager.send_message(session_id, "What's my name?")
            >>> print(response)
            "Your name is Alice Johnson!"
        """
        url = urljoin(self.base_url, "/chat")
        payload = {
            "session_id": session_id,
            "message": message
        }
        
        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            return data.get("response", data.get("text", ""))
        
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Cannot connect to ADK Web at {self.base_url}. "
                "Make sure 'adk web' is running."
            )
        except requests.exceptions.Timeout:
            raise TimeoutError(f"Request timed out after {self.timeout} seconds")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Session not found: {session_id}")
            raise ValueError(f"Failed to send message: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise ValueError(f"Unexpected error: {str(e)}")
    
    def list_sessions(self, agent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all active sessions.
        
        Args:
            agent_id: Optional filter by agent (not currently supported by ADK Web)
        
        Returns:
            List[Dict]: List of session objects with metadata and state
        
        Example:
            >>> sessions = manager.list_sessions()
            >>> for session in sessions:
            ...     print(f"{session['session_id']}: {session['state']['user_name']}")
        """
        url = urljoin(self.base_url, "/sessions")
        
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            sessions = data.get("sessions", [])
            
            # Filter by agent_id if specified
            if agent_id:
                sessions = [s for s in sessions if s.get("agent_id") == agent_id]
            
            return sessions
        
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Cannot connect to ADK Web at {self.base_url}. "
                "Make sure 'adk web' is running."
            )
        except requests.exceptions.Timeout:
            raise TimeoutError(f"Request timed out after {self.timeout} seconds")
        except Exception as e:
            raise ValueError(f"Unexpected error: {str(e)}")
    
    def get_session(self, session_id: str) -> Dict[str, Any]:
        """
        Get details for a specific session.
        
        Args:
            session_id: Session UUID
        
        Returns:
            Dict: Session object with metadata and state
        
        Example:
            >>> details = manager.get_session(session_id)
            >>> print(details['state']['user_name'])
            "Alice Johnson"
        """
        url = urljoin(self.base_url, f"/sessions/{session_id}")
        
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            return response.json()
        
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Cannot connect to ADK Web at {self.base_url}. "
                "Make sure 'adk web' is running."
            )
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Session not found: {session_id}")
            raise ValueError(f"Failed to get session: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise ValueError(f"Unexpected error: {str(e)}")
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.
        
        Args:
            session_id: Session UUID
        
        Returns:
            bool: True if deleted successfully
        
        Example:
            >>> manager.delete_session(session_id)
            True
        """
        url = urljoin(self.base_url, f"/sessions/{session_id}")
        
        try:
            response = requests.delete(url, timeout=self.timeout)
            response.raise_for_status()
            return True
        
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Cannot connect to ADK Web at {self.base_url}. "
                "Make sure 'adk web' is running."
            )
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Session not found: {session_id}")
            raise ValueError(f"Failed to delete session: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise ValueError(f"Unexpected error: {str(e)}")
    
    def get_chat_url(self, session_id: str) -> str:
        """
        Get direct URL to chat with a session in ADK Web UI.
        
        Args:
            session_id: Session UUID
        
        Returns:
            str: Full URL to chat interface
        
        Example:
            >>> url = manager.get_chat_url(session_id)
            >>> print(f"Chat here: {url}")
        """
        return f"{self.base_url}/?session={session_id}"


# Example usage
if __name__ == "__main__":
    # Create manager
    manager = SessionManager()
    
    # Create session
    print("Creating session for Alice...")
    alice_session = manager.create_session(
        agent_id="dynamic_session_agent",
        user_name="Alice Johnson",
        user_email="alice@devcompany.com",
        user_preferences="Software engineer, loves Python"
    )
    print(f"✅ Session created: {alice_session}")
    
    # Send messages
    print("\n📤 Sending messages...")
    response1 = manager.send_message(alice_session, "Hi! What's my name?")
    print(f"Agent: {response1}")
    
    response2 = manager.send_message(alice_session, "What do you know about me?")
    print(f"Agent: {response2}")
    
    # Get session details
    print("\n📊 Session details:")
    details = manager.get_session(alice_session)
    print(f"State: {details['state']}")
    
    # Get chat URL
    print(f"\n💬 Chat URL: {manager.get_chat_url(alice_session)}")
    
    print("\n✅ Done! Try the chat URL in your browser!")
