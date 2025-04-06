import os
import sys
import importlib.resources
import argparse
import logging
from rich.console import Console
from rich.markdown import Markdown
from aurora.agent.agent import Agent
from aurora.agent.conversation import MaxRoundsExceededError


def main():
    try:
        with importlib.resources.files("aurora.prompts").joinpath("system_instructions.txt").open("r", encoding="utf-8") as f:
            system_prompt = f.read()
    except (FileNotFoundError, ModuleNotFoundError, AttributeError):
        print("[Error] Could not find 'aurora/prompts/system_instructions.txt'. Please ensure it exists.")
        sys.exit(1)

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
        system_prompt_display = args.system_prompt or "(default system prompt not provided)"
        print("System Prompt:", system_prompt_display)
        # Tool definitions
        import json as _json
        print("Tool Definitions:")
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

    agent = Agent(api_key=api_key, system_prompt=(args.system_prompt or system_prompt))

    console = Console()

    def on_content(content):
        console.print(Markdown(content))

    messages = []
    if agent.system_prompt:
        messages.append({"role": "system", "content": agent.system_prompt})

    messages.append({"role": "user", "content": prompt})

    try:
        try:
            response = agent.chat(messages, on_content=on_content)
            if args.verbose_response:
                import json
                console.print_json(json.dumps(response))
        except MaxRoundsExceededError:
            print("[Error] Conversation exceeded maximum rounds.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n[Interrupted by user]")
        sys.exit(1)


if __name__ == "__main__":
    main()
