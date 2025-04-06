import os
from aurora.agent.tool_handler import ToolHandler

@ToolHandler.register_tool
def view_file(path: str, start_line: int = 1, max_lines: int = 100) -> str:
    """
    View the contents of a file or list the contents of a directory.

    path: The path of the file or directory to view
    start_line: The starting line number (1-based) for file content (default: 1)
    max_lines: Maximum number of lines to return from the file content (default: 100)
    """
    print(f"📂 Viewing file or directory: '{path}', start line {start_line}, max lines {max_lines} ... ", end="")
    try:
        if os.path.isdir(path):
            files = os.listdir(path)
            print(f"Success (listed {len(files)} items)")
            return "\n".join(files)
        else:
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                total_lines = len(lines)

                # Adjust start line
                s = start_line - 1 if start_line and start_line > 0 else 0

                # Slice selected range based on max_lines
                e = s + max_lines if max_lines is not None and max_lines > 0 else total_lines
                e = min(e, total_lines)

                selected = lines[s:e]

                # Prefix each line with its original line number
                numbered = [
                    f"{s + idx + 1}: {line}" for idx, line in enumerate(selected)
                ]
                
                # Determine last line number included
                last_line_included = s + len(selected)

                print(f"Success (read {len(selected)} of total {total_lines} lines)")

                result = "".join(numbered)

                if last_line_included < total_lines:
                    result += "\n... Output truncated. Use 'start_line' and 'max_lines' to view more."

                return result
    except Exception as e:
        print(f"Error: {e}")
        return f"Failed to view '{path}': {e}"
