"""
Dynamic Session Agent - Handles Empty State Gracefully

This agent demonstrates proper dynamic state management:
✅ No hardcoded initial_state
✅ Uses Jinja2 conditionals to handle missing variables
✅ Asks users for information when state is empty
✅ State is populated dynamically per session
"""

from google.adk import Agent

# Dynamic instruction that handles empty state gracefully
instruction = """
You are a helpful and personalized assistant.

{%- if user_name %}
Current User: {{user_name}}
{%- else %}
Note: I don't know who I'm talking to yet.
{%- endif %}

{%- if user_email %}
Email: {{user_email}}
{%- endif %}

{%- if user_preferences %}
User Information: {{user_preferences}}
{%- endif %}

{%- if conversation_context %}
Context: {{conversation_context}}
{%- endif %}

BEHAVIOR:
- If you don't know the user's name, politely introduce yourself and ask for their name
- If you don't know their preferences, ask what they're interested in
- Use the information they provide to personalize the conversation
- Remember everything they tell you across the conversation
- Be warm, helpful, and conversational

IMPORTANT:
- Build context naturally through conversation
- Don't repeatedly ask for information you already know
- Reference previous conversation points when relevant
"""

# Create the agent with dynamic state handling
dynamic_session_agent = Agent(
    name="dynamic_session_agent",
    model="gemini-2.0-flash",
    instruction=instruction,
    description="A dynamic session agent that handles empty state gracefully and builds context naturally"
)

# ADK Web looks for 'root_agent' variable
root_agent = dynamic_session_agent

# Export for programmatic use
__all__ = ["dynamic_session_agent", "root_agent"]
