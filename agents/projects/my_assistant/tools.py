import os
import json
import requests
from typing import Dict, Any

# Load environment variables
PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
PUSHOVER_URL = "https://api.pushover.net/1/messages.json"

def push_notification(message: str) -> Dict[str, Any]:
    """Send push notification via Pushover"""
    print(f"Push: {message}")
    if PUSHOVER_USER and PUSHOVER_TOKEN:
        try:
            payload = {"user": PUSHOVER_USER, "token": PUSHOVER_TOKEN, "message": message}
            response = requests.post(PUSHOVER_URL, data=payload)
            return {"status": "sent", "response": response.status_code}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    else:
        return {"status": "no_credentials", "message": "Pushover credentials not found"}

def record_user_details(email: str, name: str = "Name not provided", notes: str = "not provided") -> Dict[str, Any]:
    """Record user details and send notification"""
    message = f"Recording interest from {name} with email {email} and notes {notes}"
    push_notification(message)
    return {"recorded": "ok", "email": email, "name": name, "notes": notes}

def record_unknown_question(question: str) -> Dict[str, Any]:
    """Record questions that couldn't be answered"""
    message = f"Recording unknown question: {question}"
    push_notification(message)
    return {"recorded": "ok", "question": question}

def search_knowledge_base(query: str, vector_store) -> Dict[str, Any]:
    """Search the knowledge base using vector similarity"""
    try:
        results = vector_store.search(query, n_results=3)
        formatted_results = []
        for result in results:
            formatted_results.append({
                "content": result["document"],
                "metadata": result["metadata"],
                "relevance_score": 1 - result["distance"] if result["distance"] else 1.0
            })
        
        return {
            "status": "success",
            "results": formatted_results,
            "query": query
        }
    except Exception as e:
        return {"status": "error", "error": str(e), "query": query}

# Tool definitions for OpenAI API
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "record_user_details",
            "description": "Use this tool to record that a user is interested in being in touch and has provided an email address.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The email address of the user (required)."
                    },
                    "name": {
                        "type": "string",
                        "description": "The user's name, if provided."
                    },
                    "notes": {
                        "type": "string",
                        "description": "Additional context or notes about the conversation."
                    }
                },
                "required": ["email"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "record_unknown_question",
            "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question that couldn't be answered"
                    }
                },
                "required": ["question"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "Search the knowledge base for relevant information to answer user questions",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to find relevant information"
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        }
    }
]

def handle_tool_calls(tool_calls, vector_store=None):
    """Handle tool calls from the LLM"""
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        print(f"Tool called: {tool_name}")
        
        # Execute the appropriate tool
        if tool_name == "record_user_details":
            result = record_user_details(**arguments)
        elif tool_name == "record_unknown_question":
            result = record_unknown_question(**arguments)
        elif tool_name == "search_knowledge_base":
            result = search_knowledge_base(arguments["query"], vector_store)
        else:
            result = {"error": f"Unknown tool: {tool_name}"}
        
        results.append({
            "role": "tool",
            "content": json.dumps(result),
            "tool_call_id": tool_call.id
        })
    
    return results