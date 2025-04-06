from aurora.agent.tool_handler import ToolHandler

@ToolHandler.register_tool
def ask_user(question: str) -> str:
    """
    Ask the user a question and return their response.

    question: The question to ask the user
    """
    print(f"[ask_user] Question: {question}")
    response = input("> ")
    return response
