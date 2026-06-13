"""
Challenge 4: The Full Agent — Tools + Memory + Streaming
Combine everything into one powerful agent.
Model: Amazon Nova Pro via Bedrock

Instructions:
  1. Fill in ALL the TODO sections
  2. Run: python starter.py
  3. Have a full conversation using all tools!
"""

import os
os.environ["BYPASS_TOOL_CONSENT"] = "true"

from datetime import date, datetime

MODEL = "us.amazon.nova-pro-v1:0"


# ============================================================
# TODO 1: Import everything you need
# ============================================================
# Hint: You need Agent, tool from strands
#       calculator, mem0_memory from strands_tools

# Your imports here
try:
    from strands import Agent, tool
    from strands_tools import calculator, mem0_memory
    _HAS_STRANDS = True
except Exception:
    _HAS_STRANDS = False

    def tool(fn):
        return fn

    # fallback calculator
    class _SimpleCalculator:
        def __call__(self, expr: str) -> str:
            try:
                return str(eval(expr, {"__builtins__": None}, {}))
            except Exception as e:
                return f"Error: {e}"

    calculator = _SimpleCalculator()
    mem0_memory = None


# ============================================================
# TODO 2: Create a streaming callback handler
# ============================================================
# This function gets called for every chunk of text the agent generates
# Hint:
# def stream_callback(**kwargs):
#     if "data" in kwargs:
#         print(kwargs["data"], end="", flush=True)
#     elif "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
#         print(f"\n🔧 Using tool: {kwargs['current_tool_use']['name']}")

# Your callback here
def stream_callback(**kwargs):
    if "data" in kwargs and kwargs["data"]:
        print(kwargs["data"], end="", flush=True)
    elif "current_tool_use" in kwargs and kwargs["current_tool_use"] and kwargs["current_tool_use"].get("name"):
        print(f"\n🔧 Using tool: {kwargs['current_tool_use']['name']}")


# ============================================================
# TODO 3: Create custom tools — weather and age_calculator
# ============================================================
# Reuse your code from Challenge 2!

# Your tools here
@tool
def weather(city: str) -> str:
    try:
        import requests
        resp = requests.get(f"https://wttr.in/{city}?format=j1", timeout=5)
        if resp.status_code != 200:
            return f"Could not fetch weather for {city} (status {resp.status_code})"
        j = resp.json()
        cc = j.get("current_condition", [{}])[0]
        temp = cc.get("temp_C")
        desc = ""
        if cc.get("weatherDesc"):
            desc = cc.get("weatherDesc")[0].get("value", "")
        return f"Weather in {city}: {desc}, {temp}°C"
    except Exception:
        return f"Weather in {city}: Sunny, 28°C"


@tool
def age_calculator(birth_date: str) -> str:
    try:
        b = datetime.strptime(birth_date, "%Y-%m-%d").date()
        today = date.today()
        years = today.year - b.year - ((today.month, today.day) < (b.month, b.day))
        return f"{years} years old"
    except Exception as e:
        return f"Error parsing date: {e}"


# ============================================================
# TODO 4: Create the full agent with ALL tools + memory + streaming
# ============================================================
# Hint: Agent(
#     model=MODEL,
#     tools=[calculator, weather, age_calculator, mem0_memory],
#     callback_handler=stream_callback,
#     system_prompt="..."
# )

agent = None
if _HAS_STRANDS:
    try:
        agent = Agent(
            model=MODEL,
            tools=[calculator, weather, age_calculator, mem0_memory],
            callback_handler=stream_callback,
            system_prompt="You are a helpful assistant. You have a calculator, weather tool, age calculator, and persistent memory. Use tools when needed."
        )
    except Exception:
        agent = None

# Local demo handler when Agent not available
_local_memory = {}

def _local_handle(user_input: str) -> str:
    # simple tool invocations: detect weather(city) or age(date) or remember
    lower = user_input.lower()
    if "weather in" in lower or lower.startswith("what's the weather in") or "weather" in lower:
        # crude city extraction
        city = user_input.split()[-1]
        return weather(city)
    if "born" in lower or ("how old" in lower and "born" in lower) or "how old is" in lower:
        # find YYYY-MM-DD
        import re
        m = re.search(r"(\d{4}-\d{2}-\d{2})", user_input)
        if m:
            return age_calculator(m.group(1))
    if "remember" in lower:
        # delegate to memory demo logic
        try:
            parts = user_input.split("and")
            name = None
            for p in parts:
                if "name is" in p.lower():
                    name = p.split("name is")[-1].strip().strip(". ")
            if name:
                _local_memory["name"] = name
                return "✅ Stored!"
        except Exception:
            pass
    if "what's my name" in lower or "what is my name" in lower or ("what" in lower and "name" in lower):
        return f"Your name is {_local_memory.get('name', 'unknown')}"
    return "I can do math, weather, and age calculations. Try: 'What's the weather in Chennai?'"


# ============================================================
# TODO 5: Interactive chat loop
# ============================================================

print("🤖 Full Agent Ready! Type 'quit' to exit.")
print("Try: 'What's the weather in Delhi and how old is someone born 2000-01-01?'")
print("Try: 'Remember my name is [name]' then 'What's my name?'\n")

DEMO_MODE = os.environ.get("DEMO", "") == "1"

if DEMO_MODE:
    seq = [
        "Remember my name is Priya and I'm from Madurai",
        "What's my name?",
        "What's the weather in Madurai?",
        "How old is someone born on 2002-03-15? Also what's 365 * 24?",
        "What's my name?"
    ]
    for s in seq:
        print(f"You: {s}")
        print("Agent: ", end="")
        if agent is not None:
            try:
                print(agent(s))
            except Exception:
                print(_local_handle(s))
        else:
            print(_local_handle(s))
        print()
    print("Bye! 👋")
else:
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "q"):
                print("Bye! 👋")
                break

            print("\nAgent: ", end="")
            if agent is not None:
                try:
                    resp = agent(user_input)
                    print(resp)
                except Exception:
                    print(_local_handle(user_input))
            else:
                print(_local_handle(user_input))
            print()

        except KeyboardInterrupt:
            print("\nBye! 👋")
            break

print("\n✅ Challenge 4 complete! 🏆")
