import os
import sys
from aurora.render_prompt import render_system_prompt


def handle_exit(console, **kwargs):
    console.print("[bold red]Exiting chat mode.[/bold red]")
    sys.exit(0)


def handle_restart(console, **kwargs):
    console.print("[bold yellow]Restarting CLI...[/bold yellow]")
    os.execv(sys.executable, [sys.executable, "-m", "aurora"] + sys.argv[1:])


def handle_paste(console, **kwargs):
    console.print("[bold cyan]Paste your content below. Press Ctrl+D (Unix) or Ctrl+Z (Windows) then Enter to finish.[/bold cyan]")
    pasted_lines = []
    try:
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            pasted_lines.append(line.rstrip('\n'))
    except EOFError:
        pass
    return "\n".join(pasted_lines).strip()


def handle_continue(console, state, **kwargs):
    import json, os
    save_path = os.path.join('.aurora', 'last_conversation.json')
    if not os.path.exists(save_path):
        console.print('[bold red]No saved conversation found.[/bold red]')
        return
    try:
        with open(save_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        state['messages'].clear()
        state['messages'].extend(data.get('messages', []))
        state['history_list'].clear()
        state['history_list'].extend(data.get('prompts', []))
        state['mem_history'].clear()
        for item in state['history_list']:
            state['mem_history'].append_string(item)
        console.print('[bold green]Conversation restored from last session.[/bold green]')
    except Exception as e:
        console.print(f'[bold red]Failed to load conversation:[/bold red] {e}')

def handle_help(console, **kwargs):
    console.print("""
[bold green]Available commands:[/bold green]
  /exit     - Exit chat mode
  /restart  - Restart the CLI
  /paste    - Paste multiline input
  /help     - Show this help message
  /continue - Restore last saved conversation
  /system   - Show the system prompt
""")


def handle_system(console, **kwargs):
    prompt = render_system_prompt("software engineer")
    console.print(f"[bold magenta]System Prompt:[/bold magenta]\n{prompt}")


COMMAND_HANDLERS = {
    "/continue": handle_continue,
    "/exit": handle_exit,
    "/restart": handle_restart,
    "/paste": handle_paste,
    "/help": handle_help,
    "/system": handle_system,
}


def handle_command(command, console, **kwargs):
    handler = COMMAND_HANDLERS.get(command)
    if handler:
        return handler(console=console, **kwargs)
    return None
