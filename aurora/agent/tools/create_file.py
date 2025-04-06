import os
from aurora.agent.tool_handler import ToolHandler

@ToolHandler.register_tool
def create_file(path: str, content: str) -> str:
    """
    Create or overwrite a file with the specified content.

    path: The path of the file to create
    content: The content to write into the file
    """
    print(f"📝 Creating file: '{path}' ... ", end="")
    try:
        if os.path.isdir(path):
            print("Error: is a directory")
            return f"Cannot create file: '{path}' is an existing directory."

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Success")
        return f"Successfully created or overwritten the file at '{path}'."
    except Exception as e:
        print(f"Error: {e}")
        return f"Failed to create or overwrite the file at '{path}': {e}"
