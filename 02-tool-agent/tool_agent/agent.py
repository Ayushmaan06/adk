from datetime import datetime
import time
from google.adk.agents import Agent
# NOTE: google_search and built_in_code_execution are NOT supported with gemini-2.0-flash
# Error: "Code execution and search tool is not supported"
# These tools may require Vertex AI or specific API configurations
from google.adk.tools.long_running_tool import LongRunningFunctionTool

# NOTE: Built-in tools like google_search and built_in_code_execution are NOT available
# with the standard Gemini API. They require Vertex AI or enterprise features.
# However, you CAN create custom tools and long-running tools! ✅

# ==================== Custom Tools ====================

def get_current_time() -> dict:
    """
    Get the current time in the format YYYY-MM-DD HH:MM:SS.
    
    Returns:
        dict: Contains the current_time string
    """
    return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def get_date_info() -> dict:
    """
    Get detailed date information including day of week, month, year.
    
    Returns:
        dict: Contains date, day_of_week, month, year, day_of_year
    """
    now = datetime.now()
    return {
        "date": now.strftime("%Y-%m-%d"),
        "day_of_week": now.strftime("%A"),
        "month": now.strftime("%B"),
        "year": now.year,
        "day_of_year": now.timetuple().tm_yday,
    }


# ==================== Long-running Tool Functions ====================
# These are regular functions that will be wrapped in LongRunningFunctionTool

def analyze_large_dataset(data_size: int) -> dict:
    """
    Simulate analyzing a large dataset. This is a long-running operation.
    
    Args:
        data_size: The size of the dataset to analyze (in thousands of records)
    
    Returns:
        dict: Analysis results including status, processing_time, records_processed
    """
    print(f"[LONG-RUNNING] Starting analysis of {data_size}k records...")
    
    # Simulate processing time (1 second per 1000 records)
    processing_time = min(data_size / 1000, 5)  # Cap at 5 seconds
    time.sleep(processing_time)
    
    print(f"[LONG-RUNNING] Analysis complete!")
    
    return {
        "status": "completed",
        "records_processed": data_size * 1000,
        "processing_time_seconds": processing_time,
        "insights": f"Successfully analyzed {data_size}k records",
    }


def fetch_weather_data(city: str) -> dict:
    """
    Simulate fetching weather data from an external API (long-running operation).
    
    Args:
        city: The name of the city to get weather for
    
    Returns:
        dict: Weather information for the city
    """
    print(f"[LONG-RUNNING] Fetching weather data for {city}...")
    
    # Simulate API call delay
    time.sleep(2)
    
    # Mock weather data
    weather_mock = {
        "new york": {"temp": 72, "condition": "Sunny", "humidity": 65},
        "london": {"temp": 58, "condition": "Cloudy", "humidity": 78},
        "tokyo": {"temp": 68, "condition": "Rainy", "humidity": 82},
        "default": {"temp": 70, "condition": "Clear", "humidity": 60},
    }
    
    weather = weather_mock.get(city.lower(), weather_mock["default"])
    
    print(f"[LONG-RUNNING] Weather data retrieved!")
    
    return {
        "city": city,
        "temperature_f": weather["temp"],
        "condition": weather["condition"],
        "humidity_percent": weather["humidity"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


# ==================== Agent Configuration ====================

root_agent = Agent(
    name="tool_agent",
    model="gemini-2.0-flash",
    description="Advanced tool agent with datetime and long-running capabilities",
    instruction="""
    You are a helpful assistant with multiple tools at your disposal:
    
    **Time & Date Tools:**
    - get_current_time: Get the current time in YYYY-MM-DD HH:MM:SS format
    - get_date_info: Get detailed date information (day of week, month, year, day of year)
    
    **Long-running Tools (these take time, inform user):**
    - analyze_large_dataset: Analyze large datasets (simulation, takes 1-5 seconds)
    - fetch_weather_data: Fetch weather information (simulation, takes 2 seconds)
    
    When using long-running tools, let the user know that the operation 
    will take a few moments to complete.
    
    You can combine multiple tools to answer complex queries!
    
    NOTE: You do NOT have access to web search or code execution tools.
    """,
    tools=[
        # Custom datetime tools (regular functions)
        get_current_time,
        get_date_info,
        # Long-running tools (wrapped in LongRunningFunctionTool)
        LongRunningFunctionTool(analyze_large_dataset),
        LongRunningFunctionTool(fetch_weather_data),
    ],
)

# ==================== Notes ====================
# ⚠️ NO: Built-in tools (google_search, built_in_code_execution) NOT supported with standard Gemini API
# ✅ YES: Custom tools work perfectly!
# ✅ YES: Long-running tools work with LongRunningFunctionTool wrapper
# ℹ️  INFO: Built-in tools require Vertex AI or enterprise API access
# 
# How to use long-running tools:
# 1. Define a regular function with proper docstring and type hints
# 2. Wrap it with LongRunningFunctionTool(your_function)
# 3. Add to the tools list
# 
# Common issues that might prevent multiple tools from working:
# 1. Missing docstrings (LLM needs them to understand the tool)
# 2. Missing type hints on function parameters
# 3. Incorrect function signatures
# 4. Not importing the tools properly