import argparse


def create_parser():
    parser = argparse.ArgumentParser(description="OpenRouter API call using OpenAI Python SDK")
    parser.add_argument("prompt", type=str, nargs="?", help="Prompt to send to the model")
    parser.add_argument("-s", "--system-prompt", type=str, default=None, help="Optional system prompt")
    parser.add_argument("-r", "--role", type=str, default=None, help="Role description for the system prompt")
    parser.add_argument("--verbose-http", action="store_true", help="Enable verbose HTTP logging")
    parser.add_argument("--verbose-http-raw", action="store_true", help="Enable raw HTTP wire-level logging")
    parser.add_argument("--verbose-response", action="store_true", help="Pretty print the full response object")
    parser.add_argument("--show-system", action="store_true", help="Show model, parameters, system prompt, and tool definitions, then exit")
    parser.add_argument("--verbose-tools", action="store_true", help="Print tool call parameters and results")
    parser.add_argument("--set-local-config", type=str, default=None, help='Set a local config key-value pair, format "key=val"')
    parser.add_argument("--set-global-config", type=str, default=None, help='Set a global config key-value pair, format "key=val"')
    parser.add_argument("--show-config", action="store_true", help="Show effective configuration and exit")
    parser.add_argument("--version", action="store_true", help="Show program's version number and exit")
    parser.add_argument("--continue-session", action="store_true", help="Continue from the last saved conversation")
    return parser
