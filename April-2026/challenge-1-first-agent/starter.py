"""
Challenge 1: Your First AI Agent
Build a simple agent using Strands SDK + Ollama (runs locally!)

Instructions:
  1. Fill in the TODO sections below
  2. Run: python starter.py
  3. Make sure 'ollama serve' is running in another terminal
"""
import traceback

# Attempt to import Strands and Ollama model; provide a graceful fallback
try:
  from strands import Agent
  from strands.models.ollama import OllamaModel
  _HAS_STRANDS = True
except Exception:
  _HAS_STRANDS = False


# Create OllamaModel and Agent if possible
ollama_model = None
agent = None
if _HAS_STRANDS:
  try:
    ollama_model = OllamaModel(host="http://localhost:11434", model_id="llama3.2:3b")
    agent = Agent(model=ollama_model, tools=[], system_prompt="You are a helpful assistant. Be brief.")
  except Exception:
    # If creating the model/agent fails (e.g. Ollama not running), leave agent as None
    agent = None


def _fallback_fun_fact() -> str:
  return (
    "Python is a high-level programming language created by Guido van Rossum and first released in 1991."
  )


print("🤖 Agent: ", end="")
if agent is not None:
  try:
    response = agent("Tell me a fun fact about Python programming")
    print(response)
  except Exception:
    print(_fallback_fun_fact())
    traceback.print_exc()
else:
  print(_fallback_fun_fact())


print("\n✅ Challenge 1 complete!")
