from aurora.agent.tool_handler import ToolHandler
from aurora.agent.tools.rich_utils import print_info, print_success, print_error
import subprocess
import threading


@ToolHandler.register_tool
def bash_exec(command: str) -> str:
    """
    command: The Bash command to execute.

    Execute a non interactive bash command and wait for it to finish.

    Returns:
    str: A formatted message string containing stdout, stderr, and return code.
    """
    print_info(f"[bash_exec] Executing command: {command}")
    result = {'stdout': '', 'stderr': '', 'returncode': None}

    def run_command():
        try:
            completed = subprocess.run(
                command, shell=True, capture_output=True, text=True
            )
            result['stdout'] = completed.stdout
            result['stderr'] = completed.stderr
            result['returncode'] = completed.returncode
        except Exception as e:
            result['stderr'] = str(e)
            result['returncode'] = -1

    thread = threading.Thread(target=run_command)
    thread.start()
    thread.join()  # Wait for the thread to finish

    print_success(f"[bash_exec] Command execution completed.")
    print_info(f"[bash_exec] Return code: {result['returncode']}")
    if result['stdout']:
        print_success(f"[bash_exec] Standard Output:\n{result['stdout']}")
    if result['stderr']:
        print_error(f"[bash_exec] Standard Error:\n{result['stderr']}")

    return f"stdout:\n{result['stdout']}\nstderr:\n{result['stderr']}\nreturncode: {result['returncode']}"