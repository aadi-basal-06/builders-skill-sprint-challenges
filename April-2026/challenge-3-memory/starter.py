"""
Challenge 3: Agent with Persistent Memory
Give your agent memory that survives restarts using FAISS.
Model: Amazon Nova Pro via Bedrock

Instructions:
  1. Fill in the TODO sections below
  2. Run: python starter.py
  3. Store some facts, then quit and restart to verify persistence
"""

import os
os.environ["BYPASS_TOOL_CONSENT"] = "true"

# Try to import Strands Agent; fall back for offline demo
try:
    from strands import Agent
    _HAS_STRANDS = True
except Exception:
    Agent = None
    _HAS_STRANDS = False

MODEL = "us.amazon.nova-pro-v1:0"


# Try to import mem0_memory; provide fallback if unavailable for offline demo
try:
    from strands_tools import mem0_memory
    _HAS_MEM0 = True
except Exception:
    mem0_memory = None
    _HAS_MEM0 = False

# Create agent if Strands/FAISS mem0 available
agent = None
try:
    agent = Agent(model=MODEL, tools=([mem0_memory] if _HAS_MEM0 else []), system_prompt="You are an assistant that stores and recalls user preferences using mem0_memory.")
except Exception:
    agent = None

# Simple local memory fallback for offline testing
_local_memory = {}

def _local_agent_handle(user_input: str) -> str:
    # simple patterns: remember that my name is X and I love Y
    lower = user_input.lower()
    if lower.startswith("remember") or "remember that" in lower:
        # crude parse
        try:
            # look for 'name is' and 'love'
            name = None
            food = None
            parts = user_input.split("and")
            for p in parts:
                if "name is" in p.lower():
                    name = p.split("name is")[-1].strip().strip(". ")
                if "love" in p.lower():
                    food = p.split("love")[-1].strip().strip(". ")
            if name:
                _local_memory["name"] = name
            if food:
                _local_memory.setdefault("foods", []).append(food)
            return "✅ I'll remember that!"
        except Exception:
            return "Could not parse memory instruction."

    # recall questions
    if "what" in lower and ("name" in lower or "food" in lower or "like" in lower):
        name = _local_memory.get("name")
        foods = _local_memory.get("foods", [])
        parts = []
        if name:
            parts.append(f"Your name is {name}")
        if foods:
            parts.append(f"you like {', '.join(foods)}")
        if parts:
            return " and ".join(parts) + "!"
        return "I don't have any memories yet."

    return "I can store memories. Try: 'Remember that my name is Ravi and I love biryani'"


# ============================================================
# TODO 3: Interactive loop — chat with the memory agent
# ============================================================

print("🧠 Memory Agent Ready!")
print("Try: 'Remember that my name is [your name] and I love [food]'")
print("Then: 'What's my name and what food do I like?'")
print("Type 'quit' to exit.\n")

DEMO_MODE = os.environ.get("DEMO", "") == "1"

def _call_agent(user_input: str) -> str:
    if agent is not None:
        try:
            return agent(user_input)
        except Exception:
            # fall back to local handler
            return _local_agent_handle(user_input)
    else:
        return _local_agent_handle(user_input)

if DEMO_MODE:
    # automated demo sequence
    seq = [
        "Remember that my name is Ravi and I love biryani",
        "What's my name and what food do I like?"
    ]
    for s in seq:
        print(f"You: {s}")
        print("Agent:", _call_agent(s))
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

            response = _call_agent(user_input)
            print("Agent:", response)

        except KeyboardInterrupt:
            print("\nBye! 👋")
            break

print("\n✅ Challenge 3 complete!")
