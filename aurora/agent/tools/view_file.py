import os
from aurora.agent.tool_handler import ToolHandler
from aurora.agent.tools.rich_utils import print_info, print_success, print_error, format_path, format_number

@ToolHandler.register_tool
def view_file(path: str, start_line: int = 1, max_lines: int = 100) -> str:
    """
    View the contents of a file or list the contents of a directory.

    path: The path of the file or directory to view
    start_line: The starting line number (1-based) for file content (default: 1)
    max_lines: Maximum number of lines to return from the file content (default: 100)
    """
    print_info(f"📂 Viewing path: '{format_path(path)}', start line {format_number(start_line)}, max lines {format_number(max_lines)} ... ")
    try:
        if os.path.isdir(path):
            files = os.listdir(path)
            print_success(f"✅ Success (listed {format_number(len(files))} items)")
            return "\n".join(files)
        else:
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                total_lines = len(lines)

                s = start_line - 1 if start_line and start_line > 0 else 0
                e = s + max_lines if max_lines is not None and max_lines > 0 else total_lines
                e = min(e, total_lines)

                selected = lines[s:e]

                numbered = [
                    f"{s + idx + 1}: {line}" for idx, line in enumerate(selected)
                ]

                last_line_included = s + len(selected)

                if last_line_included >= total_lines:
                    print_success(f"✅ Success (returning all {format_number(total_lines)} lines)")
                else:
                    print_success(f"✅ Success (returning {format_number(len(selected))} of total {format_number(total_lines)} lines)")

                result = "".join(numbered)

                if last_line_included < total_lines:
                    result += "\n... Output truncated. Use 'start_line' and 'max_lines' to view more."

                start_display = s + 1
                end_display = last_line_included
                summary = f"\nShowing lines {start_display} to {end_display} of {total_lines} total lines."
                if last_line_included < total_lines:
                    summary += " More lines available."
                result += summary

                return result
    except Exception as e:
        print_error(f"❌ Error: {e}")
        return f"❌ Failed to view '{path}': {e}"
