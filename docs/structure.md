# Project Structure

## Root
- `.gitignore`: Git ignore rules.
- `pyproject.toml`: Project metadata and build configuration.
- `LICENSE`: MIT license for the project.
- `README.md`: Project overview, installation, and usage instructions.
- `aurora.egg-info/`: Packaging metadata generated during build/distribution.
- `aurora/`: Main source code package.
- `docs/`: Project documentation.

## `aurora/`
- `__init__.py`: Package marker.
- `__main__.py`: Command-line interface for running the agent, handling arguments, API key, and output.
- `prompts/`: Contains prompt templates or system instructions.
- `agent/`: Core agent logic and tools.

## `aurora/agent/`
- `__init__.py`: Package marker.
- `agent.py`: Defines the main `Agent` class.
- `conversation.py`: Conversation management, including error classes.
- `tool_handler.py`: Tool registration and dispatch.
- `tools/`: Built-in tool implementations.

## `aurora/agent/tools/`
- `__init__.py`: Imports all tool functions for easy access.
- `ask_user.py`: Tool to interactively ask the user questions.
- `create_directory.py`: Tool to create directories.
- `create_file.py`: Tool to create files.
- `remove_file.py`: Tool to delete files.
- `replace_file.py`: Tool to replace file contents.
- `view_file.py`: Tool to view file contents or list directory contents.
- `find_files.py`: Tool to recursively search for files matching a pattern.
- `search_text.py`: Tool to search for a regex pattern inside files matching a glob pattern.
- `bash_exec.py`: Tool to execute Bash commands in a separate thread, returning a formatted message string with stdout, stderr, and return code.
