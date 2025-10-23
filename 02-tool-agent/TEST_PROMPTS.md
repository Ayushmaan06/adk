# Test Prompts for Tool Agent (Working Tools Only)

These prompts work with the **4 custom tools** currently available:
- ⏰ `get_current_time`
- ⏰ `get_date_info`
- ⏱️ `analyze_large_dataset` (long-running)
- ⏱️ `fetch_weather_data` (long-running)

---

## ⏰ Test DateTime Tools

### Current Time
```
What's the current time?
```

```
Tell me the exact time right now
```

```
Can you show me the current time in YYYY-MM-DD HH:MM:SS format?
```

### Date Information
```
Give me detailed information about today's date
```

```
What day of the week is it?
```

```
Tell me the current month, year, and what day of the year we're on
```

```
What's today's date with all the details?
```

---

## ⏱️ Test Long-Running Tools

### Dataset Analysis (1-5 seconds)
```
Analyze a dataset with 2000 records
```

```
I need you to analyze a large dataset of 5000 records. Let me know how long it takes.
```

```
Process and analyze 1000 records from my dataset
```

```
Analyze 3500 records and tell me the processing time
```

### Weather Data (2 seconds)
```
Fetch the weather data for New York
```

```
What's the weather like in Tokyo?
```

```
Get me weather information for London
```

```
Check the weather in Paris
```

```
Show me the weather conditions for Berlin
```

---

## 🔥 Test Multiple Tools Together

### Combining 2 Tools
```
What's the current time, and then fetch the weather for New York?
```

```
Tell me today's date information, then analyze a dataset of 2000 records
```

```
Get the current time and analyze 1500 records
```

```
First fetch weather for Tokyo, then tell me what time it is
```

### Combining 3+ Tools
```
Tell me the current time, give me detailed date info, and then analyze 2500 records
```

```
Get today's date, fetch weather for London, and analyze 3000 records
```

```
First, what time is it? Then get detailed date info. Finally, fetch weather for New York
```

### Complex Multi-Step Query
```
I need a complete report: 
1. Get current date and time
2. Analyze a dataset of 3000 records
3. Fetch weather for Tokyo
4. Tell me what day of the week it is
```

```
Give me everything: current time, date details, weather for London, and analyze 2000 records
```

---

## 🎯 Test Intelligent Tool Selection

### Agent Should Choose Correct Tool
```
I need to know what time it is (use only time tool, not date)
```

```
Just tell me the day of the week and month
```

```
Only fetch weather for Paris, nothing else
```

```
Only analyze 1000 records, no other tools
```

---

## 💡 Creative & Fun Queries

### Creative Combination
```
Pretend you're a weather reporter. Get the current time, fetch weather for New York, and present it like a TV weather forecast
```

```
I'm a data scientist. Get today's date, analyze 4000 records, and give me a professional report
```

### Story-Based Query
```
I'm planning my day. First tell me what time it is, then check the weather for London, and finally help me analyze how much data I can process (try 2500 records)
```

```
Create a morning briefing: current time, today's date, weather in Tokyo, and dataset analysis for 3000 records
```

---

## 🧪 Edge Cases & Error Handling

### Test Long Processing
```
Analyze a dataset with 10000 records (this will be capped at 5 seconds)
```

### Test Invalid City (Mock Data)
```
Fetch weather for "XYZ_NonExistent_City_123" (agent will return default mock data)
```

### Rapid Multiple Tools
```
Quick! Give me time, date, weather for Paris, and analyze 1000 records - all at once!
```

---

## 📊 Expected Behavior

| Tool | Response Time | Output |
|------|--------------|---------|
| `get_current_time` | Instant | `{"current_time": "2025-10-17 20:30:45"}` |
| `get_date_info` | Instant | Day of week, month, year, day of year |
| `analyze_large_dataset` | 1-5 seconds | Processing stats, time taken |
| `fetch_weather_data` | ~2 seconds | Temperature, condition, humidity |

---

## 🚀 Quick Start

1. **Start the web UI:**
   ```powershell
   cd d:\agentic\adk\02-tool-agent
   adk web
   ```

2. **Open browser:** http://localhost:8000

3. **Paste any prompt** from above and test!

4. **Watch terminal** for `[LONG-RUNNING]` debug messages

---

## 💡 Pro Tips

- Long-running tools will show progress in the terminal
- You can combine all 4 tools in a single query
- The agent will automatically select the right tools
- Mock weather returns different data for: New York, London, Tokyo, or default
- Dataset analysis time scales with size (max 5 seconds)

**Happy Testing! 🎉**
