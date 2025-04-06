import os
import fnmatch
from aurora.agent.tool_handler import ToolHandler
from aurora.agent.tools.rich_utils import print_info, print_success, print_error, format_path, format_number

@ToolHandler.register_tool
def find_files(directory: str, pattern: str = "*") -> str:
    """
    Recursively find files matching a pattern within a directory.

    directory: The root directory to start searching from.
    pattern: Glob pattern to match filenames (default: '*').
    """
    print_info(f"🔍 Searching for files in '{format_path(directory)}' matching pattern '{pattern}' ... ")
    matches = []
    try:
        for root, dirs, files in os.walk(directory):
            for filename in fnmatch.filter(files, pattern):
                matches.append(os.path.join(root, filename))
        print_success(f"✅ Found {format_number(len(matches))} files")
        if matches:
            return "\n".join(matches)
        else:
            return "No matching files found."
    except Exception as e:
        print_error(f"❌ Error: {e}")
        return f"❌ Failed to search files in '{directory}': {e}"
