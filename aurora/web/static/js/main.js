import { createContentModal, showContentPopup, showPopup } from "./modal.js";
import { setupTerminal } from "./terminal.js";
import { sendCommandStream } from "./stream.js";
import { handleToolProgress } from "./toolProgress.js";
import { setupSessionControls } from "../js/sessionControl.js";

window.contentStore = [];
window.showContentPopup = showContentPopup;
window.showPopup = showPopup;

document.addEventListener("DOMContentLoaded", async function() {
  setupSessionControls();
  createContentModal();

  // Auto-load last conversation
  try {
    const response = await fetch('/load_conversation');
    const data = await response.json();
    if(data.status === 'ok' && Array.isArray(data.conversation)) {
      data.conversation.forEach(msg => {
        if(msg.role === 'user') {
          terminalApi.appendOutput('**You:** ' + msg.content);
        } else if(msg.role === 'assistant') {
          terminalApi.appendOutput('**Assistant:** ' + msg.content);
        }
      });
    }
  } catch(err) {
    console.error('Error loading conversation:', err);
  }

  const terminalApi = setupTerminal(async (command) => {
    const trimmed = command.trim();
    if(trimmed.startsWith('/')) {
      if(trimmed === '/continue') {
        try {
          const response = await fetch('/load_conversation');
          const data = await response.json();
          if(data.status === 'ok' && Array.isArray(data.conversation)) {
            data.conversation.forEach(msg => {
              if(msg.role === 'user') {
                terminalApi.appendOutput('**You:** ' + msg.content);
              } else if(msg.role === 'assistant') {
                terminalApi.appendOutput('**Assistant:** ' + msg.content);
              }
            });
          } else {
            terminalApi.appendOutput('No previous conversation found.');
          }
        } catch(err) {
          terminalApi.appendOutput('Error loading conversation: ' + err);
        }
      } else if(trimmed === '/help') {
        terminalApi.appendOutput(`Available commands:\n/continue - Load the last conversation\n/help - Show this help message`);
      } else {
        terminalApi.appendOutput('Unknown command: ' + trimmed);
      }
      return;
    }

    await sendCommandStream(command, (data) => {
      if(data.type === "content" && data.content) {
        terminalApi.appendOutput(data.content);
      } else if(data.type === "tool_progress") {
        handleToolProgress(data.data, document.getElementById("terminal"));
      } else if(data.type === "error") {
        terminalApi.appendOutput("Error: " + data.error);
      }
    });
  });
});
