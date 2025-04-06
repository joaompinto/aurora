import os
from aurora.agent.tool_handler import ToolHandler

@ToolHandler.register_tool
def replace_file(path: str, content: str) -> str:
    """
    Replace the content of an existing file.

    path: The path of the file to replace
    content: The new content to write into the file
    """
    print(f"✏️ Replacing file content: '{path}' ... ", end="")
    try:
        if os.path.isdir(path):
            print("Error: is a directory")
            return f"Cannot replace content: '{path}' is a directory."

        if not os.path.isfile(path):
            print("Error: does not exist")
            return f"Cannot replace content: The file '{path}' does not exist."

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Success")
        return f"Successfully replaced the content of the file at '{path}'."
    except Exception as e:
        print(f"Error: {e}")
        return f"Failed to replace the content of the file at '{path}': {e}"
