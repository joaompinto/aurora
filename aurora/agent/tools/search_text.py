import os
import re
import fnmatch


def search_text(directory: str, file_pattern: str, text_pattern: str, case_sensitive: bool = False, max_matches: int = 1000):
    """
    directory: Root directory to search.
    file_pattern: Glob pattern for filenames (e.g., '*.py').
    text_pattern: Regex pattern to search within files.
    case_sensitive: Whether the search is case sensitive.
    max_matches: Maximum number of matches to return.

    Returns a list of matches in 'filepath:line_number:matched_line' format.
    """
    flags = 0 if case_sensitive else re.IGNORECASE
    regex = re.compile(text_pattern, flags)
    results = []

    for root, _, files in os.walk(directory):
        for filename in fnmatch.filter(files, file_pattern):
            filepath = os.path.join(root, filename)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    for lineno, line in enumerate(f, start=1):
                        if regex.search(line):
                            results.append(f"{filepath}:{lineno}:{line.rstrip()}")
                            if len(results) >= max_matches:
                                return results
            except Exception:
                continue  # Ignore unreadable files

    return results
