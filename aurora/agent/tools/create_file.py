import os
from aurora.agent.tool_handler import ToolHandler
from aurora.agent.tools.rich_utils import print_info, print_success, print_error, format_path

@ToolHandler.register_tool
def create_file(path: str, content: str) -> str:
    """
    Create or overwrite a file with the specified content.

    path: The path of the file to create
    content: The content to write into the file
    """
    print_info(f"📝 Creating file: '{format_path(path)}' ... ")
    try:
        if os.path.isdir(path):
            print_error("❌ Error: is a directory")
            return f"❌ Cannot create file: '{path}' is an existing directory."

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print_success("✅ Success")
        return f"✅ Successfully created or overwritten the file at '{path}'."
    except Exception as e:
        print_error(f"❌ Error: {e}")
        return f"❌ Failed to create or overwrite the file at '{path}': {e}"
