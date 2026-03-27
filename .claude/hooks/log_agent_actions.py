import json
import sys
import os
from typing import List, Dict, Any
from datetime import datetime


'''
Save log files when CARD*CURATE is run.
From: https://github.com/kenneth-liao/claude-agent-sdk-intro/tree/main
I added the User Query so we can see that in the log file.
'''


def parse_agent_actions(filepath: str) -> List[Dict[str, Any]]:
    """
    Parse a JSONL transcript file and extract all agent tool calls.

    Returns a list of dictionaries containing:
    - timestamp: when the action occurred
    - tool_name: name of the tool that was called
    - tool_input: arguments passed to the tool
    - tool_use_id: unique identifier for the tool use
    """
    
    events = []
    with open(filepath, 'r') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                timestamp = entry.get("timestamp", "")
                
                # Retrieve user query
                if entry.get('type') == 'user':
                    message = entry.get("message", {})
                    content = message.get("content", "")

                    # Skip if content is a list/dict containing tool_use_id (tool result)
                    if isinstance(content, list):
                        # Often tool results come as a list of dicts
                        if any(isinstance(item, dict) and 'tool_use_id' in item for item in content):
                            continue

                    elif isinstance(content, dict) and 'tool_use_id' in content:
                        continue
                    
                    events.append({
                        "event_type": "query",
                        "timestamp": timestamp,
                        "content": content
                    })
                
                # Retrieve assistant message
                if entry.get('type') == 'assistant':
                    message = entry.get('message', {})
                    content = message.get('content', [])
                    timestamp = entry.get('timestamp', '')

                    # Look for tool_use in content
                    for item in content:
                        if isinstance(item, dict) and item.get('type') == 'tool_use':
                            action = {
                                "event_type": "tool",
                                'timestamp': timestamp,
                                'tool_name': item.get('name'),
                                'tool_input': item.get('input'),
                                'tool_use_id': item.get('id')
                            }
                            events.append(action)

            except json.JSONDecodeError:
                # Skip malformed lines
                continue

    return events


def get_logged_tool_ids(log_filepath: str) -> set:
    """
    Read existing log file and extract all tool IDs that have been logged.

    Args:
        log_filepath: Path to the log file

    Returns:
        Set of tool IDs that have already been logged
    """
    logged_ids = set()

    if not os.path.exists(log_filepath):
        return logged_ids

    with open(log_filepath, 'r') as f:
        for line in f:
            # Look for lines with "Tool ID: "
            if line.strip().startswith("Tool ID:"):
                tool_id = line.split("Tool ID:")[1].strip()
                logged_ids.add(tool_id)

    return logged_ids


def save_agent_log(events: List[Dict[str, Any]], session_id: str, logs_dir="logs"):

    os.makedirs(logs_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filepath = os.path.join(logs_dir, f"{session_id}.log")

    with open(log_filepath, "w") as f: 
        f.write(f"{'='*80}\n")
        f.write(f"Agent Session Log - {session_id}\n")
        f.write(f"{'='*80}\n\n")

        for event in events:
            if event["event_type"] == "query":
                # Skip queries that are tool results
                content = event.get("content", "")
                if isinstance(content, list) and any(isinstance(item, dict) and 'tool_use_id' in item for item in content):
                    continue
                if isinstance(content, dict) and 'tool_use_id' in content:
                    continue

                f.write("User Query:\n")
                f.write(f"  Timestamp: {event['timestamp']}\n")
                f.write(f"  Text: {content}\n\n")

            elif event["event_type"] == "tool":
                f.write("Tool Use:\n")
                f.write(f"  Timestamp: {event['timestamp']}\n")
                f.write(f"  Tool: {event['tool_name']}\n")
                f.write(f"  Tool ID: {event['tool_use_id']}\n")
                f.write(f"  Input: {json.dumps(event['tool_input'], indent=4)}\n\n")

    return log_filepath


if __name__ == "__main__":
    try:
        payload: dict = json.load(sys.stdin)
        transcript_path = payload.get('transcript_path', '')
        session_id = payload.get('session_id', 'unknown_session')

        if not transcript_path:
            raise ValueError("No transcript path provided")

        # Parse agent actions and save to log file (append mode, no duplicates)
        events = parse_agent_actions(transcript_path)
        log_filepath, new_actions_count = save_agent_log(events, session_id)


    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)