# Example: OpenRouter API call using OpenAI Python SDK >=1.0.0
# Make sure to install the OpenAI package:
# pip install --upgrade openai
#
# Before running, set your API key as an environment variable:
# export OPENROUTER_API_KEY='your-api-key'   (Linux/macOS)
# set OPENROUTER_API_KEY=your-api-key       (Windows CMD)
# $env:OPENROUTER_API_KEY="your-api-key"    (PowerShell)
#
# Usage:
# python -m aurora "Your prompt here"

import os
import sys
import importlib.resources

try:
    with importlib.resources.files("aurora.prompts").joinpath("system_instructions.txt").open("r", encoding="utf-8") as f:
        system_prompt = f.read()
except (FileNotFoundError, ModuleNotFoundError, AttributeError):
    print("[Error] Could not find 'aurora/prompts/system_instructions.txt'. Please ensure it exists.")
    sys.exit(1)
from aurora.agent.conversation import MaxRoundsExceededError
from rich.console import Console
from rich.markdown import Markdown
import argparse
import logging
from aurora.agent.agent import Agent

parser = argparse.ArgumentParser(description="OpenRouter API call using OpenAI Python SDK")
parser.add_argument("prompt", type=str, nargs="?", help="Prompt to send to the model")
parser.add_argument("-s", "--system-prompt", type=str, default=None, help="Optional system prompt")
parser.add_argument("--verbose-http", action="store_true", help="Enable verbose HTTP logging")
parser.add_argument("--verbose-http-raw", action="store_true", help="Enable raw HTTP wire-level logging")
parser.add_argument("--verbose-response", action="store_true", help="Pretty print the full response object")
parser.add_argument("--show-system", action="store_true", help="Show model, parameters, system prompt, and tool definitions, then exit")
args = parser.parse_args()

if args.show_system:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("Please set the OPENROUTER_API_KEY environment variable.")

    agent = Agent(api_key=api_key)
    print("Model:", agent.model)
    # Placeholder for model parameters (none explicitly stored)
    print("Parameters: {}")
    # System prompt: user-supplied or default
    system_prompt = args.system_prompt or "(default system prompt not provided)"
    print("System Prompt:", system_prompt)
    # Tool definitions
    print("Tool Definitions:")
    import json as _json
    print(_json.dumps(agent.tool_handler.tools, indent=2))
    sys.exit(0)

if args.verbose_http or args.verbose_http_raw:
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    httpx_logger.addHandler(handler)

if args.verbose_http_raw:
    # Set environment variable to increase HTTPX verbosity
    os.environ["HTTPX_LOG_LEVEL"] = "trace"

    httpcore_logger = logging.getLogger("httpcore")
    httpcore_logger.setLevel(logging.DEBUG)
    handler_core = logging.StreamHandler()
    handler_core.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    httpcore_logger.addHandler(handler_core)

    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    httpx_logger.addHandler(handler)

if not args.prompt:
    print("Error: You must provide a prompt unless using --show-system.")
    sys.exit(1)

prompt = args.prompt

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENROUTER_API_KEY environment variable.")

agent = Agent(api_key=api_key, system_prompt=system_prompt)

console = Console()

def on_content(content):
    console.print(Markdown(content))

messages = []
if agent.system_prompt:
    messages.append({
        "role": "system",
        "content": agent.system_prompt
    })
messages.append({
    "role": "user",
    "content": prompt
})

try:
    response = agent.run(messages, on_content=on_content, verbose_response=args.verbose_response)
except MaxRoundsExceededError as e:
    print(f"[Error] {e}")
