from flask import Flask, render_template, request, jsonify, make_response, Response
import os
import json
import uuid
from aurora.agent.agent import Agent

app = Flask(__name__)

# Initialize Aurora agent
api_key = os.getenv('OPENROUTER_API_KEY')
if not api_key:
    raise RuntimeError('OPENROUTER_API_KEY environment variable not set')

agent = Agent(api_key=api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    try:
        data = request.get_json()
        command = data.get('command', '').strip()
        if not command:
            return jsonify({'output': 'Error: No command provided'}), 400

        messages = []
        if agent.system_prompt:
            messages.append({"role": "system", "content": agent.system_prompt})
        messages.append({"role": "user", "content": command})

        result = agent.chat(messages)
        return jsonify({'output': result})
    except Exception as e:
        print(f"Error during execution: {e}")
        return jsonify({'output': f"Error: {str(e)}"}), 500

@app.route('/execute_stream', methods=['POST'])
def execute_stream():
    try:
        data = request.get_json()
        command = data.get('command', '').strip()
        if not command:
            return jsonify({'error': 'No command provided'}), 400

        command_id = str(uuid.uuid4())

        messages = []
        if agent.system_prompt:
            messages.append({"role": "system", "content": agent.system_prompt})
        messages.append({"role": "user", "content": command})

        def generate():
            try:
                buffer = []
                tool_events = []

                def on_content(content):
                    payload = json.dumps({
                        'command_id': command_id,
                        'type': 'content',
                        'content': content
                    })
                    buffer.append(f"data: {payload}\n\n")

                def on_tool_progress(progress_data):
                    payload = json.dumps({
                        'command_id': command_id,
                        'type': 'tool_progress',
                        'progress': progress_data
                    })
                    tool_events.append(f"data: {payload}\n\n")

                # patch tool handler to pass on_progress
                agent.tool_handler.handle_tool_call = (lambda orig_func=agent.tool_handler.handle_tool_call:
                    lambda tool_call, **kwargs: orig_func(tool_call, on_progress=on_tool_progress, **kwargs))()

                agent.chat(messages, on_content=on_content)

                # yield content events
                for event in buffer:
                    yield event
                # yield tool progress events
                for event in tool_events:
                    yield event

            except Exception as e:
                error_payload = json.dumps({'command_id': command_id, 'error': str(e)})
                yield f"data: {error_payload}\n\n"

        return Response(generate(), mimetype='text/event-stream')

    except Exception as e:
        print(f"Error during streaming execution: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/favicon.ico')
def favicon():
    return make_response('', 204)

if __name__ == '__main__':
    app.run(debug=True)
