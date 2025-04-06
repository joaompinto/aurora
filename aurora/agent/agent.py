import os
import json
from openai import OpenAI
from aurora.agent.conversation import ConversationHandler
from aurora.agent.tool_handler import ToolHandler

import aurora.agent.tools.view_file
import aurora.agent.tools.remove_file
import aurora.agent.tools.create_file
import aurora.agent.tools.replace_file
import aurora.agent.tools.ask_user
import aurora.agent.tools.create_directory
import aurora.agent.tools.search_text

class Agent:
    def __init__(self, api_key: str, model: str = "openrouter/quasar-alpha", system_prompt: str | None = None):
        self.api_key = api_key
        self.model = model
        self.system_prompt = system_prompt
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.tool_handler = ToolHandler()
        self.conversation_handler = ConversationHandler(
            self.client, self.model, self.tool_handler
        )

    def chat(self, messages, on_content=None, verbose_response=False):
        return self.conversation_handler.handle_conversation(messages, on_content=on_content, verbose_response=verbose_response)