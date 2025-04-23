# MODEL = "openai/gpt-4.1" # Unsure on performance, more expesnvie
# MODEL = "anthropic/claude-sonnet" # Best, most expesnvie. So far no other model seems to work
# MODEL = "lbl/cborg-chat:latest" # Free
MODEL = "lbl/cborg-coder:latest" # Free, least compute, seems to perform better and faster than llama 
# MODEL = "lbl/llama" # Free, Does not do well. Needs help to come up with single class answers. Often comes up with wrong thing
# MODEL = "google/gemini-flash-exp" # Free during experiment, temporary, seems to perform adequately, not as well as sonnet
# MODEL = "google/gemini-flash" # Cheapest tokens
# MODEL = "anthropic/claude-haiku" # More expensive, less performant than gemeni

import openai # CBORG API Proxy Server is OpenAI-compatible through the openai module
import yaml
import json

with open('../../../cborg/api_key.yaml', 'r') as file:
    config = yaml.safe_load(file)
    API_KEY = config['key']
    BASE_URL = config['base_url']

client = openai.OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)
SYSTEM_PROMPT = None
# llama needs a little help returning a single class
def get_completion(prompt, system_prompt = SYSTEM_PROMPT, as_agent = False, comma_sep_list = False):
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]
    if system_prompt:
        messages.append(
            {
                "role": "system",
                "content":system_prompt
            }
        )
    if comma_sep_list:
        tools=[{
            "type": "function",
            "function": {
                "name": "provide_class_names",
                "description": "Provide a list of class names",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "class_names": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "description": "A class name"
                            },
                            "description": "List of class names"
                        }
                    },
                    "required": ["class_names"]
                }
            }
        }]
        function_key = "class_names"
        tool_choice = {"type": "function", "function": {"name": "provide_class_names"}}
    else:
        tools=[{  # Note: newer versions use 'tools' instead of 'functions'
                "type": "function",
                "function": {
                    "name": "provide_class_name",
                    "description": "Provide the single class name as the answer",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "class_name": {
                                "type": "string",
                                "description": "the class name of the answer"
                            }
                        },
                        "required": ["class_name"]
                    }
                }
            }]
        function_key = "class_name"
        tool_choice = {"type": "function", "function": {"name": "provide_class_name"}}
        
    response = client.chat.completions.create(
            model=MODEL, 
            messages = messages,
            tools=tools,
            tool_choice=tool_choice,  # Force use of this tool
            temperature=0.0  
        )

    # Extract the single word from the function call
    tool_call = response.choices[0].message.tool_calls[0]
    function_args = json.loads(tool_call.function.arguments)
    
    return function_args.get(function_key)