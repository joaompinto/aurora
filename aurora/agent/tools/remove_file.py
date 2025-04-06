import os
from aurora.agent.tool_handler import ToolHandler

@ToolHandler.register_tool
def remove_file(path: str) -> str:
    """
    Remove a specified file.

    path: The path of the file to remove
    """
    print(f"🗑️ Removing file: '{path}' ... ", end="")
    try:
        os.remove(path)
        print("Success")
        return f"Successfully deleted the file at '{path}'."
    except Exception as e:
        print(f"Error: {e}")
        return f"Failed to delete the file at '{path}': {e}"
