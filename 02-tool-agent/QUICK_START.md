# 🚀 Quick Start Guide - Tool Agent

## ✅ Current Status
Agent has **4 working tools** (built-in tools NOT supported with standard Gemini API)

---

## 🎯 How to Run

```powershell
cd d:\agentic\adk\02-tool-agent
adk web
```

Open: **http://localhost:8000**

---

## 🔧 Available Tools

| Tool | Type | Speed | What it does |
|------|------|-------|--------------|
| **get_current_time** | Standard | Instant | Returns current timestamp |
| **get_date_info** | Standard | Instant | Day of week, month, year, etc |
| **analyze_large_dataset** | Long-running | 1-5s | Simulates data processing |
| **fetch_weather_data** | Long-running | 2s | Simulates weather API call |

---

## 💬 Try These Prompts

### Simple Queries:
- `"What time is it?"`
- `"What day is today?"`
- `"Fetch weather for Tokyo"`
- `"Analyze 2000 records"`

### Combined:
- `"Time, date, weather for NYC, analyze 3000 records"`

---

## ⚠️ What's NOT Available

❌ **google_search** - Requires Vertex AI  
❌ **built_in_code_execution** - Requires Vertex AI

These work only with enterprise Google Cloud setup.

---

## 📝 Files Created

- `agent.py` - Main agent configuration
- `AGENT_INFO.md` - Detailed documentation
- `TEST_PROMPTS.md` - 50+ test prompts to try
- `QUICK_START.md` - This file

---

## 🎨 What Makes This Agent Special

✅ Multiple custom tools working together  
✅ Long-running tool demonstration  
✅ Proper type hints and docstrings  
✅ Mock data for testing without real APIs  

---

## 🔍 Debug Tips

- Watch terminal for `[LONG-RUNNING]` messages
- Long tools take 1-5 seconds (you'll see delay)
- All tools can be used in single query
- Agent intelligently picks which tools to use

---

**Start testing! Open the web UI and try the prompts from TEST_PROMPTS.md** 🎉
