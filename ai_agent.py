from anthropic import Anthropic
import json

client = Anthropic(api_key="your-key")

def chat_with_data(user_question: str):
    # Define tools Claude can use
    tools = [
        {
            "name": "get_player_stats",
            "description": "Get stats for a specific player",
            "input_schema": {
                "type": "object",
                "properties": {
                    "player_name": {"type": "string"}
                }
            }
        },
        {
            "name": "get_top_scorers",
            "description": "Get top goal scorers",
            ...
        }
    ]
    
    # Send to Claude
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        tools=tools,
        messages=[{
            "role": "user", 
            "content": user_question
        }]
    )
    
    # Handle tool calls (Claude asking for data)
    # Return final answer
