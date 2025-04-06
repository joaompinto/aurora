import os
from aurora.agent.tool_handler import ToolHandler
from aurora.agent.tools.rich_utils import print_info, print_success, print_error, format_path

@ToolHandler.register_tool
def replace_file(path: str, content: str) -> str:
    """
    Replace the content of an existing file.

    path: The path of the file to replace
    content: The new content to write into the file
    """
    print_info(f"✏️ Replacing file content: '{format_path(path)}' ... ")
    try:
        if os.path.isdir(path):
            print_error("❌ Error: is a directory")
            return f"❌ Cannot replace content: '{path}' is a directory."

        if not os.path.isfile(path):
            print_error("❌ Error: does not exist")
            return f"❌ Cannot replace content: The file '{path}' does not exist."

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print_success("✅ Success")
        return f"✅ Successfully replaced the content of the file at '{path}'."
    except Exception as e:
        print_error(f"❌ Error: {e}")
        return f"❌ Failed to replace the content of the file at '{path}': {e}"
