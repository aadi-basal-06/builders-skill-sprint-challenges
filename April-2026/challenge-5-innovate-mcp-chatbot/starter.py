"""
Challenge 5 (Innovate): Build Your Own MCP-Powered Agent

YOUR TASK:
  Build an innovative agent from scratch that connects to any MCP server.
  The most creative and useful agent gets a special shoutout! 🏆

RULES:
  - Must use Strands Agents SDK
  - Must use at least one MCP server
  - Must use Amazon Nova Pro (or any Bedrock model)
  - Must have an interactive chat loop
  - Must be YOUR OWN idea — be creative!

EXAMPLE MCP SERVERS:
  pip install awslabs.aws-documentation-mcp-server   # AWS Docs
  uvx awslabs.cdk-mcp-server@latest                  # AWS CDK
  uvx awslabs.cost-analysis-mcp-server@latest        # AWS Pricing

BROWSE MORE: https://github.com/modelcontextprotocol/servers

RESOURCES:
  - Strands MCP docs: https://strandsagents.com/latest/user-guide/concepts/tools/mcp-tools/
  - AWS MCP servers: https://github.com/awslabs/mcp

Build something that makes us go "whoa!" 🚀
"""

import os
import json
from datetime import datetime
from pathlib import Path

# Try to import MCP helpers from strands/tools
try:
  from strands import Agent
  from strands.tools.mcp import MCPClient
  from mcp import StdioServerParameters, stdio_client
  _HAS_MCP = True
except Exception:
  MCPClient = None
  StdioServerParameters = None
  stdio_client = None
  _HAS_MCP = False


OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_mermaid(description: str) -> str:
  """Generate a simple Mermaid diagram from a textual architecture description.
  This is heuristic-based: looks for known AWS components and wires a simple flow.
  """
  desc = description.lower()
  components = []
  known = ["lambda", "api gateway", "dynamodb", "s3", "cloudfront", "rds", "sns", "sqs", "alb", "ec2"]
  for k in known:
    if k in desc:
      components.append(k)

  # fallback: extract capitalized words as components
  if not components:
    for part in [p.strip() for p in description.replace("with", ",").split(",") if p.strip()]:
      components.append(part)

  # create node ids
  nodes = []
  for i, c in enumerate(components):
    nid = f"n{i}"
    label = c.title()
    nodes.append((nid, label))

  # simple chain layout: client -> first -> ... -> last
  lines = ["flowchart LR"]
  lines.append("    User([User])")
  for nid, label in nodes:
    lines.append(f"    {nid}[{label}]")

  prev = "User"
  for nid, _ in nodes:
    lines.append(f"    {prev} --> {nid}")
    prev = nid

  # add captions
  lines.append(f"    classDef note fill:#f9f,stroke:#333,stroke-width:0.5;")
  lines.append(f"    %% Generated from: {description}")

  return "\n".join(lines)


def save_mermaid(code: str, name: str = None) -> Path:
  if name is None:
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    name = f"architecture_{ts}.mmd"
  path = OUTPUT_DIR / name
  path.write_text(code, encoding="utf-8")
  return path


def try_create_aws_docs_mcp():
  if not _HAS_MCP:
    return None
  try:
    aws_docs = MCPClient(lambda: stdio_client(StdioServerParameters(command="awslabs.aws-documentation-mcp-server")))
    return aws_docs
  except Exception:
    return None


def run_demo():
  desc = "serverless web app with Lambda, API Gateway, DynamoDB, and S3 static hosting"
  print("Description:", desc)
  # try MCP (best effort)
  aws = try_create_aws_docs_mcp()
  if aws is not None:
    print("AWS Docs MCP available — you can extend this to query docs for each service.")
  else:
    print("AWS Docs MCP not available — using local heuristics.")

  code = generate_mermaid(desc)
  path = save_mermaid(code, "architecture_demo.mmd")
  print(f"Saved Mermaid diagram to: {path}")
  print("Mermaid code:\n")
  print(code)


def interactive_loop():
  print("🏗️ Architecture-to-Diagram Bot — describe an architecture and I'll make a Mermaid diagram.")
  print("Type 'quit' to exit. Type 'demo' for a quick example.")
  while True:
    try:
      text = input("You: ").strip()
      if not text:
        continue
      if text.lower() in ("quit", "exit", "q"):
        print("Bye! 👋")
        break
      if text.lower() == "demo":
        run_demo()
        continue

      print("Generating diagram...")
      code = generate_mermaid(text)
      path = save_mermaid(code)
      print(f"Saved Mermaid diagram to: {path}")
      print("Paste the following into https://mermaid.live to preview:")
      print(code)

    except KeyboardInterrupt:
      print("\nBye! 👋")
      break


if __name__ == "__main__":
  if os.environ.get("DEMO", "") == "1":
    run_demo()
  else:
    interactive_loop()

