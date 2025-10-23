# Tool Agent - Configuration Summary

## ✅ Successfully Configured!

This agent now has **4 tools** configured:

### ⏰ Custom DateTime Tools (2)
1. **get_current_time** - Get current time in YYYY-MM-DD HH:MM:SS format
2. **get_date_info** - Get detailed date info (day of week, month, year, day of year)

### ⏱️ Long-running Tools (2)
3. **analyze_large_dataset** - Simulates analyzing large datasets (1-5 seconds)
4. **fetch_weather_data** - Simulates fetching weather from API (2 seconds)

---

## ⚠️ Important Note About Built-in Tools

### ❌ NOT Supported with Standard Gemini API:
- `google_search` - NOT available (requires Vertex AI)
- `built_in_code_execution` - NOT available (requires Vertex AI)

**Error Message:** `Code execution and search tool is not supported`

These built-in tools require:
- Vertex AI API access
- Enterprise Google Cloud configuration
- Different API endpoints

### ✅ What DOES Work:
- **Custom function tools** (like our datetime tools)
- **Long-running tools** with `LongRunningFunctionTool` wrapper
- **Multiple custom tools** can be used together

### ✅ Long-running Tools Implementation
To create long-running tools in ADK:

1. **Define a regular function** with proper docstring and type hints
2. **Wrap it with `LongRunningFunctionTool()`**
3. **Add to tools list**

```python
from google.adk.tools.long_running_tool import LongRunningFunctionTool

def my_long_task(param: str) -> dict:
    """Description of what this tool does."""
    time.sleep(5)  # Simulate long operation
    return {"result": "done"}

# In agent configuration:
tools=[
    LongRunningFunctionTool(my_long_task),
]
```

---

## 🚀 How to Run

### Start Web UI:
```powershell
cd d:\agentic\adk\02-tool-agent
adk web
```
Then open: http://localhost:8000

### Start CLI:
```powershell
cd d:\agentic\adk\02-tool-agent
adk run tool_agent
```

---

## 💡 Example Queries to Test

### Test Built-in Tools:
- "Search for the latest AI news"
- "Execute this Python code: print(sum([1,2,3,4,5]))"

### Test DateTime Tools:
- "What's the current time?"
- "Give me detailed date information"

### Test Long-running Tools:
- "Analyze a dataset of 3000 records"
- "Fetch weather data for Tokyo"

### Test Multiple Tools Together:
- "What's the current time, and then search Google for today's weather forecast?"
- "Get today's date and execute code to calculate days until Christmas"

---

## 🔍 Available ADK Built-in Tools

According to the ADK library, these built-in tools are available:
- `google_search` ✅ (used)
- `built_in_code_execution` ✅ (used)
- `exit_loop` - For loop-based agents
- `get_user_choice` - For interactive user input
- `load_artifacts` - Load artifacts from storage
- `load_memory` - Load memory from storage
- `preload_memory` - Preload memory before agent execution
- `transfer_to_agent` - Transfer control to another agent
- `vertex_ai_search` - Vertex AI search tool
- `apihub_tool` - API Hub integration

You can add more built-in tools to test them out!

---

## 🐛 Common Issues & Solutions

### Issue: "Tools don't work"
**Solution:** Ensure:
1. ✅ Function has proper docstring (LLM needs it!)
2. ✅ Parameters have type hints
3. ✅ Function returns a dict
4. ✅ Import is correct

### Issue: "Long-running tool fails"
**Solution:** 
- Use `LongRunningFunctionTool(function)` wrapper, not decorator
- Import: `from google.adk.tools.long_running_tool import LongRunningFunctionTool`

### Issue: "Multiple tools conflict"
**Solution:**
- This shouldn't happen! ADK supports multiple tools
- Check for naming conflicts
- Ensure all tools have unique names
