# Aurora AI Command Line Agent (for openrouter/quasar-alpha)
# ==========================

Aurorsa is command line agent for natural language coding using the `openrouter/quasar-alpha` model

## Features
- **Command-Line Interface:** Run the agent with configurable arguments and API keys.
- **Modular Agent Core:** Handles conversation management, tool dispatch, and agent logic.
- **Built-in Tools:** File management, directory operations, user interaction, and search utilities.
- **Extensible Design:** Easily add new tools or customize prompts.

## Command-Line Options
- `prompt` (positional): The prompt to send to the model (optional if using `--show-system`).
- `-s`, `--system-prompt`: Provide an optional system prompt.
- `--verbose-http`: Enable verbose HTTP logging.
- `--verbose-http-raw`: Enable raw HTTP wire-level logging.
- `--verbose-response`: Pretty print the full response object.
- `--show-system`: Show model, parameters, system prompt, and tool definitions, then exit.

## Getting Started
1. **Install dependencies:**
   ```bash
   pip install -e .
   ```
2. **Set your API key as an environment variable:**
   ```bash
   export OPENROUTER_API_KEY=YOUR_API_KEY
   ```
3. **Run the agent:**
   ```bash
   python -m aurora "Your prompt here"
   ```

## License
Specify your license here.

## Contributing
Pull requests and issues are welcome!
