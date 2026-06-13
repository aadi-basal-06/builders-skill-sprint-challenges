"""
Challenge 2: Adding Tools to Your Agent
Give your agent a calculator, weather tool, and age calculator.
Model: Amazon Nova Pro via Bedrock

Instructions:
  1. Fill in the TODO sections below
  2. Run: python starter.py
  3. Needs AWS credentials configured (aws configure)
"""

import os
os.environ["BYPASS_TOOL_CONSENT"] = "true"

from datetime import date, datetime

# Import strands and tools with graceful fallbacks for offline testing
try:
  from strands import Agent, tool
  from strands_tools import calculator
  _HAS_STRANDS = True
except Exception:
  _HAS_STRANDS = False

  def tool(fn):
    return fn

  # Minimal calculator fallback (safe eval)
  class _SimpleCalculator:
    def __call__(self, expr: str) -> str:
      try:
        # very small sandbox for arithmetic expressions
        allowed_names = {}
        return str(eval(expr, {"__builtins__": None}, allowed_names))
      except Exception as e:
        return f"Error: {e}"

  calculator = _SimpleCalculator()

MODEL = "us.amazon.nova-pro-v1:0"


# ============================================================
# TODO 1: Create a custom weather tool
# ============================================================
# Hint: Use the @tool decorator
# The function should take a city name and return weather info
# Use wttr.in API: https://wttr.in/{city}?format=j1
# Or return dummy data: f"The weather in {city} is sunny, 28°C"

@tool
def weather(city: str) -> str:
  """Get the current weather for a city.
  Args:
    city: The name of the city.
  """
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
    return f"The weather in {city} is sunny, 28°C"


# ============================================================
# TODO 2: Create a custom age calculator tool
# ============================================================
# Hint: Use @tool decorator
# Take a birth_date string in YYYY-MM-DD format
# Calculate the age using datetime

@tool
def age_calculator(birth_date: str) -> str:
  """Calculate age from a birth date.
  Args:
    birth_date: Date of birth in YYYY-MM-DD format.
  """
  try:
    b = datetime.strptime(birth_date, "%Y-%m-%d").date()
    today = date.today()
    years = today.year - b.year - ((today.month, today.day) < (b.month, b.day))
    return f"{years} years old"
  except Exception as e:
    return f"Error parsing date: {e}"


# ============================================================
# TODO 3: Create an agent with all tools
# ============================================================
# Hint: Agent(model=MODEL, tools=[calculator, weather, age_calculator], ...)

agent = None
if _HAS_STRANDS:
  try:
    agent = Agent(model=MODEL, tools=[calculator, weather, age_calculator], system_prompt="You are an assistant with calculator and custom tools. Use tools when helpful.")
  except Exception:
    agent = None


# ============================================================
# TODO 4: Test the agent with different questions
# ============================================================

# Test math
print("🧮 Math test:")
if agent is not None:
  try:
    response = agent("What is 42 * 17?")
    print(response)
  except Exception:
    print("Agent math call failed; falling back to local calculator")
    print(calculator("42 * 17"))
else:
  print(calculator("42 * 17"))

# Test weather
print("\n🌤️ Weather test:")
if agent is not None:
  try:
    response = agent("What's the weather in Chennai?")
    print(response)
  except Exception:
    print("Agent weather call failed; falling back to local tool")
    print(weather("Chennai"))
else:
  print(weather("Chennai"))

# Test age
print("\n🎂 Age test:")
if agent is not None:
  try:
    response = agent("How old is someone born on 2000-05-15?")
    print(response)
  except Exception:
    print("Agent age call failed; falling back to local tool")
    print(age_calculator("2000-05-15"))
else:
  print(age_calculator("2000-05-15"))


print("\n✅ Challenge 2 complete!")
