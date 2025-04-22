# MODEL = "openai/gpt-4.1" # Unsure on performance, more expesnvie
# MODEL = "anthropic/claude-sonnet" # Best, most expesnvie. So far no other model seems to work
# MODEL = "lbl/cborg-chat:latest" # Free
MODEL = "lbl/cborg-coder:latest" # Free, least compute, seems to perform better and faster than llama 
# MODEL = "lbl/llama" # Free, Does not do well. Needs help to come up with single class answers. Often comes up with wrong thing
# MODEL = "google/gemini-flash-exp" # Free during experiment, temporary, seems to perform adequately, not as well as sonnet
# MODEL = "google/gemini-flash" # Cheapest tokens
# MODEL = "anthropic/claude-haiku" # More expensive, less performant than gemeni

import asyncio
from devtools import pprint
from pydantic import BaseModel
from pydantic_ai import Agent, capture_run_messages
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.mcp import MCPServerStdio

import openai # CBORG API Proxy Server is OpenAI-compatible through the openai module
import yaml
import json

# allowing nest_asyncio for running in ipynb or ipy
import nest_asyncio
nest_asyncio.apply()

with open('/Users/lazlopaul/Desktop/cborg/api_key.yaml', 'r') as file:
    config = yaml.safe_load(file)
    API_KEY = config['key']
    BASE_URL = config['base_url']

client = openai.OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)
SYSTEM_PROMPT = None
# llama needs a little help returning a single class
def get_simple_completion(prompt, system_prompt):
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
    response = client.chat.completions.create(
            model=MODEL, 
            messages = messages,
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
            }],
            tool_choice={"type": "function", "function": {"name": "provide_class_name"}},  # Force use of this tool
            temperature=0.0  
        )

    # Extract the single word from the function call
    tool_call = response.choices[0].message.tool_calls[0]
    function_args = json.loads(tool_call.function.arguments)
    
    return function_args.get("class_name")

# server = MCPServerStdio(
#     "uv",
#     args=[
#         "run",
#         "--with",
#         "mcp[cli]",
#         "--with",
#         "rdflib",
#         "--with",
#         "oxrdflib",
#         "mcp",
#         "run",
#         "brick.py"
#     ],
# )

model = OpenAIModel(
        model_name=MODEL,
        # i'm using LM Studio here, but you could use any other provider that exposes
        # an OpenAI-like API
        provider=OpenAIProvider(base_url=BASE_URL, api_key=API_KEY),
    )

class S223_Type(BaseModel):
    name: str

agent = Agent(
    model,
    output = S223_Type
    # mcp_servers=[server],
)

async def run_agent(prompt, system_prompt = SYSTEM_PROMPT):
    with capture_run_messages() as messages:
        result = await agent.run(prompt, system_prompt=system_prompt)
        # async with agent.run_mcp_servers():
        #     result = await agent.run(prompt, system_prompt=system_prompt)
    # pprint(messages)
    return result
    

def get_completion(prompt, system_prompt = SYSTEM_PROMPT, as_agent= False):

    """
    Get a completion for a given prompt, with an optional system prompt. Optionally runs the prompt through the mcp server.

    Args:
        prompt (str): The prompt to complete.
        system_prompt (str, optional): The system prompt to provide to the model. Defaults to None.
        with_mcp (bool, optional): Whether to run the prompt through the mcp server. Defaults to False.

    Returns:
        str: The completed prompt.
    """
    if as_agent:
        response = asyncio.run(run_agent(prompt, system_prompt))
    else:
        response = get_simple_completion(prompt, system_prompt)

    return response