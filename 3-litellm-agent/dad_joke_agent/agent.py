import os
import random

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# ==================== LiteLLM Model Configuration ====================
# LiteLLM allows you to use ANY LLM provider with a unified interface!
# https://docs.litellm.ai/docs/providers

# OPTION 1: Google Gemini (using your existing API key) ✅ RECOMMENDED
model = LiteLlm(
    model="gemini/gemini-2.0-flash-exp",  # gemini/ prefix for LiteLLM
    api_key=os.getenv("GOOGLE_API_KEY"),
)

# OPTION 2: OpenRouter (free models often rate-limited) ⚠️
# model = LiteLlm(
#     model="openrouter/meta-llama/llama-3.2-3b-instruct:free",  # Different free model
#     api_key=os.getenv("OPENROUTER_API_KEY"),
#     api_base="https://openrouter.ai/api/v1",
# )

# OPTION 3: OpenAI (requires OpenAI API key)
# model = LiteLlm(
#     model="gpt-4o-mini",
#     api_key=os.getenv("OPENAI_API_KEY"),
# )

# OPTION 4: Anthropic Claude (requires Anthropic API key)
# model = LiteLlm(
#     model="claude-3-5-sonnet-20241022",
#     api_key=os.getenv("ANTHROPIC_API_KEY"),
# )

# OPTION 5: Ollama (local models, free but requires Ollama installed)
# model = LiteLlm(
#     model="ollama/llama3.2",
#     api_base="http://localhost:11434",
# )

# Learn more: https://docs.litellm.ai/docs/providers


def get_dad_joke():
    jokes = [
        "Why did the chicken cross the road? To get to the other side!",
        "What do you call a belt made of watches? A waist of time.",
        "What do you call fake spaghetti? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
    ]
    return random.choice(jokes)


root_agent = Agent(
    name="dad_joke_agent",
    model=model,
    description="Dad joke agent",
    instruction="""
    You are a helpful assistant that can tell dad jokes. 
    Only use the tool `get_dad_joke` to tell jokes.
    """,
    tools=[get_dad_joke],
)
